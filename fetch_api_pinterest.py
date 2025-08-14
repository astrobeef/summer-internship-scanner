"""
Databricks internships come from a JSON GET endpoint.
"""
# first-party
from __future__ import annotations
import json
import requests
# local
from constants import (
    TIMEOUT,
    HITS_SAVE_DIR,
    JOBS_SAVE_DIR,
    Job
)
from util_fetch_io import (
    save_hits,
    save_jobs,
    load_objects
    )



SOURCE = "pinterest"

INTERNSHIP_DEPARTMENT   = "University"
DEPARTMENT_METADATA_KEY = "Careers Page Department"

# Greenhouse API constants
BASE_GREENHOUSE_API: str = "https://boards-api.greenhouse.io/v1/boards"
GREENHOUSE_BOARD_TOKEN: str = "pinterest"  # public token used by the embed
ENDPOINT: str = f"{BASE_GREENHOUSE_API}/{GREENHOUSE_BOARD_TOKEN}/jobs"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "application/json",
    "Referer": "https://boards.greenhouse.io/"
}

#######
# I/O #
#######

def _parse_id(hit) -> str:
    return str(hit["id"])

############
#  FETCH   #
############

def _is_internship(hit):
    for m in hit["metadata"]:
        if m["name"].strip().lower() == DEPARTMENT_METADATA_KEY.lower():
            values = m["value"]
            if isinstance(values, str):
                values = [values]
            if isinstance(values, list):
                return any(
                    isinstance(v, str) and v.strip().lower() == INTERNSHIP_DEPARTMENT.lower()
                    for v in values
                )
            return False
    return False

def _fetch_hits(
    timeout_seconds :int,
    *,
    save_local      :bool,
    verbose         :bool,
) -> list:
    try:
        response = requests.get(
            url=ENDPOINT,
            headers=HEADERS,
            timeout=timeout_seconds
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("Databricks request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Databricks request failed: {response.status_code} {response.text}"
        ) from exc

    data = response.json()

    # Greenhouse schema: {"jobs": [ ... ]}
    hits = data["jobs"]
    # Filter for internships
    hits = [h for h in hits if _is_internship(h)]
    verbose and print(f"Fetched {len(hits)} jobs from Greenhouse (Databricks board)")
    if save_local and hits:
        save_hits(hits, source=SOURCE, id_fn=_parse_id, verbose=verbose)
    return hits

LOCATION_COMMA_SEP: str        = ","
LOCATION_HYPHEN_SEP: str       = "-"
TOKEN_MULTIPLE_LOCATIONS: str  = "multiple locations"
TOKEN_BLANK: str               = "blank"
TOKEN_REMOTE: str              = "remote"

def _format_location(loc_name: str | None) -> str:
    if not loc_name:
        return ""
    raw = loc_name.strip()
    if not raw:
        return ""
    if raw.strip().lower() == TOKEN_MULTIPLE_LOCATIONS:
        return "Multiple Locations"
    parts = [p.strip() for p in raw.split(LOCATION_COMMA_SEP)]
    parts = [p for p in parts if p.lower() != TOKEN_BLANK]
    if len(parts) >= 2:
        city = parts[0]
        country = parts[-1]
        return f"{city}{LOCATION_COMMA_SEP} {country}"
    single = parts[0] if parts else raw
    if LOCATION_HYPHEN_SEP in single:
        lhs, rhs = (s.strip() for s in single.split(LOCATION_HYPHEN_SEP, 1))
        if lhs.lower() == TOKEN_REMOTE and rhs:
            return f"{lhs} {LOCATION_HYPHEN_SEP} {rhs}"
    return single

# NOTE: All the keys referenced were derived from the .har file
def _parse_jobs_from_hits(
    hits: list,
    *,
    save_local: bool,
    verbose: bool
) -> list[Job]:
    jobs: list[Job] = []

    for h in hits:
        dept = INTERNSHIP_DEPARTMENT    # Because of filtering in `_fetch_hits(..)`, department will always be internship
        loc_name = h["location"]["name"]
        company  = h["company_name"]
        job: Job = {
            "source"        : SOURCE,
            "id"            : _parse_id(h),
            "title"         : h["title"],
            "url"           : h["absolute_url"],
            "location"      : _format_location(loc_name),
            "contract_type" : "",
            "unique_meta"   : {
                "department"     : dept,
                "company"        : company,
                "requisition_id" : h["requisition_id"],
                "first_published": h["first_published"],
                "updated_at"     : h["updated_at"],
                "education"      : h.get("education", ""),
            },
        }
        jobs.append(job)


    if save_local:
        save_jobs(jobs, verbose=verbose)
    return jobs

###########
# EXECUTE #
###########

def parse_jobs_fetch_hits(
    timeout_seconds :int    = TIMEOUT,
    *,
    save_local      :bool   = True,
    verbose         :bool   = False,
) -> list[Job]:
    hits = _fetch_hits(timeout_seconds, save_local=save_local, verbose=verbose)
    return _parse_jobs_from_hits(hits, save_local=save_local, verbose=verbose)

def parse_jobs_cached_hits(
    *,
    save_local  :bool = True,
    verbose     :bool = False
) -> list[Job]:
    hits = load_objects(source=SOURCE, dir=HITS_SAVE_DIR, verbose=verbose)
    return _parse_jobs_from_hits(hits, save_local=save_local, verbose=verbose)

def load_cached_jobs(
    *,
    verbose :bool = False
) -> list[Job]:
    return load_objects(source=SOURCE, dir=JOBS_SAVE_DIR, verbose=verbose)

if __name__ == "__main__":
    for job in parse_jobs_fetch_hits(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")
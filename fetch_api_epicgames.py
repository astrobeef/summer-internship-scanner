"""
Epic Games internships come from a Greenhouse-proxy JSON GET endpoint.
# NOTE Right now the endpoint returns an empty ``hits`` list
"""
# first-party
from __future__ import annotations
import requests, json, glob, os
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

SOURCE = "epicgames"

# Greenhouse proxy from epicgames.har
ENDPOINT = (
    "https://greenhouse-service.debc.live.use1a.on.epicgames.com/"
    "api/job?limit=50&skip=0&page=1&type=Intern"
)
# NOTE: There are no internships, so the endpoint below can be used for testing
# ENDPOINT = (
#     "https://greenhouse-service.debc.live.use1a.on.epicgames.com/api/job?limit=50&skip=0&page=1&company=Epic%20Games&department=Engineering&product=Quixel"
# )

# Derived from epicgames.har
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.epicgames.com",
    "Referer": "https://www.epicgames.com/",
}

#######
# I/O #
#######

def _parse_id(hit) -> str:
    return hit["id"]

############
#  FETCH   #
############

# NOTE: All the keys referenced were derived from the .har file
def _fetch_hits(
    timeout_seconds :int,
    *,
    save_local      :bool,
    verbose         :bool,
) -> list:
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            timeout=timeout_seconds
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("Epic Games request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Epic Games request failed: {response.status_code} {response.text}"
        ) from exc
    data  = response.json()
    hits  = data.get("hits", [])
    total = data.get("total", 0)
    verbose and print(f"Fetched {len(hits)} / total={total} hits from Epic")
    if save_local and hits:
        save_hits(hits, source=SOURCE, id_fn=_parse_id, verbose=verbose)
    return hits

def _format_location(loc_name: str | None) -> str:
    """
    Convert Epic's location.name to a user-friendly string.

    - 'Stockholm,Stockholm County,Sweden'     -> 'Stockholm, Sweden'
    - 'BLANK, BLANK, Multiple Locations'      -> 'Multiple Locations'
    - Anything ending with 'Multiple Locations' (even with blanks) -> 'Multiple Locations'
    """
    if not loc_name:
        return ""
    parts = [p.strip() for p in loc_name.split(",")]
    # Remove any parts that are just 'BLANK' (case-insensitive)
    parts = [p for p in parts if p.lower() != "blank"]
    if parts and parts[-1].lower() == "multiple locations":
        return "Multiple Locations"
    if len(parts) >= 2:
        # First is city, last is country
        return f"{parts[0]}, {parts[-1]}"
    raise ValueError(f"Unhandled location name \"{loc_name}\"")

# NOTE: All the keys referenced were derived from the .har file
def _parse_jobs_from_hits(
    hits        :list,
    *,
    save_local  :bool,
    verbose     :bool
) -> list[Job]:
    jobs: list[Job] = []
    for h in hits:
        location_str = h.get("location", {}).get("name", "")
        job: Job = {
            "source"        :SOURCE,
            "id"            :_parse_id(h),
            "title"         :h["title"],
            "url"           :h["absolute_url"],
            "location"      :_format_location(location_str),
            "contract_type" :h["type"],
            "unique_meta"   :{
                    "department":      h.get("department", ""),
                    "company":         h.get("company_name", ""),
                    "remote":          h.get("remote", False),
                    "updated_epoch":   h.get("updated_at"),
                }
        }
        jobs.append(job)
    if save_local:
        save_jobs(jobs, SOURCE, verbose=verbose)
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
    for job in parse_jobs_cached_hits(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")
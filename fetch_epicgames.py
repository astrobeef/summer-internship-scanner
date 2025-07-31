"""
fetch_epic.py
Epic Games internships come from a Greenhouse-proxy JSON GET endpoint.
Right now the endpoint returns an empty ``hits`` list; if that changes
the script raises NotImplementedError so parsers can be added quickly.
"""
# first-party
from __future__ import annotations
import requests, json, glob, os
# local
from constants import (
    TIMEOUT,
    HITS_SAVE_DIR,
    JOBS_SAVE_DIR,
    build_path,
)

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

def _build_epic_path(
        job_id      :str,
        *,
        dir         :str,
        make_dir    :bool
) -> str:
    return build_path("epic", job_id, dir=dir, make_dir=make_dir)

def _save_hits(
        hits    :list,
        *,
        verbose :bool = False
) -> None:
    for h in hits:
        job_id = str(h.get("id", "None"))
        if job_id == "None":
            raise ValueError('Could not find id in hit')
        path = _build_epic_path(job_id, dir=HITS_SAVE_DIR, make_dir=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(h, f, indent=2, ensure_ascii=False)
    verbose and print(f"Saved {len(hits)} raw hits")

def _save_jobs(
        jobs: list,
        *,
        verbose: bool = False
) -> None:
    for j in jobs:
        path = _build_epic_path(j["id"], dir=JOBS_SAVE_DIR, make_dir=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(j, f, indent=2, ensure_ascii=False)

def _load(
        dir         :str,
        verbose     :bool = False
) -> list:
    elements = []
    pattern = _build_epic_path("*", dir=dir, make_dir=False)
    for path in glob.glob(pattern):
      with open(path, encoding="utf-8") as f:
          e = json.load(f)
      elements.append(e)
    verbose and print(f"Loaded {len(elements)} elements from pattern: \"{pattern}\"")
    return elements

############
#  FETCH   #
############

# NOTE: All the keys referenced were derived from the .har file
def _fetch_hits(
    *,
    timeout_seconds: int,
    save_local: bool,
    verbose: bool,
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
        _save_hits(hits, verbose=verbose)
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
) -> list:
    jobs: list = []
    for h in hits:
        location_str = h.get("location", {}).get("name", "")
        job = (
            {
                "source": "Epic Games",
                "id": h["id"],
                "title":  h["title"],
                "url":    h["absolute_url"],
                "location": _format_location(location_str),
                "contract_type":  h["type"],
                "unique_meta": {
                    "department":      h.get("department", ""),
                    "company":         h.get("company_name", ""),
                    "remote":          h.get("remote", False),
                    "updated_epoch":   h.get("updated_at"),
                },
            }
        )
        jobs.append(job)
    if save_local:
        _save_jobs(jobs, verbose=verbose)
    return jobs

###########
# EXECUTE #
###########

def parse_jobs_fetch_hits(
    timeout_seconds :int    = TIMEOUT,
    *,
    save_local      :bool   = True,
    verbose         :bool   = False,
) -> list:
    hits = _fetch_hits(timeout_seconds=timeout_seconds, save_local=save_local, verbose=verbose)
    return _parse_jobs_from_hits(hits, verbose=verbose)

def parse_jobs_cached_hits(
        *,
        save_local  :bool = True,
        verbose     :bool = False
) -> list:
    hits = _load(HITS_SAVE_DIR, verbose=verbose)
    return _parse_jobs_from_hits(hits, save_local=save_local, verbose=verbose)

def load_cached_jobs(
        *,
        verbose :bool = False
) -> list:
    return _load(JOBS_SAVE_DIR, verbose=verbose)

if __name__ == "__main__":
    for job in parse_jobs_cached_hits(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")
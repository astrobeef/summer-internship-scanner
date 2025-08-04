"""
Fetches AMD jobs from the public careers API.
"""
from __future__ import annotations
import json
import requests
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

SOURCE = "amd"

# Derived from HAR file
ENDPOINT = (
    "https://careers.amd.com/api/jobs?page=1&categories=Student%20/%20Intern%20/%20Temp&sortBy=relevance&descending=false&internal=false"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://careers.amd.com/careers-home/jobs?page=1&categories=Student%20%2F%20Intern%20%2F%20Temp",
    "Referer": "https://careers.amd.com/careers-home/jobs?page=1&categories=Student%20%2F%20Intern%20%2F%20Temp",
}

def _parse_id(hit) -> str:
    return str(hit["data"]["req_id"])

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
        raise RuntimeError("AMD request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"AMD request failed: {response.status_code} {response.text}"
        ) from exc
    data = response.json()
    hits = data["jobs"]
    verbose and print(f"Fetched {len(hits)} hits from AMD")
    if save_local and hits:
        save_hits(hits, source=SOURCE, id_fn=_parse_id, verbose=verbose)
    return hits

def _format_location(data) -> str:
    city    = data["city"]
    country = data["country"]
    if city and country:
        return f"{city}, {country}"
    return city or country

def _parse_jobs_from_hits(
    hits        :list,
    *,
    save_local  :bool,
    verbose     :bool
) -> list[Job]:
    jobs: list[Job] = []
    for h in hits:
        data = h["data"]
        job: Job = {
            "source"        : SOURCE,
            "id"            : _parse_id(h),
            "title"         : data["title"],
            "url"           : data["apply_url"],
            "location"      : _format_location(data),
            "contract_type" : data["category"][0],
            "unique_meta": {
                "post_date"         : data["posted_date"],
                "created_date"      : data["create_date"],
            }
        }
        jobs.append(job)
    if save_local:
        save_jobs(jobs, verbose=verbose)
    return jobs

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
    verbose: bool = False
) -> list[Job]:
    return load_objects(source=SOURCE, dir=JOBS_SAVE_DIR, verbose=verbose)

if __name__ == "__main__":
    for job in parse_jobs_fetch_hits(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")

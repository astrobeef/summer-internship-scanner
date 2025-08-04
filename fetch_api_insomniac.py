"""
Insomniac Games jobs are fetched from the Greenhouse API endpoint.
"""
from __future__ import annotations
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

SOURCE = "insomniac"

# Derived from HAR file: this endpoint returns all jobs with full content.
ENDPOINT = (
    "https://boards-api.greenhouse.io/v1/boards/insomniac/jobs?content=true"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://insomniac.games",
    "Referer": "https://insomniac.games/",
}

def _parse_id(hit) -> str:
    return str(hit.get("id", ""))

def _format_location(job: dict) -> str:
    # Greenhouse returns a "location" dict with "name" field, or may have multiple offices.
    loc = job.get("location", {})
    name = loc.get("name", "") if isinstance(loc, dict) else ""
    if not name:
        return ""
    parts = [p.strip() for p in name.split(",")]
    parts = [p for p in parts if p.lower() != "blank"]
    if parts and parts[-1].lower() == "multiple locations":
        return "Multiple Locations"
    if len(parts) >= 2:
        return f"{parts[0]}, {parts[-1]}"
    return name

def _fetch_hits(
    timeout_seconds: int,
    *,
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
        raise RuntimeError("Insomniac request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Insomniac request failed: {response.status_code} {response.text}"
        ) from exc
    data = response.json()
    # Greenhouse returns "jobs" not "hits"
    hits = data.get("jobs", [])
    total = len(hits)
    verbose and print(f"Fetched {total} jobs from Insomniac")
    if save_local and hits:
        save_hits(hits, source=SOURCE, id_fn=_parse_id, verbose=verbose)
    return hits

def _parse_jobs_from_hits(
    hits: list,
    *,
    save_local: bool,
    verbose: bool
) -> list[Job]:
    jobs: list[Job] = []
    for h in hits:
        job: Job = {
            "source": SOURCE,
            "id": _parse_id(h),
            "title": h["title"],
            "url": f"https://job-boards.greenhouse.io/insomniac/jobs/{_parse_id(h)}",       # Post shown at greenhouse. Absolute URL does not parse well
            "location": _format_location(h),
            "contract_type": "",    # not provided
            "unique_meta": {
                "absolute_url"  :h["absolute_url"],
                "updated_at": h.get("updated_at", ""),
                "first_published": h.get("first_published", ""),
            }
        }
        jobs.append(job)
    if save_local:
        save_jobs(jobs, verbose=verbose)
    return jobs

def parse_jobs_fetch_hits(
    timeout_seconds: int = TIMEOUT,
    *,
    save_local: bool = True,
    verbose: bool = False,
) -> list[Job]:
    hits = _fetch_hits(timeout_seconds, save_local=save_local, verbose=verbose)
    return _parse_jobs_from_hits(hits, save_local=save_local, verbose=verbose)

def parse_jobs_cached_hits(
    *,
    save_local: bool = True,
    verbose: bool = False
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

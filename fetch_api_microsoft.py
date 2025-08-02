"""
Fetches Microsoft jobs from the public careers API.
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

URL = "https://jobs.careers.microsoft.com/global/en/search?lc=Canada&lc=United%20States&d=Software%20Engineering&exp=Students%20and%20graduates&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true"

SOURCE = "microsoft"

# Derived from HAR file: Software Engineering, Students and graduates, US+Canada, English
ENDPOINT = (
    "https://gcsservices.careers.microsoft.com/search/api/v1/search"
    "?lc=Canada&lc=United%20States"
    "&d=Software%20Engineering"
    "&exp=Students%20and%20graduates"
    "&l=en_us"
    "&pg=1"
    "&pgSz=20"
    "&o=Relevance"
    "&flt=true"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://jobs.careers.microsoft.com",
    "Referer": "https://jobs.careers.microsoft.com/",
}

def _parse_id(hit) -> str:
    # "jobId" is the unique identifier in Microsoft job data.
    return str(hit.get("jobId", ""))

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
        raise RuntimeError("Microsoft request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Microsoft request failed: {response.status_code} {response.text}"
        ) from exc
    data = response.json()
    hits = data["operationResult"]["result"]["jobs"]
    total = data.get("totalJobs", len(hits))
    verbose and print(f"Fetched {len(hits)} / total={total} jobs from Microsoft")
    if save_local and hits:
        save_hits(hits, source=SOURCE, id_fn=_parse_id, verbose=verbose)
    return hits

def _parse_jobs_from_hits(
    hits        :list,
    *,
    save_local  :bool,
    verbose     :bool
) -> list[Job]:
    jobs: list[Job] = []
    for h in hits:
        properties = h["properties"]
        job: Job = {
            "source"        : SOURCE,
            "id"            : _parse_id(h),
            "title"         : h["title"],
            "url"           : URL,  # Not included within hit
            "location"      : properties["primaryLocation"],
            "contract_type" : properties["jobType"],
            "unique_meta": {
                "post_date"         : h["postingDate"],
                "work_site_flex"    : properties["workSiteFlexibility"],
                "discipline"        : properties["discipline"],
                "roleType"          : properties["roleType"],
                "employmentType"    : properties["employmentType"]
            }
        }
        jobs.append(job)
    if save_local:
        save_jobs(jobs, SOURCE, verbose=verbose)
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

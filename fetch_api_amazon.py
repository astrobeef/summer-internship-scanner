"""
Amazon internship jobs fetched from the /api/jobs/search?is_als=true POST endpoint.
"""
from __future__ import annotations
import requests, json
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

SOURCE   = "amazon"
ENDPOINT = "https://www.amazon.jobs/api/jobs/search?is_als=true"

# Key taken from the HAR; Amazon rotates this periodically.
_API_KEY = "PbxxNwIlTi4FP5oijKdtk3IrBF5CLd4R4oPHsKNh"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "application/json",
    "Origin": "https://www.amazon.jobs",
    "Referer": (
        "https://www.amazon.jobs/content/en/career-programs/university/"
        "internships-for-students?employment-type%5B%5D=Intern&country%5B%5D=US"
    ),
    "Content-Type": "text/plain;charset=UTF-8",
    "x-api-key": _API_KEY,
}

# Payload copied verbatim from the successful HAR request
POST_DATA = {
    "accessLevel": "EXTERNAL",
    "contentFilterFacets": [
        {
            "name": "primarySearchLabel",
            "requestedFacetCount": 9999,
            "values": [{"name": "studentprograms.team-internships-for-students"}]
        }
    ],
    "excludeFacets": [
        {
            "name": "isConfidential",
            "values": [{"name": "1"}]
        },
        {
            "name": "businessCategory",
            "values": [{"name": "a-confidential-job"}]
        }
    ],
    "filterFacets": [],
    "includeFacets": [],
    "jobTypeFacets": [
        {
            "name": "employeeClass",
            "values": [{"name": "Intern"}]
        }
    ],
    "locationFacets": [[
        {
            "name": "country",
            "requestedFacetCount": 9999,
            "values": [{"name": "US"}]
        },
        {"name": "normalizedStateName", "requestedFacetCount": 9999},
        {"name": "normalizedCityName",  "requestedFacetCount": 9999}
    ]],
    "query": "",
    "size": 10,
    "start": 0,
    "treatment": "OM",
    "cookieInfo": "",         # Leaving blank; server accepts empty string
    "sort": {"sortOrder": "DESCENDING", "sortType": "SCORE"}
}

def _parse_id(hit) -> str:
    fields = hit["fields"]
    return str(fields["icimsJobId"][0])

def _format_location(fields) -> str:
    return fields["normalizedLocation"][0]
    # if the above does not work, there's also "country" and "city" within fields

def _fetch_hits(
    timeout_seconds :int,
    *,
    save_local      :bool,
    verbose         :bool,
) -> list:
    try:
        response = requests.post(
            ENDPOINT,
            headers=HEADERS,
            data=json.dumps(POST_DATA),
            timeout=timeout_seconds
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("Amazon request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Amazon request failed: {response.status_code} {response.text}"
        ) from exc
    data = response.json()
    hits  = data["searchHits"]
    total = len(hits)
    verbose and print(f"Fetched {len(hits)} / total={total} Amazon hits")
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
        fields   = h["fields"]
        job_url = "https://www.amazon.jobs/en/jobs/" + _parse_id(h)  # URL not listed, but amazon job posts can be autocompleted using the 'icimsJobId'
        job: Job = {
            "source"       : SOURCE,
            "id"           : _parse_id(h),
            "title"        : fields["title"][0],
            "url"          : job_url,
            "location"     : _format_location(fields),
            "contract_type": fields["employeeClass"][0],
            "unique_meta"  : {
                "job_role"      : fields["jobRole"][0],
                "job_family"    : fields["jobFamily"][0],
                "work_hours"    : fields["scheduleTypeId"][0],
                "post_date"     : fields["createdDate"][0],
                "apply_url"     : fields["urlNextStep"][0]
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

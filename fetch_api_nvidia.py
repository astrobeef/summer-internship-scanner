"""
NVIDIA jobs are fetched from the Workday API endpoint via POST.
No cookies or CSRF token are needed for public listings.
# NOTE: Workday response
"""
# first-party
import requests
from constants import (
    TIMEOUT,
    HITS_SAVE_DIR,
    JOBS_SAVE_DIR,
    Job
)
# local
from util_fetch_io import (
    save_hits,
    save_jobs,
    load_objects
)

SOURCE = "nvidia"

# Derived from HAR
# NOTE: Filtering is done in PAYLOAD, not in URL
ENDPOINT = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"

# Derived from HAR
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Referer": "https://nvidia.wd5.myworkdayjobs.com/External",
}

# Properties parsed from HAR. No internships atm, so unable to filter for them.
PAYLOAD = {
    "appliedFacets": {
        "locationHierarchy1":["2fcb99c455831013ea529c3b93ba3236",
                              "2fcb99c455831013ea52fb338f2932d8"],
        "workerSubType":["0c40f6bd1d8f10adf6dae42e46d44a17"]
    },
    "limit": 20,
    "offset": 0,
    "searchText": ""
}

#######
# I/O #
#######

def _parse_id(hit) -> str:
    return hit.get("bulletFields", "None")[0]

############
#  FETCH   #
############

# NOTE: All the keys referenced were derived from the .har file
def _fetch_hits(
    timeout_seconds: int,
    *,
    save_local: bool,
    verbose: bool,
) -> list:
    try:
        response = requests.post(
            ENDPOINT,
            headers =HEADERS,
            json    =PAYLOAD,
            timeout =timeout_seconds
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("Activision request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Activision request failed: {response.status_code} {response.text}"
        ) from exc
    data = response.json()
    hits = data.get("jobPostings", [])
    total = data.get("total", 0)
    verbose and print(f"Fetched {len(hits)} / total={total} hits from Activision")
    if save_local and hits:
        save_hits(hits, source=SOURCE, id_fn=_parse_id, verbose=verbose)
    return hits

# NOTE: All the keys referenced were derived from the .har file
def _parse_jobs_from_hits(
    hits        :list,
    *,
    save_local  :bool,
    verbose     :bool
) -> list[Job]:
    jobs: list[Job] = []
    for h in hits:
        job: Job = {
            "source"        : SOURCE,
            "id"            : _parse_id(h),
            "title"         : h.get("title", ""),
            "url"           : "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite" + h.get("externalPath", ""),
            "location"      : h["locationsText"],
            "contract_type" : "",        # Not provided
            "unique_meta"   : {
                "postedOn": h.get("postedOn", ""),
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
    for job in parse_jobs_fetch_hits(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")

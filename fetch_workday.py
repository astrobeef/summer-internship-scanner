"""
Abbott jobs are fetched from the Workday API endpoint via POST.
No cookies or CSRF token are needed for public listings.
# NOTE: Workday response
"""
# first-party
import requests, json
# local
from constants import (
    TIMEOUT,
    HITS_SAVE_DIR,
    JOBS_SAVE_DIR,
    Job,
    WorkdaySite
)
from util_fetch_io import (
    save_hits,
    save_jobs,
    load_objects
)

workday_sites: list[WorkdaySite] = [
        {
            "source"            :"abbott",
            "endpoint"          :"https://abbott.wd5.myworkdayjobs.com/wday/cxs/abbott/abbottcareers/jobs",
            "referer"           :"https://abbott.wd5.myworkdayjobs.com/abbottcareers?Location_Country=bc33aa3152ec42d4995f4791a106ed09&Location_Country=a30a87ed25634629aa6c3958aa2b91ea&workerSubType=d0663057a84410077d944a83d8896dd3",
            "applied_facets"    :{
                "Location_Country"   :["bc33aa3152ec42d4995f4791a106ed09",
                                       "a30a87ed25634629aa6c3958aa2b91ea"],
                "workerSubType"     :["d0663057a84410077d944a83d8896dd3"]
            },
            "job_url_prefix"    :"https://abbott.wd5.myworkdayjobs.com/en-US/abbottcareers"
        },
        {
            "source"            :"activision",
            "endpoint"          :"https://activision.wd1.myworkdayjobs.com/wday/cxs/activision/External/jobs",
            "referer"           :"https://activision.wd1.myworkdayjobs.com/External",
            "applied_facets"    :{
                "locationCountry"   :["bc33aa3152ec42d4995f4791a106ed09"],
                "jobFamilyGroup"    :["d5b22c2cbd48013cad00235c009aaa19",
                                      "d5b22c2cbd480127a6ee0a5c009a9e19"]
            },
            "job_url_prefix"    :"https://activision.wd1.myworkdayjobs.com/en-US/External"
        },
        {
            "source"            :"intel",
            "endpoint"          :"https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs",
            "referer"           :"https://intel.wd1.myworkdayjobs.com/External?workerSubType=dc8bf79476611087dfde99931439ae75",
            "applied_facets"    :{
                "workerSubType"   :["dc8bf79476611087dfde99931439ae75"],
            },
            "job_url_prefix"    :"https://intel.wd1.myworkdayjobs.com/en-US/External"
        },
        {
            "source"            :"intel",
            "endpoint"          :"https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs",
            "referer"           :"https://intel.wd1.myworkdayjobs.com/External?workerSubType=dc8bf79476611087dfde99931439ae75",
            "applied_facets"    :{
                "workerSubType"   :["dc8bf79476611087dfde99931439ae75"],
            },
            "job_url_prefix"    :"https://intel.wd1.myworkdayjobs.com/en-US/External"
        },
        {
            "source"            :"nvidia",
            "endpoint"          :"https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs",
            "referer"           :"https://nvidia.wd5.myworkdayjobs.com/External",
            "applied_facets"    :{
                "locationHierarchy1":["2fcb99c455831013ea529c3b93ba3236",
                              "2fcb99c455831013ea52fb338f2932d8"],
                "workerSubType"     :["0c40f6bd1d8f10adf6dae42e46d44a17"]
            },
            "job_url_prefix"    :"https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"
        },
    ]

# Derived from HAR
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Referer": "%s",
}

# Properties parsed from HAR. No internships atm, so unable to filter for them.
# NOTE: Filtering is done in PAYLOAD, not in URL
PAYLOAD = {
    "appliedFacets": "%s",
    "limit": 20,
    "offset": 0,
    "searchText": ""
}

#######
# I/O #
#######

def _parse_id(hit) -> str:
    return hit["bulletFields"][0]

############
#  FETCH   #
############

# NOTE: All the keys referenced were derived from the .har file
def _fetch_hits(
    timeout_seconds : int,
    *,
    source          :str,
    endpoint        :str,
    referer         :str,
    applied_facets  :dict,
    save_local      :bool,
    verbose         :bool,
) -> list:
    headers = HEADERS.copy()
    headers["Referer"] = referer
    payload = PAYLOAD.copy()
    payload["appliedFacets"] = applied_facets
    try:
        response = requests.post(
            endpoint,
            headers =headers,
            json    =payload,
            timeout =timeout_seconds
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("{source} request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"{source} request failed: {response.status_code} {response.text}"
        ) from exc
    data = response.json()
    hits = data.get("jobPostings", [])
    total = data.get("total", 0)
    verbose and print(f"Fetched {len(hits)} / total={total} hits from {source}")
    if save_local and hits:
        save_hits(hits, source=source, id_fn=_parse_id, verbose=verbose)
    return hits

# NOTE: All the keys referenced were derived from the .har file
def _parse_jobs_from_hits(
    hits            :list,
    *,
    source          :str,
    job_url_prefix  :str,
    save_local      :bool,
    verbose         :bool
) -> list[Job]:
    jobs: list[Job] = []
    for h in hits:
        job: Job = {
            "source"        : source,
            "id"            : _parse_id(h),
            "title"         : h.get("title", ""),
            "url"           : job_url_prefix + h.get("externalPath", ""),
            "location"      : h["locationsText"],
            "contract_type" : "",        # Not provided
            "unique_meta"   : {
                "postedOn": h.get("postedOn", ""),
            }
        }
        jobs.append(job)
    if save_local:
        save_jobs(jobs, source, verbose=verbose)
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
    jobs = []
    for site in workday_sites:
        hits = _fetch_hits(
            timeout_seconds,
            source              =site["source"],
            endpoint            =site["endpoint"],
            referer             =site["referer"],
            applied_facets      =site["applied_facets"],
            save_local          =save_local,
            verbose             =verbose
            )
        jobs.extend(_parse_jobs_from_hits(
            hits,
            source          =site["source"],
            job_url_prefix  =site["job_url_prefix"],
            save_local      =save_local,
            verbose         =verbose
            ))
    return jobs

def parse_jobs_cached_hits(
    *,
    save_local  :bool = True,
    verbose     :bool = False
) -> list[Job]:
    jobs = []
    for site in workday_sites:
        hits = load_objects(source=site["source"], dir=HITS_SAVE_DIR, verbose=verbose)
        jobs.extend(_parse_jobs_from_hits(
            hits,
            source          =site["source"],
            job_url_prefix  =site["job_url_prefix"],
            save_local      =save_local,
            verbose         =verbose
            ))
    return jobs

def load_cached_jobs(
    *,
    verbose :bool = False
) -> list[Job]:
    jobs = []
    for site in workday_sites:
        jobs.extend(load_objects(source=site["source"], dir=JOBS_SAVE_DIR, verbose=verbose))

if __name__ == "__main__":
    for job in parse_jobs_fetch_hits(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")

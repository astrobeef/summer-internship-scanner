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
            "Referer"           :"https://abbott.wd5.myworkdayjobs.com/abbottcareers?Location_Country=bc33aa3152ec42d4995f4791a106ed09&Location_Country=a30a87ed25634629aa6c3958aa2b91ea&workerSubType=d0663057a84410077d944a83d8896dd3",
            "appliedFacets"    :{
                "Location_Country"   :["bc33aa3152ec42d4995f4791a106ed09",
                                       "a30a87ed25634629aa6c3958aa2b91ea"],
                "workerSubType"     :["d0663057a84410077d944a83d8896dd3"]
            },
            "job_url_prefix"    :"https://abbott.wd5.myworkdayjobs.com/en-US/abbottcareers"
        },
        {
            "source"            :"activision",
            "endpoint"          :"https://activision.wd1.myworkdayjobs.com/wday/cxs/activision/External/jobs",
            "Referer"           :"https://activision.wd1.myworkdayjobs.com/External",
            "appliedFacets"    :{
                "locationCountry"   :["bc33aa3152ec42d4995f4791a106ed09"],
                "jobFamilyGroup"    :["d5b22c2cbd48013cad00235c009aaa19",
                                      "d5b22c2cbd480127a6ee0a5c009a9e19"]
            },
            "job_url_prefix"    :"https://activision.wd1.myworkdayjobs.com/en-US/External"
        },
        {
            "source"            :"intel",
            "endpoint"          :"https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs",
            "Referer"           :"https://intel.wd1.myworkdayjobs.com/External?workerSubType=dc8bf79476611087dfde99931439ae75",
            "appliedFacets"    :{
                "workerSubType"   :["dc8bf79476611087dfde99931439ae75"],
            },
            "job_url_prefix"    :"https://intel.wd1.myworkdayjobs.com/en-US/External"
        },
        # {
        #     "source"            :"nvidia",
        #     "endpoint"          :"https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs",
        #     "Referer"           :"https://nvidia.wd5.myworkdayjobs.com/External",
        #     "appliedFacets"    :{
        #         "locationHierarchy1":["2fcb99c455831013ea529c3b93ba3236",
        #                       "2fcb99c455831013ea52fb338f2932d8"],
        #         "workerSubType"     :["0c40f6bd1d8f10adf6dae42e46d44a17"]
        #     },
        #     "job_url_prefix"    :"https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"
        # },
        {
            "source"            :"sonyglobal",
            "endpoint"          :"https://sonyglobal.wd1.myworkdayjobs.com/wday/cxs/sonyglobal/SonyGlobalCareers/jobs",
            "Referer"           :"https://sonyglobal.wd1.myworkdayjobs.com/SonyGlobalCareers?workerSubType=7306bd11847f108d51604b3183153b95&locationCountry=bc33aa3152ec42d4995f4791a106ed09",
            "appliedFacets"    :{
                "locationCountry":["bc33aa3152ec42d4995f4791a106ed09"],
                "workerSubType"     :["7306bd11847f108d51604b3183153b95"]
            },
            "job_url_prefix"    :"https://sonyglobal.wd1.myworkdayjobs.com/en-US/SonyGlobalCareers"
        },
        {
            "source"            :"salesforce",
            "endpoint"          :"https://salesforce.wd12.myworkdayjobs.com/wday/cxs/salesforce/External_Career_Site/jobs",
            "Referer"           :"https://salesforce.wd12.myworkdayjobs.com/External_Career_Site?workerSubType=3a910852b2c31010f48d2cefdccd0000&CF_-_REC_-_LRV_-_Job_Posting_Anchor_-_Country_from_Job_Posting_Location_Extended=bc33aa3152ec42d4995f4791a106ed09",
            "appliedFacets"    :{
                "CF_-_REC_-_LRV_-_Job_Posting_Anchor_-_Country_from_Job_Posting_Location_Extended":["bc33aa3152ec42d4995f4791a106ed09"],
                "workerSubType"     :["3a910852b2c31010f48d2cefdccd0000"]
            },
            "job_url_prefix"    :"https://salesforce.wd12.myworkdayjobs.com/en-US/External_Career_Site"
        },
        {
            "source"            :"adobe",
            "endpoint"          :"https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/external_experienced/jobs",
            "Referer"           :"https://adobe.wd5.myworkdayjobs.com/external_experienced?workerSubType=3ba4ecdf4893100b2f8d08d56d8d6c8e&locationCountry=bc33aa3152ec42d4995f4791a106ed09",
            "appliedFacets"    :{
                "locationCountry":["bc33aa3152ec42d4995f4791a106ed09"],
                "workerSubType"     :["3ba4ecdf4893100b2f8d08d56d8d6c8e"]
            },
            "job_url_prefix"    :"https://adobe.wd5.myworkdayjobs.com/en-US/external_experienced"
        },
        {
            "source"            :"snap",
            "endpoint"          :"https://wd1.myworkdaysite.com/wday/cxs/snapchat/snap/jobs",
            "Referer"           :"https://wd1.myworkdaysite.com/en-US/recruiting/snapchat/snap?q=intern&jobFamily=8d73f0a7971d102b9db74b4c3651e667&jobFamily=8d73f0a7971d102b9d459841e16ae3a5",
            "appliedFacets"    :{
                "jobFamily	":["8d73f0a7971d102b9db74b4c3651e667",
                              "8d73f0a7971d102b9d459841e16ae3a5"],
            },
            "searchText"        : "intern",
            "job_url_prefix"    :"https://wd1.myworkdaysite.com/en-US/recruiting/snapchat/snap"
        },
        {
            "source"            :"cadence",
            "endpoint"          :"https://cadence.wd1.myworkdayjobs.com/wday/cxs/cadence/External_Careers/jobs",
            "Referer"           :"https://cadence.wd1.myworkdayjobs.com/en-US/External_Careers/jobs?workerSubType=631f97c41c2749729ac5abe683f281d0&Location_Country=bc33aa3152ec42d4995f4791a106ed09",
            "appliedFacets"    :{
                "Location_Country":["bc33aa3152ec42d4995f4791a106ed09"],
                "workerSubType":["631f97c41c2749729ac5abe683f281d0"]
            },
            "job_url_prefix"    :"https://cadence.wd1.myworkdayjobs.com/en-US/External_Careers"
        },
        {
            "source"            :"analogdevices",
            "endpoint"          :"https://analogdevices.wd1.myworkdayjobs.com/wday/cxs/analogdevices/External/jobs",
            "Referer"           :"https://analogdevices.wd1.myworkdayjobs.com/External",
            "appliedFacets"    :{
                "locationCountry":["bc33aa3152ec42d4995f4791a106ed09"],
                "workerSubType":["633b03df4f5d1000ec10ab4627a80000"]
            },
            "job_url_prefix"    :"https://analogdevices.wd1.myworkdayjobs.com/en-US/External"
        },
        {
            "source"            :"nxp",
            "endpoint"          :"https://nxp.wd3.myworkdayjobs.com/wday/cxs/nxp/careers/jobs",
            "Referer"           :"https://nxp.wd3.myworkdayjobs.com/careers?workerSubType=98d67abaaa8a100fa367c93a27fc8ec5&Location_Country=bc33aa3152ec42d4995f4791a106ed09",
            "appliedFacets"    :{
                "Location_Country":["bc33aa3152ec42d4995f4791a106ed09"],
                "workerSubType":["98d67abaaa8a100fa367c93a27fc8ec5"]
            },
            "job_url_prefix"    :"https://nxp.wd3.myworkdayjobs.com/en-US/careers"
        },
        {
            "source"            :"microchip",
            "endpoint"          :"https://wd5.myworkdaysite.com/wday/cxs/microchiphr/External/jobs",
            "Referer"           :"https://wd5.myworkdaysite.com/en-US/recruiting/microchiphr/External?zz_LRV_Career_Level_Requisition_Extended=57f4a35d19da0166ec5d6a6365019c99&locationCountry=bc33aa3152ec42d4995f4791a106ed09",
            "appliedFacets"    :{
                "locationCountry":["bc33aa3152ec42d4995f4791a106ed09"],
                "zz_LRV_Career_Level_Requisition_Extended":["57f4a35d19da0166ec5d6a6365019c99"]
            },
            "job_url_prefix"    :"https://wd5.myworkdaysite.com/en-US/recruiting/microchiphr/External"
        },
        # {
        #     "source"            :"northrop",
        #     "endpoint"          :"https://ngc.wd1.myworkdayjobs.com/wday/cxs/ngc/Northrop_Grumman_External_Site/jobs",
        #     "Referer"           :"https://ngc.wd1.myworkdayjobs.com/Northrop_Grumman_External_Site?workerSubType=a111b0a898f10129e4db58f2e700d97a",
        #     "appliedFacets"    :{
        #         "workerSubType":["a111b0a898f10129e4db58f2e700d97a"]
        #     },
        #     "job_url_prefix"    :"https://ngc.wd1.myworkdayjobs.com/en-US/Northrop_Grumman_External_Site"
        # },
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
    Referer         :str,
    applied_facets  :dict,
    save_local      :bool,
    verbose         :bool,
) -> list:
    headers = HEADERS.copy()
    headers["Referer"] = Referer
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
    jobs = []
    for site in workday_sites:
        hits = _fetch_hits(
            timeout_seconds,
            source              =site["source"],
            endpoint            =site["endpoint"],
            Referer             =site["Referer"],
            applied_facets      =site["appliedFacets"],
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

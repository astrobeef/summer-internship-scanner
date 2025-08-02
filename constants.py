import os
from typing import TypedDict

TIMEOUT = 10#seconds
HITS_SAVE_DIR = "./data/hits"
JOBS_SAVE_DIR = "./data/jobs"

class Job(TypedDict):
    source          :str
    id              :str
    title           :str
    url             :str
    location        :str
    contract_type   :str
    unique_meta     :dict

class WorkdaySite(TypedDict):
    source          :str
    endpoint        :str
    Referer         :str
    appliedFacets  :dict
    job_url_prefix  :str
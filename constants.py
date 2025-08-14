import re
from typing import TypedDict

TIMEOUT = 20#seconds
HITS_SAVE_DIR = "./data/hits"
JOBS_SAVE_DIR = "./data/jobs"
DETAILED_JOBS_SAVE_DIR = "./data/jobs_detailed"

class Job(TypedDict):
    source          :str
    id              :str
    title           :str
    url             :str
    location        :str
    contract_type   :str
    unique_meta     :dict
    description     :str = "Not Implemented"

class WorkdaySite(TypedDict):
    source          :str
    endpoint        :str
    Referer         :str
    appliedFacets   :dict
    job_url_prefix  :str

# OPEN AI CONSTANTS
GPT_MODELS      = ["gpt-4o", "gpt-4.1", "gpt-4.1-mini", "gpt-4o-mini", "gpt-4.1-nano"]      # Ordered by cost (high to low)
GPT_BEST        = GPT_MODELS[1]#gpt-4.1
GPT_CHEAPEST    = GPT_MODELS[4]#gpt-4.1-nano
ASK_TOKEN_BUDGET= 100_000           # Standard small default is 4096 - 500, but this project needs a larger context
CHAT_TEMPERATURE= 0

class Eval(TypedDict):
    url     :str
    title   :str
    reason  :str

class Response(TypedDict):
    close_match     :list[Eval]
    near_match      :list[Eval]
    non_match       :list[Eval]
import re
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

def clean_filename(name: str) -> str:
    name = name.strip()
    name = re.sub(r'[\\/*?:"<>|]', '_', name)   # Replace forbidden characters
    name = re.sub(r'\s+', '-', name)            # Replace spaces (and any whitespace) with hyphens
    return name[:255]
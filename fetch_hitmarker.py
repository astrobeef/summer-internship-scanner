"""
IBM uses a JSON POST response to return all of its job data, meaning we can call this POST directly instead of parsing rendered HTML.
"""
# first-party
from __future__ import annotations
import requests, json, glob
# local
from constants import (
    TIMEOUT,
    HITS_SAVE_DIR,
    JOBS_SAVE_DIR,
    build_path)

ENDPOINT = "https://search.hitmarker.com/multi_search?q="

# Headers copied from HAR
HEADERS = {
    "User-Agent":        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Accept":            "application/json, text/plain, */*",
    "Content-Type":      "application/json",
    "Origin":            "https://hitmarker.net",
    "Referer":           "https://hitmarker.net/",
    "X-TYPESENSE-API-KEY": (
        "QjFTckNNRFBWR2JOWjBvMUdlWmpEMUlYUEJJNnNnTFV6dEcxQVhvb28rVT1YNHFieyJleGNsdWRlX2ZpZWxkcyI6InRvdGFsQ291bnQsYWx0U2VhcmNoVGVybXMsYXV0aG9yIiwibGltaXRfbXVsdGlfc2VhcmNoZXMiOjEwMDAwfQ=="  # key from HAR; replace if it changes
    ),
    "DNT": "1",
    "Sec-GPC": "1",
}

PAYLOAD = {
    "searches": [
        {
            "collection": "hitmarker_jobs_open",
            "query_by": (
                "title,jobLocation.title,jobLocation.parents.title,"
                "jobCompany.title,jobTags.title,jobDescription"
            ),
            "filter_by": (
                "jobLocation.id:[233,39] || jobLocation.parents.id:[233,39] "
                "&& jobContract.id:[internship]"
            ),
            "page": 1,
            "per_page": 40,
            "exhaustive_search": True,
            "filter_curated_hits": True,
        }
    ]
}

#######
# I/O #
#######

def _build_hitmarker_path(
        job_id,
        *,
        dir         :str,
        make_dir    :bool
) -> str:
    return build_path("hitmarker", job_id, dir=dir, make_dir=make_dir)

def _save_hits(
        hits          :list,
        *,
        verbose       :bool = False
) -> None:
    for h in hits:
        job_id = h.get("document", {}).get("id", "None")
        if job_id == "None":
            raise ValueError('Could not find h["_id"]')
        path = _build_hitmarker_path(job_id, dir=HITS_SAVE_DIR, make_dir=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(h, f, indent=2, ensure_ascii=False)

def _save_jobs(
        jobs          :list,
        *,
        verbose       :bool = False
) -> None:
    for j in jobs:
        job_id = j["id"]
        path = _build_hitmarker_path(job_id, dir=JOBS_SAVE_DIR, make_dir=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(j, f, indent=2, ensure_ascii=False)

def _load(
        dir         :str,
        verbose     :bool = False
) -> list:
    elements = []
    pattern = _build_hitmarker_path("*", dir=dir, make_dir=False)
    for path in glob.glob(pattern):
      with open(path, encoding="utf-8") as f:
          e = json.load(f)
      elements.append(e)
    verbose and print(f"Loaded {len(elements)} elements from pattern: \"{pattern}\"")
    return elements

###############
# FETCH/PARSE #
###############

def _get_location(doc) -> str | None:
    loc_list = doc.get("jobLocation", [])
    if loc_list:
        city   = loc_list[0]["title"]
        parent = next((p["title"] for p in loc_list[0]["parents"] if p["type"] == "country"), "")
        return f"{city}, {parent}" if parent else city
    else:
        return None

def _get_contract_type(doc) -> str | None:
    job_contract = doc.get("jobContract", [])
    if job_contract:
        return job_contract[0]["title"]
    else:
        return None
    
# NOTE: All the keys referenced were derived from the .har file
def _fetch_hits(
        timeout_seconds :int,
        *,
        save_local      :bool,
        verbose         :bool
) -> list:
    try:
        response = requests.post(
            ENDPOINT,
            headers=HEADERS,
            json=PAYLOAD,
            timeout=timeout_seconds
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("Hitmarker request timed out")
    except requests.HTTPError as e:
        if response.status_code in (401, 403) and "x-typesense-api-key" in response.text.lower():
            raise RuntimeError(
                "Hitmarker returned 401/403 Forbidden: the Typesense API key is missing, invalid, or has rotated. "
                "Capture a fresh X-TYPESENSE-API-KEY by loading the jobs page in a browser, "
                "exporting a new HAR file, and copying the key from the request headers."
            ) from e
        raise RuntimeError(f"Hitmarker request failed: {response.status_code} {response.text}") from e
    data = response.json()
    hits = data["results"][0]["hits"]
    verbose and print(f"Fetched {len(hits)} hits from \"{ENDPOINT}\"")
    if save_local:
      _save_hits(hits, verbose=verbose)
    return hits

# NOTE: All the keys referenced were derived from the .har file
def _parse_jobs_from_hits(
        hits        :list,
        *,
        save_local  :bool,
        verbose     :bool
) -> list:
    jobs = []
    for h in hits:
        doc = h["document"]
        job = {
                "source": "Hitmarker",
                "id": doc["id"],
                "title": doc["title"],
                "url":  "https://hitmarker.net" + doc["url"]
                         if doc["url"].startswith("/") else doc["url"],
                "location": _get_location(doc),
                "contract_type": _get_contract_type(doc),
                "unique_meta":{
                    "external_url": doc.get("jobApplicationUrl", "None"),
                }
            }
        jobs.append(job)
    if save_local:
        _save_jobs(jobs, verbose=verbose)
    return jobs

###########
# EXECUTE #
###########


def parse_jobs_fetch_hits(
        timeout_seconds :int  = TIMEOUT,
        *,
        save_local      :bool = True,
        verbose         :bool = False
) -> list:
    hits = _fetch_hits(timeout_seconds, save_local=save_local, verbose=verbose)
    return _parse_jobs_from_hits(hits, save_local=save_local, verbose=verbose)

def parse_jobs_cached_hits(
        *,
        save_local  :bool = True,
        verbose     :bool = False
) -> list:
    hits = _load(HITS_SAVE_DIR, verbose=verbose)
    return _parse_jobs_from_hits(hits, save_local=save_local, verbose=verbose)

def load_cached_jobs(
        *,
        verbose :bool = False
) -> list:
    return _load(JOBS_SAVE_DIR, verbose=verbose)

if __name__ == "__main__":
    for job in parse_jobs_fetch_hits():
        print(f"{job['title']} | {job['location']} | {job['url']}")
"""
IBM uses a JSON GET endpoint to return all of its job data, meaning we can call this GET directly instead of parsing rendered HTML.
"""
# first-party
import json, requests, glob
# local
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

SOURCE = "ibm"

ENDPOINT = "https://www-api.ibm.com/search/api/v2"

# Headers copied from HAR
HEADERS = {
    "User-Agent":        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Accept":            "application/json, text/plain, */*",
    "Accept-Language":   "en-US,en;q=0.5",
    "Accept-Encoding":   "gzip, deflate, br, zstd",
    "Content-Type":      "application/json",
    "Origin":            "https://www.ibm.com",
    "Referer":           "https://www.ibm.com/",
    "Sec-Fetch-Dest":    "empty",
    "Sec-Fetch-Mode":    "cors",
    "Sec-Fetch-Site":    "same-site",
    "DNT":               "1",
    "Sec-GPC":           "1",
    "Pragma":            "no-cache",
    "Cache-Control":     "no-cache",
}

# Payload copied from HAR
PAYLOAD = json.loads(
    """
    {
      "appId": "careers",
      "scopes": ["careers2"],
      "query": { "bool": { "must": [] } },
      "post_filter": {
        "bool": {
          "must": [
            { "term": { "field_keyword_18": "Internship" } },
            { "term": { "field_keyword_05": "United States" } }
          ]
        }
      },
      "aggs": {
        "field_keyword_172": {
          "filter": {
            "bool": {
              "must": [
                { "term": { "field_keyword_18": "Internship" } },
                { "term": { "field_keyword_05": "United States" } }
              ]
            }
          },
          "aggs": {
            "field_keyword_17": { "terms": { "field": "field_keyword_17", "size": 6 } },
            "field_keyword_17_count": { "cardinality": { "field": "field_keyword_17" } }
          }
        },
        "field_keyword_083": {
          "filter": {
            "bool": {
              "must": [
                { "term": { "field_keyword_18": "Internship" } },
                { "term": { "field_keyword_05": "United States" } }
              ]
            }
          },
          "aggs": {
            "field_keyword_08": { "terms": { "field": "field_keyword_08", "size": 6 } },
            "field_keyword_08_count": { "cardinality": { "field": "field_keyword_08" } }
          }
        },
        "field_keyword_184": {
          "filter": { "term": { "field_keyword_05": "United States" } },
          "aggs": {
            "field_keyword_18": { "terms": { "field": "field_keyword_18", "size": 6 } },
            "field_keyword_18_count": { "cardinality": { "field": "field_keyword_18" } }
          }
        },
        "field_keyword_055": {
          "filter": { "term": { "field_keyword_18": "Internship" } },
          "aggs": {
            "field_keyword_05": { "terms": { "field": "field_keyword_05", "size": 1000 } },
            "field_keyword_05_count": { "cardinality": { "field": "field_keyword_05" } }
          }
        }
      },
      "size": 30,
      "sort": [
        { "_score": "desc" },
        { "pageviews": "desc" }
      ],
      "lang": "zz",
      "localeSelector": {},
      "sm": { "query": "", "lang": "zz" },
      "_source": [
        "_id",
        "title",
        "url",
        "description",
        "language",
        "entitled",
        "field_keyword_17",
        "field_keyword_08",
        "field_keyword_18",
        "field_keyword_19"
      ]
    }
    """
)

#######
# I/O #
#######

def _parse_id(hit) -> str:
    return hit["_id"]

###############
# FETCH/PARSE #
###############

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
            timeout=timeout_seconds,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("IBM request timed out")
    except requests.HTTPError as e:
        raise RuntimeError(f"IBM request failed: {response.status_code} {response.text}") from e
    data = response.json()
    hits = data.get("hits", {}).get("hits", [])
    verbose and print(f"Fetched {len(hits)} hits from \"{ENDPOINT}\"")
    if save_local:
      save_hits(hits, source=SOURCE, id_fn=_parse_id, verbose=verbose)
    return hits

# NOTE: All the keys referenced were derived from the .har file
def _parse_jobs_from_hits(
        hits        :list,
        *,
        save_local  :bool,
        verbose     :bool
) -> list[Job]:
    jobs = []
    for h in hits:
        doc = h["_source"]
        job: Job = {
            "source"        :SOURCE,
            "id"            :_parse_id(h),
            "title"         : doc["title"],
            "url"           : doc["url"],
            "location"      : doc.get("field_keyword_19", ""),
            "contract_type" : doc.get("field_keyword_18", ""),
            "unique_meta"   : {
                "area_of_work": doc.get("field_keyword_08", ""),
                "work_env": doc.get("field_keyword_17", ""),
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
        timeout_seconds :int  = TIMEOUT,
        *,
        save_local      :bool = True,
        verbose         :bool = False
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
    for job in parse_jobs_fetch_hits():
        print(f"{job['title']} | {job['location']} | {job['url']}")
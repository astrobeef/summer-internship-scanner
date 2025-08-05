import json
import os
from fetch import fetch_all_jobs
from append_full_descriptions import augment_jobs_with_descriptions
from openai_filter import filter_jobs
from openai_parse_response import (parse_response)
from dispatch_email import dispatch_email
from constants import (DETAILED_JOBS_SAVE_DIR, Response, GPT_MODELS)
from openai_create_client import CACHE_QUERY_DIR
from util_fetch_io import (is_saved, load_all_jobs)

def _merge_responses(
        new_response    :Response   =None,
        *,
        dir             :str        =CACHE_QUERY_DIR
):
    responses = [new_response] if new_response else []
    if not os.path.isdir(dir):
        return new_response
    for fname in os.listdir(dir):
        if not fname.endswith(".json"):
            continue
        try:
            with open(os.path.join(dir, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
                response_str = data["response"]
                response = parse_response(response_str)
                responses.append(response)
        except Exception as e:
            print(f"Warning: Could not parse {fname}: {e}")
    merged = {
        "close_match"   : [],
        "near_match"    : [],
        "non_match"     : [],
    }
    seen = {
        "close_match"   : set(),
        "near_match"    : set(),
        "non_match"     : set(),
    }
    for r in responses:
        for key in merged:
            for entry in r.get(key, []):
                url = entry.get("url")
                if url and url not in seen[key]:
                    merged[key].append(entry)
                    seen[key].add(url)
    return merged

def _load_all_filtered_urls(
        responses_dir   :str =CACHE_QUERY_DIR
):
    urls = set()
    if not os.path.isdir(responses_dir):
        return urls
    for fname in os.listdir(responses_dir):
        if not fname.endswith(".json"):
            continue
        try:
            with open(os.path.join(responses_dir, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
                response_str = data["response"]
                response = parse_response(response_str)
                for key in ("close_match", "near_match", "non_match"):
                    for eval in response[key]:
                        url = eval["url"]
                        if url and not url in urls:
                            urls.add(url)
        except Exception as e:
            print(f"Warning: Could not parse {fname}: {e}")
    return urls

def _get_all_job_descriptions(jobs, verbose:bool):
    jobs_with_desc      = load_all_jobs(dir = DETAILED_JOBS_SAVE_DIR)
    jobs_missing_desc   = [job for job in jobs if not is_saved(job, dir=DETAILED_JOBS_SAVE_DIR)]
    new_jobs_described  = augment_jobs_with_descriptions(jobs_missing_desc, verbose=verbose)
    return new_jobs_described + jobs_with_desc

def fetch_all_jobs_and_dispatch(
        *,
        model       :str = GPT_MODELS[1],
        verbose     :bool = False
):
    all_jobs = fetch_all_jobs(verbose=verbose)
    all_jobs = _get_all_job_descriptions(all_jobs, verbose=verbose)
    already_filtered_urls = _load_all_filtered_urls()
    jobs_unfiltered = [job for job in all_jobs if job["url"] not in already_filtered_urls]
    if jobs_unfiltered and len(jobs_unfiltered) > 0:
        response_str = filter_jobs(jobs_unfiltered, model=model, verbose=verbose)
        response: Response = parse_response(response_str)
        merged_responses = _merge_responses(response)
    else:
        merged_responses = _merge_responses()
    dispatch_email(merged_responses)
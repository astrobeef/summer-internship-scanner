from fetch import fetch_all_jobs
from append_full_descriptions import augment_jobs_with_descriptions
from openai_filter import filter_jobs
from openai_parse_response import parse_response
from dispatch_email import dispatch_email
from constants import (Response, GPT_MODELS)

def fetch_all_jobs_and_dispatch(
        *,
        model       :str = GPT_MODELS[1],
        verbose     :bool = False
):
    all_jobs = fetch_all_jobs(verbose=verbose)
    all_jobs = augment_jobs_with_descriptions(all_jobs, verbose=verbose)
    response_str = filter_jobs(all_jobs, model=model, verbose=verbose)
    response: Response = parse_response(response_str)
    dispatch_email(response)
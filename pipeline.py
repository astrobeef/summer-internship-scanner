from fetch import fetch_all_jobs
from openai_filter import filter_jobs
from openai_parse_response import parse_response
from dispatch_email import dispatch_email
from constants import (Response)

def fetch_all_jobs_and_dispatch(
        *,
        verbose     :bool = False
):
    all_jobs = fetch_all_jobs(verbose=verbose)
    response_str = filter_jobs(all_jobs, verbose=verbose)
    response: Response = parse_response(response_str)
    dispatch_email(response)
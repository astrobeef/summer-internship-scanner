# aggregate_jobs.py

from fetch_api_amazon import parse_jobs_fetch_hits as fetch_amazon
from fetch_api_amd import parse_jobs_fetch_hits as fetch_amd
from fetch_api_epicgames import parse_jobs_fetch_hits as fetch_epic
from fetch_api_hitmarker import parse_jobs_fetch_hits as fetch_hitmarker
from fetch_api_honeywell import parse_jobs_fetch_hits as fetch_honeywell
from fetch_api_ibm import parse_jobs_fetch_hits as fetch_ibm
from fetch_api_insomniac import parse_jobs_fetch_hits as fetch_insomniac
from fetch_api_microsoft import parse_jobs_fetch_hits as fetch_microsoft
from fetch_api_sony import parse_jobs_fetch_hits as fetch_sony
from fetch_api_workday import parse_jobs_fetch_hits as fetch_workday
from fetch_html_ea import fetch_ea_jobs
from fetch_html_riot import fetch_riot_jobs
from fetch_html_zenimax import fetch_zenimax_jobs
import fetch_obsidian
from constants import (TIMEOUT, Job)

def fetch_all_jobs(
        timeout :str    = TIMEOUT,
        *,
        verbose :bool   = False
) -> list[Job]:
    all_jobs: list[Job] = []
    for fetcher in [
        fetch_amazon,
        fetch_amd,
        fetch_epic,
        fetch_hitmarker,
        fetch_honeywell,
        fetch_ibm,
        fetch_insomniac,
        fetch_microsoft,
        fetch_sony,
        fetch_workday,
        fetch_ea_jobs,
        fetch_riot_jobs,
        fetch_zenimax_jobs,
    ]:
        jobs = fetcher(timeout_seconds=timeout, verbose=verbose)
        all_jobs.extend(jobs)
    # Obsidian is presence-only (no jobs if not implemented)
    try:
        fetch_obsidian.check_for_internships()
    except NotImplementedError as e:
        raise
    except Exception as e:
        print(f"Obsidian fetch failed: {e}")
    return all_jobs

if __name__ == "__main__":
    jobs = fetch_all_jobs(verbose=True)
    print(f"Total jobs fetched: {len(jobs)}")
    for job in jobs:
        print(f"{job['source']} | {job['title']} | {job['location']} | {job['url']}")

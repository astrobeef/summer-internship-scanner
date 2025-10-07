import logging
from pathlib import Path
from constants import JOBS_SAVE_DIR
from util_fetch_io import load_all_jobs
from ignore_blacklist import extract_blacklist_urls

# Constants
OUTPUT_MARKDOWN_FILE = Path("blacklist.md")

logging.basicConfig(level=logging.INFO, format="%(message)s")

def _append_urls_to_markdown(urls, markdown_file: Path):
    with markdown_file.open("a", encoding="utf-8") as md_file:
        for url in urls:
            md_file.write(f"- {url}\n")

## Filters Linkedin job posts by three criteria:
# 1. Must have less than 100 applicants
# 2. Must be less than one month old
# 3. Must include "Internship" preference
# Returns all which do NOT satisfy these criteria
def _collect_jobs_to_blacklist(blacklist_urls):
    all_jobs = load_all_jobs(JOBS_SAVE_DIR, blacklist_urls=blacklist_urls)
    filtered_jobs = []
    for job in all_jobs:
        if job.get("source") != "linkedin":
            continue
        details = job.get("unique_meta", {}).get("details", [])
        preferences = job.get("unique_meta", {}).get("preferences", [])
        clicked_apply = any("Over 100 people clicked apply" in d for d in details)
        long_duration = any("month" in d.lower() for d in details if "ago" in d.lower())
        not_internship = "Internship" not in preferences
        if clicked_apply or long_duration or not_internship:
            filtered_jobs.append(job)
            logging.info(f"Blacklisting job: {job.get('title')} (ID: {job.get('id')})")
    return filtered_jobs

if __name__ == "__main__":
    blacklisted         = extract_blacklist_urls()
    jobs_to_blacklist   = _collect_jobs_to_blacklist(blacklisted)

    urls_to_blacklist = [job.get("url") for job in jobs_to_blacklist if job.get("url")]
    if urls_to_blacklist:
        _append_urls_to_markdown(urls_to_blacklist, OUTPUT_MARKDOWN_FILE)
        logging.info(f"Appended {len(urls_to_blacklist)} URLs to {OUTPUT_MARKDOWN_FILE}")
    else:
        logging.info("No new jobs to blacklist.")

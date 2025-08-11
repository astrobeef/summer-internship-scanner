"""
Scrapes internship job listings from Notion's careers page.

Parses the 'University' section:
  <section aria-labelledby="open-positions-university"> ... </section>
"""

from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from constants import (
    TIMEOUT,
    Job,
)
from util_fetch_io import save_jobs

SOURCE      = "notion"
NOTION_URL  = "https://www.notion.com/careers"

HEADERS     = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
}

SECTION_SELECTOR    = 'section[aria-labelledby="open-positions-university"]'
JOBS_UL_SELECTOR    = 'ul[class^="openPositions_jobsList"]'
JOB_LI_SELECTOR     = 'li[class^="openPositions_jobsListItem"]'
LINK_SELECTOR       = 'a[href]'
TITLE_SELECTOR      = 'div[class^="jobPosting_jobTitle"]'
LOCATION_SELECTOR   = 'div[class^="jobPosting_jobLocation"]'

###########
# PARSING #
###########

def _derive_id_from_url(url: str) -> str:
    """
    For AshbyHQ links like:
      https://jobs.ashbyhq.com/notion/39d70209-37f6-4623-949b-18fbd8889933
    Use the final path segment as the job ID.
    """
    path = urlparse(url).path.rstrip("/")
    return path.split("/")[-1] if path else url

def _safe_text(node) -> str:
    return node.get_text(strip=True) if node else ""

def _parse_jobs_from_html(
    html    :str,
    *,
    verbose :bool = False,
) -> list[Job]:
    soup = BeautifulSoup(html, "html.parser")
    section = soup.select_one(SECTION_SELECTOR)
    if not section:
        verbose and print(f"{SECTION_SELECTOR} not found; no internship section present.")
        return []
    jobs_ul = section.select_one(JOBS_UL_SELECTOR)
    if not jobs_ul:
        verbose and print(f"{JOBS_UL_SELECTOR} not found under internship section.")
        return []
    jobs: list[Job] = []
    for li in jobs_ul.select(JOB_LI_SELECTOR):
        a_tag = li.select_one(LINK_SELECTOR)
        if not a_tag:
            continue
        url = a_tag["href"]
        title = _safe_text(a_tag.select_one(TITLE_SELECTOR))
        location = _safe_text(a_tag.select_one(LOCATION_SELECTOR))
        job_id = _derive_id_from_url(url)
        contract_type = "Internship" if "intern" in title.lower() else ""
        job: Job = {
            "source": SOURCE,
            "id": job_id,
            "title": title,
            "url": url,
            "location": location,
            "contract_type": contract_type,
            "unique_meta": {},
        }
        jobs.append(job)

    verbose and print(f"Parsed {len(jobs)} Notion internship jobs from HTML.")
    return jobs

# -----------------------
# Fetch
# -----------------------

def fetch_notion_jobs(
    *,
    timeout_seconds :int    = TIMEOUT,
    save_local      :bool   = True,
    verbose         :bool   = False,
) -> list[Job]:
    """
    GET the Notion careers HTML, parse to job dicts, optionally save.
    """
    try:
        response = requests.get(NOTION_URL, headers=HEADERS, timeout=timeout_seconds)
        response.raise_for_status()
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("Notion request timed out") from exc
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Notion request failed: {response.status_code} {response.text}"
        ) from exc

    jobs = _parse_jobs_from_html(response.text, verbose=verbose)
    if save_local and jobs:
        save_jobs(jobs, verbose=verbose)
    return jobs

if __name__ == "__main__":
    for job in fetch_notion_jobs(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")

"""
Scrapes HTML job listings from EA's public careers board.
"""
from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from constants import (
    TIMEOUT,
    Job
)
from util_fetch_io import save_jobs

SOURCE      = "ea"

EA_URL      = "https://jobs.ea.com/en_US/careers/Home/?8171=%5B10618%2C10577%5D&8171_format=5683&4537=%5B8693%5D&4537_format=3020&listFilterMode=1&jobRecordsPerPage=20&"
# NOTE: Above is internship filter, below is regular jobs.
# EA_URL      = "https://jobs.ea.com/en_US/careers/Home/?8171=%5B10577%2C10618%5D&8171_format=5683&listFilterMode=1&jobRecordsPerPage=20&"

HEADERS     = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
}

############
#  PARSING #
############

def _derive_id_from_url(url: str) -> str:
    """
    EA job URLs look like:
      https://jobs.ea.com/en_US/careers/JobDetail/Development-Director-I/210016
    """
    parts = urlparse(url).path.rstrip("/").split("/")
    for part in reversed(parts):
        if part.isdigit():
            return part
    return parts[-1]

def _format_location(article: BeautifulSoup) -> str:
    # Primary and posting locations, joined if both exist
    locations = []
    loc = article.select_one(".list-item-location")
    if loc:
        locations.append(loc.get_text(strip=True))
    posting = article.select_one(".list-item-jobPostingLocation .list-item-0")
    if posting:
        locations.append(posting.get_text(strip=True))
    return " / ".join(locations)

def _parse_jobs_from_html(
        html    :str,
        *,
        verbose :bool = False
) -> list[Job]:
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one("div.results.results--listed")
    if not container:
        verbose and print("<div.results.results--listed> not found.")
        return []
    jobs: list[Job] = []
    for article in container.select("article.article--result"):
        a_tag = article.select_one("h3 a.link_result[href]")
        if not a_tag:
            raise ValueError("Could not find a_tag")
        url = a_tag["href"]
        title = a_tag.get_text(strip=True)
        job_id = _derive_id_from_url(url)
        location = _format_location(article)
        worker_type = article.select_one(".list-item-workerType")
        contract_type = worker_type.get_text(strip=True) if worker_type else ""
        department = article.select_one(".list-item-department")
        unique_meta = {
            "department": department.get_text(strip=True) if department else ""
        }
        job: Job = {
            "source"       : SOURCE,
            "id"           : job_id,
            "title"        : title,
            "url"          : url,
            "location"     : location,
            "contract_type": contract_type,
            "unique_meta"  : unique_meta,
        }
        jobs.append(job)
    verbose and print(f"Parsed {len(jobs)} EA jobs from HTML.")
    return jobs

############
#  FETCH   #
############

def fetch_ea_jobs(
    *,
    timeout_seconds :int    = TIMEOUT,
    save_local      :bool   = True,
    verbose         :bool   = False,
) -> list[Job]:
    """
    GET the EA board HTML, parse to job dicts, optionally save.
    """
    try:
        response = requests.get(EA_URL, headers=HEADERS, timeout=timeout_seconds)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("EA request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"EA request failed: {response.status_code} {response.text}"
        ) from exc
    jobs = _parse_jobs_from_html(response.text, verbose=verbose)
    if save_local and jobs:
        save_jobs(jobs, SOURCE, verbose=verbose)
    return jobs

###########
#  DEMO   #
###########

if __name__ == "__main__":
    for job in fetch_ea_jobs(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")
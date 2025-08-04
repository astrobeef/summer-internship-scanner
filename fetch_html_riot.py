"""
Scrapes HTML job listings from Riot Games' public board.
"""
# first-party
from __future__ import annotations
import requests, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
# local
from constants import (
    TIMEOUT,
    Job
    )
from util_fetch_io import save_jobs


SOURCE      = "riot"

RIOT_URL    = "https://www.riotgames.com/en/university-programs#roles"

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

def _derive_id_from_href(href: str) -> str:
    """
    Riot URLs look like:
       /en/work-with-us/5666698/ai-systems-engineer
    """
    slug = urlparse(href).path.rstrip("/").split("/")[-1]
    if slug.isdigit():
        return slug
    # fallback: last numeric token in path or slug itself
    for part in reversed(slug.split("-")):
        if part.isdigit():
            return part
    return slug

def _format_location(text: str) -> str:
    """
    Riot prints location as 'Aliso Viejo, California' etc.
    Return as-is after stripping whitespace.
    """
    return text.strip()

def _parse_jobs_from_html(
        html        :str,
        *,
        verbose     :bool = False
) -> list[Job]:
    soup = BeautifulSoup(html, "html.parser")
    ul   = soup.select_one("ul.job-list__body")
    if not ul:
        verbose and print("<ul.job-list__body> not found.")
        return []
    jobs: list[Job] = []
    for li in ul.select(":scope > li.job-row"):
        a_tag = li.select_one("a.job-row__inner[href]")
        if not a_tag:
            raise ValueError(f"Could not find <a> tag in li: {li}")
        # Title = the primary column
        title_div = a_tag.select_one(".job-row__col--primary")
        # Location = the last secondary column (may be blank)
        secondary_cols = a_tag.select(".job-row__col--secondary")
        location_div   = secondary_cols[-1] if secondary_cols else None
        href  = a_tag["href"]
        url   = urljoin(RIOT_URL, href)
        job_id = _derive_id_from_href(href)
        job: Job = {
            "source"        : SOURCE,
            "id"            : job_id,
            "title"         : title_div.get_text(strip=True),
            "url"           : url,
            "location"      : _format_location(location_div.get_text(strip=True)),
            "contract_type" : "Regular" if "job-list" in RIOT_URL else "Internship",
            "unique_meta"   : {},
        }
        jobs.append(job)
    verbose and print(f"Parsed {len(jobs)} Riot jobs from HTML.")
    return jobs

############
#  FETCH   #
############

def fetch_riot_jobs(
    *,
    timeout_seconds :int    = TIMEOUT,
    save_local      :bool   = True,
    verbose         :bool   = False,
) -> list[Job]:
    """
    GET the Riot board HTML, parse to job dicts, optionally save.
    """
    try:
        response = requests.get(RIOT_URL, headers=HEADERS, timeout=timeout_seconds)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("Riot Games request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Riot Games request failed: {response.status_code} {response.text}"
        ) from exc
    jobs = _parse_jobs_from_html(response.text, verbose=verbose)
    if save_local and jobs:
        save_jobs(jobs, verbose=verbose)
    return jobs

###########
#  DEMO   #
###########

if __name__ == "__main__":
    for job in fetch_riot_jobs(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")

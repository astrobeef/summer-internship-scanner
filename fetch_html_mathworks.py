"""
Scrapes HTML job listings from MathWorks' public search page (server-rendered).
"""
# first-party
from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

# local
from constants import (
    TIMEOUT,
    Job,
)
from util_fetch_io import (JOBS_SAVE_DIR, save_jobs, load_objects)

SOURCE = "mathworks"

BASE_URL = "https://www.mathworks.com"
MATHWORKS_SEARCH_URL = (
    f"{BASE_URL}/company/jobs/opportunities/search"
    "?job_type_id%5B%5D=1755&keywords=&location%5B%5D=US"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

TABLE_SELECTOR = "table.table.search_result_table"
ROW_SELECTOR = "tbody > tr"
TITLE_LINK_SELECTOR = ".search_result_desc .search_title a[href]"
ADDITIONAL_FIELD_SELECTOR = ".search_result_desc .additional_field"
LOCATION_SPAN_SELECTOR = ".add_font_color_green"

OPPORTUNITY_PATH_FRAGMENT = "/company/jobs/opportunities/"
MIN_TITLE_LEN = 6
ID_REGEX = re.compile(r"/opportunities/(\d+)-")

def _derive_id_from_href(href: str) -> str:
    """
    MathWorks job URLs typically look like:
      /company/jobs/opportunities/<digits>-<slug>[.html][?params]
    Extract the numeric id when present; fall back to last path token.
    """
    m = ID_REGEX.search(href)
    if m:
        return m.group(1)
    last = urlparse(href).path.rstrip("/").split("/")[-1]
    core = last.rsplit(".", 1)[0]
    for tok in reversed(core.split("-")):
        if tok.isdigit():
            return tok
    return core

def _format_location(text: str) -> str:
    """
    Normalize whitespace for locations such as 'US-MA-Natick' or 'US—Remote'.
    """
    return " ".join(text.split()).strip()

def _parse_additional_field(text: str) -> tuple[str, str, str]:
    """
    Example block:
      'US-MA-Natick | New Career Program (EDG) | Internships'
    Returns: (location, program, contract_type)
    """
    cleaned = " ".join(text.split()).strip()
    parts = [p.strip() for p in cleaned.split("|")]
    location = parts[0] if len(parts) >= 1 else ""
    program = parts[1] if len(parts) >= 2 else ""
    contract_type = parts[2] if len(parts) >= 3 else ""
    return location, program, contract_type

def _parse_jobs_from_html(
    html: str,
    *,
    verbose: bool = False,
) -> list[Job]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one(TABLE_SELECTOR)
    if not table:
        verbose and print(f"{TABLE_SELECTOR} not found.")
        return []
    jobs: list[Job] = []
    for row in table.select(ROW_SELECTOR):
        a = row.select_one(TITLE_LINK_SELECTOR)
        if not a:
            continue
        title = " ".join(a.get_text(" ", strip=True).split())
        if len(title) < MIN_TITLE_LEN:
            continue
        href = a.get("href", "")
        if OPPORTUNITY_PATH_FRAGMENT not in href:
            continue
        abs_url = urljoin(BASE_URL, href)
        job_id = _derive_id_from_href(href)
        location = program = contract_type = ""
        add = row.select_one(ADDITIONAL_FIELD_SELECTOR)
        if add:
            loc_span = add.select_one(LOCATION_SPAN_SELECTOR)
            if loc_span:
                location = _format_location(loc_span.get_text(" ", strip=True))
            loc2, prog2, type2 = _parse_additional_field(add.get_text(" ", strip=True))
            if not location:
                location = _format_location(loc2)
            program = prog2
            contract_type = type2
        job: Job = {
            "source": SOURCE,
            "id": job_id,
            "title": title,
            "url": abs_url,
            "location": location,
            "contract_type": contract_type or "Internship",  # default for this search
            "unique_meta": {"program": program} if program else {},
        }
        jobs.append(job)
    verbose and print(f"Parsed {len(jobs)} MathWorks jobs from HTML.")
    return jobs

def fetch_mathworks_jobs(
    *,
    timeout_seconds: int = TIMEOUT,
    save_local: bool = True,
    verbose: bool = False,
) -> list[Job]:
    try:
        resp = requests.get(MATHWORKS_SEARCH_URL, headers=HEADERS, timeout=timeout_seconds)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"[Mathworks - BYPASS TIMEOUT] MathWorks request timed out. Since this is a common occurance, avoiding raise error and returning previous saved jobs")
        return load_objects(source=SOURCE, dir=JOBS_SAVE_DIR, verbose=verbose)
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"MathWorks request failed: {getattr(resp, 'status_code', '?')} {getattr(resp, 'text', '')[:200]}"
        ) from exc
    jobs = _parse_jobs_from_html(resp.text, verbose=verbose)
    if save_local and jobs:
        save_jobs(jobs, verbose=verbose)
    return jobs

if __name__ == "__main__":
    for job in fetch_mathworks_jobs(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")
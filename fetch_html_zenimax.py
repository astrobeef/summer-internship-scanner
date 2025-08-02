"""
Scrapes HTML job listings from ZeniMax's public careers board.
# NOTE: Requires `cloudscraper` to bypass token/cookies requirement for Cloudfire
"""
from __future__ import annotations
import cloudscraper, json, re
from constants import (
    TIMEOUT,
    Job
)
from util_fetch_io import save_jobs

SOURCE   = "zenimax"
URL      = "https://jobs.zenimax.com/jobs"
HEADERS  = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
}

def _parse_jobs_from_html(
    html    :str,
    verbose :bool = False
) -> list[Job]:
    """
    Extract jobs from the :raw-data attribute on <job-filter>.
    """
    match = re.search(r':raw-data="({.+?})"', html)
    if not match:
        verbose and print("Could not find :raw-data attribute.")
        return []
    raw_json = match.group(1).replace('&quot;', '"')
    data = json.loads(raw_json)
    hits = data["jobs"]
    results: list[Job] = []
    for h in hits:
        location_str = h["location"].get("formatted_name", "")
        additional = h.get("additionalLocations") or []
        if additional:
            location_str += " + " + " + ".join(
                loc.get("formatted_name", "") for loc in additional
            )
        result: Job = {
            "source"       : SOURCE,
            "id"           : str(h["id"]),
            "title"        : h["title"],
            "url"          : h["link"],
            "location"     : location_str,
            "contract_type": "",  # Not present
            "unique_meta"  : {
                "department_id"  : h.get("department_id", ""),
                "department_name": h.get("department_name", ""),
            }
        }
        results.append(result)
    verbose and print(f"Parsed {len(results)} ZeniMax jobs from HTML.")
    return results

def fetch_zenimax_jobs(
    timeout_seconds :int    = TIMEOUT,
    *,
    save_local      :bool   = True,
    verbose         :bool   = False,
) -> list[Job]:
    """
    GET the ZeniMax board HTML using cloudscraper, parse to job dicts, optionally save.
    """
    scraper = cloudscraper.create_scraper(
        browser={"browser": "firefox", "platform": "windows", "mobile": False}
    )
    try:
        response = scraper.get(URL, headers=HEADERS, timeout=timeout_seconds)
        response.raise_for_status()
    except Exception as exc:
        raise RuntimeError(
            f"ZeniMax request failed: {getattr(exc, 'response', None)}"
        ) from exc
    jobs = _parse_jobs_from_html(response.text, verbose=verbose)
    if save_local and jobs:
        save_jobs(jobs, SOURCE, verbose=verbose)
    return jobs

if __name__ == "__main__":
    for job in fetch_zenimax_jobs(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")

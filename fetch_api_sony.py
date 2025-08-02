"""
Sony Interactive Entertainment jobs from the PlayStation careers API.
This endpoint is protected by Akamai and requires browser cookies to access.
# NOTE: Requires playwright to bypass token/cookie blocks
"""
from __future__ import annotations
import requests
from playwright.sync_api import sync_playwright
from constants import (
    TIMEOUT,
    HITS_SAVE_DIR,
    JOBS_SAVE_DIR,
    Job
)
from util_fetch_io import (
    save_hits,
    save_jobs,
    load_objects
)

SOURCE = "sony"

ENDPOINT = (
    "https://careers.playstation.com/api/get-jobs"
    "?radius=15"
    "&filter[country][0]=United%20States"
    "&filter[country][1]=United%20States%20of%20America"
    "&filter[country][2]=Canada"
    "&enable_kilometers=false"
)
REFERER = "https://careers.playstation.com/early-careers"
ORIGIN  = "https://careers.playstation.com"

PAYLOAD = {
    "disable_switch_search_mode": False,
    "site_available_languages": ["fr-ca", "ja", "en", "en-us"],
}

def _get_sony_headers_with_cookies(timeout_seconds: int) -> dict:
    """
    Uses Playwright to get cookies and headers required for Sony's API.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(REFERER, wait_until="networkidle", timeout=timeout_seconds * 1000)
        cookies = {c["name"]: c["value"] for c in context.cookies()}
        browser.close()
    cookie_header = "; ".join(f"{k}={v}" for k, v in cookies.items())
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
            "Gecko/20100101 Firefox/141.0"
        ),
        "Accept": "application/json, text/plain, */*",
        "Origin": ORIGIN,
        "Referer": REFERER,
        "Content-Type": "application/json",
        "Cookie": cookie_header,
    }

def _parse_id(hit) -> str:
    return hit.get("reference") or hit.get("uniqueID", "")

def _format_location(locations: list[dict]) -> str:
    if not locations:
        return ""
    loc = locations[0]
    city = loc.get("city", "")
    country = loc.get("country") or loc.get("countryAbbr", "")
    if city and country:
        return f"{city}, {country}"
    return loc.get("locationName", "")

def _fetch_hits(
    timeout_seconds :int,
    *,
    save_local      :bool,
    verbose         :bool,
) -> list:
    headers = _get_sony_headers_with_cookies(timeout_seconds)
    try:
        response = requests.post(
            ENDPOINT,
            headers=headers,
            json=PAYLOAD,
            timeout=timeout_seconds,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("Sony request timed out")
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Sony request failed: {response.status_code} {response.text}"
        ) from exc
    data = response.json()
    hits = data.get("jobs", [])
    total = data.get("totalJob", 0)
    verbose and print(f"Fetched {len(hits)} / total={total} hits from Sony")
    if save_local and hits:
        save_hits(hits, source=SOURCE, id_fn=_parse_id, verbose=verbose)
    return hits

def _parse_jobs_from_hits(
    hits        :list,
    *,
    save_local  :bool,
    verbose     :bool
) -> list[Job]:
    jobs: list[Job] = []
    for h in hits:
        job: Job = {
            "source": SOURCE,
            "id": _parse_id(h),
            "title": h.get("title", ""),
            "url": h.get("applyURL") or h.get("originalURL", ""),
            "location": _format_location(h.get("locations", [])),
            "contract_type": ", ".join(h.get("employmentType", [])),
            "unique_meta": {
                "department": h.get("departmentCode", ""),
                "brand": h.get("brandName", ""),
                "updated_iso": h.get("updatedDate", ""),
            },
        }
        jobs.append(job)
    if save_local:
        save_jobs(jobs, SOURCE, verbose=verbose)
    return jobs

def parse_jobs_fetch_hits(
    timeout_seconds :int    = TIMEOUT,
    *,
    save_local      :bool   = True,
    verbose         :bool   = False,
) -> list[Job]:
    hits = _fetch_hits(timeout_seconds, save_local=save_local, verbose=verbose)
    return _parse_jobs_from_hits(hits, save_local=save_local, verbose=verbose)

def parse_jobs_cached_hits(
    *,
    save_local  :bool = True,
    verbose     :bool = False,
) -> list[Job]:
    hits = load_objects(source=SOURCE, dir=HITS_SAVE_DIR, verbose=verbose)
    return _parse_jobs_from_hits(hits, save_local=save_local, verbose=verbose)

def load_cached_jobs(
    *,
    verbose: bool = False,
) -> list[Job]:
    return load_objects(source=SOURCE, dir=JOBS_SAVE_DIR, verbose=verbose)

if __name__ == "__main__":
    for job in parse_jobs_fetch_hits(verbose=True):
        print(f"{job['title']} | {job['location']} | {job['url']}")

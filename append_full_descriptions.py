"""
Get the full description of a job post from its URL property, then append it to the Job structure.
"""
# first-party
from __future__ import annotations
import re, requests, time, sys, os, json
# third-party
from bs4 import BeautifulSoup
from readability import Document
from playwright.sync_api import sync_playwright
# local
from constants import (TIMEOUT, DETAILED_JOBS_SAVE_DIR, Job, DESC_NOT_IMPLEMENTED)
from util_fetch_io import (save_jobs, load_all_jobs)
from fetch_api_amd import SOURCE as AMD_SOURCE
from fetch_api_insomniac import SOURCE as INSOMNIAC_SOURCE
from fetch_html_zenimax import SOURCE as ZENIMAX_SOURCE
from fetch_api_sony import SOURCE as SONY_SOURCE
from fetch_api_microsoft import SOURCE as MICROSOFT_SOURCE

_USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
               "Gecko/20100101 Firefox/141.0")

def _clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # 1) JSON-LD fallback for Workday and many other SPA pages
    for tag in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            data = json.loads(tag.string or "")
            if isinstance(data, dict) and "description" in data:
                return " ".join(data["description"].split())
        except Exception:
            continue
    # 2) Greenhouse job board: extract div.job__description.body if present
    desc = soup.select_one("div.job__description.body")
    if desc:
        text = desc.get_text(" ", strip=True)
        if len(text) > 100:
            return " ".join(text.split())
    # 3) Readability extraction
    article_html = Document(html).summary(html_partial=True)
    article_text = BeautifulSoup(article_html, "html.parser").get_text(" ", strip=True)
    if len(article_text) > 100:
        return " ".join(article_text.split())
    # 4) OpenGraph meta description if present
    og = soup.find("meta", {"property": re.compile(r"^og:description$")})
    if og and og.get("content"):
        return " ".join(og["content"].split())
    # 5) Plain soup text as last resort
    for tag in soup(["script", "style", "noscript", "svg", "img", "footer",
                     "nav", "aside", "form", "header"]):
        tag.decompose()
    return " ".join(soup.get_text(" ", strip=True).split())

def _fetch_dynamic_html(url, timeout=5000):
    """Fetch fully rendered HTML after JS with Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=timeout)
        page.wait_for_load_state("networkidle")
        html = page.content()
        browser.close()
    return html

def _get_html(
        job :Job,
        *,
        timeout :str
) -> str | None:
    session = requests.Session()
    session.headers.update({"User-Agent": _USER_AGENT})
    if job["source"] == MICROSOFT_SOURCE or job["source"] == INSOMNIAC_SOURCE or job["source"] == ZENIMAX_SOURCE or job["source"] == SONY_SOURCE:
        try:
            html = _fetch_dynamic_html(job["url"])
        except Exception as e:
            print(f"[FAIL] Playwright fetch for {job["source"]}: {e}", file=sys.stderr)
            job["description"] = "Unable to fetch via Playwright"
            return None
    else:
        if "https://careers.honeywell.com" in job["url"]:
            rsp = session.get(job["url"], timeout=timeout, verify=False)       # Honeywell gives verification error, but the site is reliable
        else:
            rsp = session.get(job["url"], timeout=timeout)
        try:
            rsp.raise_for_status()
            html = rsp.text
        except Exception as e:
            print(f"[FAIL] Playwright fetch for {job["source"]}: {e}", file=sys.stderr)
            job["description"] = "Unable to fetch via Playwright"
            return None
    try:
        text_json = json.loads(html)
        html = text_json["content"]
    except (AttributeError, json.JSONDecodeError, TypeError):
        pass
    return html

def augment_jobs_with_descriptions(
    jobs        :list[Job],
    *,
    save_local  :bool   = True,
    timeout     :int    = TIMEOUT,
    throttle    :float  = 0.5,
    verbose     :bool   = False,
):
    for job in jobs:
        if job.get("description") is not None and job["description"] is not DESC_NOT_IMPLEMENTED:
            continue
        if job["source"] == AMD_SOURCE:
            job["description"] = "Inaccessible"
            continue
        html = _get_html(job, timeout=timeout)
        if not html:
            continue
        if save_local:
            filename = f"{job['source']}_{job['id']}.html"
            safe_filename = "".join([c if c.isalnum() or c in ('-', '_', '.') else '_' for c in filename])
            path = os.path.join("./data/jobs_url_response", safe_filename)
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html)
            except Exception as e:
                print(f"Failed to save {safe_filename}: {e}", file=sys.stderr)
        clean_text = _clean_html(html)
        job["description"] = clean_text
        if verbose:
            print(f"[OK] {job['source']} {job['id']}  length={len(clean_text)}")
        time.sleep(throttle)
    if save_local:
        save_jobs(jobs, dir=DETAILED_JOBS_SAVE_DIR, verbose=True)
    return jobs

if __name__ == "__main__":
    jobs_dir = "./data/jobs"
    jobs = load_all_jobs(jobs_dir)
    print(f"Loaded {len(jobs)} jobs from {jobs_dir}")
    jobs = augment_jobs_with_descriptions(jobs, verbose=True)
    print(f"Finished with {sum('description' in j for j in jobs)} descriptions out of {len(jobs)} total")
    save_jobs(jobs, dir=DETAILED_JOBS_SAVE_DIR, verbose=True)
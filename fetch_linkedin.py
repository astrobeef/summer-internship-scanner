"""
Fetches Linkedin jobs using Playwright.
"""
from __future__ import annotations
import json
import random
import re
from playwright.sync_api import sync_playwright
from pathlib import Path
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

PROFILE_PATH = Path("./data/chromium-profiles/linkedin")
CRED_JSON = Path("./data/_keys/linkedin.json")
HEADLESS = False
URL = "https://www.linkedin.com/jobs/search/?currentJobId=4295730239&distance=25&f_E=1&f_I=109%2C4&f_WT=1%2C3&geoId=103644278&keywords=programmer"

SOURCE = "linkedin"
SLOW_MO = 250#ms

def _parse_id(hit) -> str:
    return hit["id"]

def _fetch_hits(
    timeout_seconds :int,
    *,
    save_local      :bool,
    verbose         :bool,
) -> list:
    hits = []

    PROFILE_PATH.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_PATH),
            headless=HEADLESS,
            slow_mo=SLOW_MO,
            args = [
                '--disable-dev-shm-usage',
                '--no-default-browser-check',
            ],
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(URL, wait_until="domcontentloaded")
        # Check for pop-up modal indicating not logged in
        button = page.locator('button[data-modal="base-sign-in-modal"]')
        if button.count() > 0:
            button.wait_for(state="visible")
            button.click()
            page.wait_for_timeout(500)
            # Wait
            page.wait_for_timeout(500)
            # Load cred
            cred = {}
            with open(CRED_JSON, "r", encoding="utf-8") as f:
                cred = json.load(f)
            # Fill form
            page.fill('input#base-sign-in-modal_session_key', cred["email"])
            page.fill('input#base-sign-in-modal_session_password', cred["password"])
            # Submit form
            button = page.locator('button[data-id="sign-in-form__submit-btn"]').last
            button.wait_for(state="visible")
            button.click()
        # Start scraping
        while(True):
            ## Get div containing the job list
            div = page.locator('div[class="scaffold-layout__list "]').first
            div.wait_for(state="visible")
            ## Get the list of jobs
            job_items_parent_ul = div.locator('ul').first
            job_items_parent_ul.wait_for(state="visible")
            # job_items_parent_ul.highlight()
            ## Next page button
            next_page_btn_list = div.locator('button[aria-label="View next page"]')
            if next_page_btn_list.count() == 0:
                break
            ## Get all jobs in the list
            job_items_li = job_items_parent_ul.locator('li[class*="scaffold-layout__list-item"]')
            print(f"DEBUG: total items: {job_items_li.count()}")
            ## Iterate over the jobs to select and grab data
            for n in range(job_items_li.count()):
                ## Get iterate list item
                data_job = {}
                job_parent_item = job_items_li.nth(n)
                # job_parent_item.highlight()
                page.wait_for_timeout(500)
                try:
                    ## Try to click the div which (when clicked) will show more details on the right
                    job_item_clickable_div = job_parent_item.locator('div').first.locator('div').first
                    # job_item_clickable_div.highlight()
                    page.wait_for_timeout(500)
                    job_item_clickable_div.click(timeout=500)



                    ## Get information
                    def shorten_job_url(url: str) -> str:
                        match = re.match(r"^(/jobs/view/\d+)", url)
                        return match.group(1) if match else url
                    def extract_job_id(url: str) -> str:
                        match = re.search(r"/jobs/view/(\d+)", url)
                        return match.group(1) if match else None
                    
                    job_details_wrapper = page.locator('div[class*="jobs-search__job-details--wrapper"]').first
                    # job_details_wrapper.highlight()

                    # Job title and link to post
                    page.wait_for_timeout(500)
                    job_title = job_details_wrapper.locator('h1').first
                    # job_title.highlight()
                    data_job["title"] = job_title.inner_text()
                    job_link = job_title.locator('a').first
                    data_job["link"] = f"https://www.linkedin.com{shorten_job_url(job_link.get_attribute('href'))}"
                    data_job["id"]   = extract_job_id(job_link.get_attribute('href'))

                    # Job header details just below title
                    page.wait_for_timeout(500)
                    job_header_details = job_details_wrapper.locator('div[class*="job-details-jobs-unified-top-card__primary-description-container"]').first
                    # job_header_details.highlight()
                    job_header_details_spans = job_header_details.locator('span')
                    data_job_details = []
                    for n in range(1, job_header_details_spans.count()):
                        try:
                            span = job_header_details_spans.nth(n)
                            # span.highlight()
                            text = span.text_content()
                            if text and len(text) > 3:
                                data_job_details.append(text.strip())
                        except:
                            continue
                    data_job["details"] = data_job_details

                    # Job preferences (such as on-site or intern)
                    page.wait_for_timeout(500)
                    job_pref_div = job_details_wrapper.locator('div[class*="job-details-fit-level-preferences"]').first
                    # job_pref_div.highlight()
                    job_pref_spans = job_pref_div.locator('span')
                    data_job_prefs = []
                    for n in range(1, job_pref_spans.count()):
                        try:
                            span = job_pref_spans.nth(n)
                            # span.highlight()
                            text = span.text_content()
                            if len(text) > 3 and "Matches your job".lower() not in text.lower():
                                data_job_prefs.append(text.strip())
                        except:
                            continue
                    data_job["preferences"] = data_job_prefs

                    # Hirers (if any)
                    page.wait_for_timeout(500)
                    job_hirer_cards = job_details_wrapper.locator('div[class*="hirer-card__hirer-information"]')
                    data_job_hirers = []
                    for n in range(job_hirer_cards.count()):
                        try:
                            data_job_hirer = {}
                            card = job_hirer_cards.nth(n)
                            # card.highlight()
                            hirer_link = card.locator('a').last
                            # hirer_link.highlight()
                            data_job_hirer["link"] = hirer_link.get_attribute('href')
                            data_job_hirer["name"] = hirer_link.text_content().strip()
                            linked_area = card.locator('div[class*="linked-area"]').first
                            # linked_area.highlight()
                            data_job_hirer["desc"] = linked_area.locator('div[class*="text-body-small"]').first.text_content().strip()
                            data_job_hirer["role"] = linked_area.locator('div').last.text_content().strip()
                            data_job_hirers.append(data_job_hirer)
                        except:
                            continue
                    data_job["hirers"] = data_job_hirers

                    # Get job 'about' article
                    page.wait_for_timeout(500)
                    about_article = job_details_wrapper.locator('article[class*="jobs-description__container"]').first
                    about_article_paras = about_article.locator('p, li')
                    about_text = ""
                    for n in range(1, about_article_paras.count()):
                        line_text = about_article_paras.nth(n).text_content().strip()
                        if len(line_text) > 0:
                            about_text += "\n"
                            about_text += line_text
                    data_job["about"] = about_text

                    # Get company details (if they exist)
                    page.wait_for_timeout(500)
                    data_job_company = {}
                    try:
                        about_company_sect = job_details_wrapper.locator('section[data-view-name="job-details-about-company-module"]').first
                        company_name_a = about_company_sect.locator('a[data-view-name="job-details-about-company-name-link"]').first
                        data_job_company["name"] = company_name_a.text_content().strip()
                        data_job_company["link"] = f"https://www.linkedin.com{company_name_a.get_attribute('href')}"
                    except:
                        pass
                    data_job["company"] = data_job_company

                    ## add job
                    hits.append(data_job)
                    ## Hover ancestor div and scroll down (scrolls down the list of jobs)
                    div.hover()
                    li_bbox = job_parent_item.bounding_box(timeout=500)
                    page.mouse.wheel(0,li_bbox["height"] if li_bbox else 100)
                except:
                        continue
            next_page_btn_list.scroll_into_view_if_needed()
            # next_page_btn_list.highlight()
            next_page_btn_list.first.click()
            pass
    
    verbose and print(f"Fetched {len(hits)} jobs from Linkedin")
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
            "source"        : SOURCE,
            "id"            : _parse_id(h),
            "title"         : h["title"],
            "url"           : h["link"],
            "location"      : "",
            "contract_type" : "",
            "unique_meta": {
                "details": h["details"],
                "preferences": h["preferences"],
                "hirers": h["hirers"],
                "description": h["about"],
                "company": h.get("company", [])
            }
        }
        jobs.append(job)
    if save_local:
        save_jobs(jobs, verbose=verbose)
    return jobs

##############
# PUBLIC API #
##############

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
    verbose     :bool = False
) -> list[Job]:
    hits = load_objects(source=SOURCE, dir=HITS_SAVE_DIR, verbose=verbose)
    return _parse_jobs_from_hits(hits, save_local=save_local, verbose=verbose)

def load_cached_jobs(
    *,
    verbose: bool = False
) -> list[Job]:
    return load_objects(source=SOURCE, dir=JOBS_SAVE_DIR, verbose=verbose)

########
# TEST #
########

if __name__ == "__main__":
    parse_jobs_cached_hits(save_local=True, verbose=True)
from pathlib import Path
import re
from constants import (Job)
from util_fetch_io import (JOBS_SAVE_DIR, load_all_jobs)

BLACKLIST   = Path("./blacklist.md")
URL_PATTERN = re.compile(r"https://[^\s\)\]]+")

def _extract_urls_from_file(
        blacklist   :Path = BLACKLIST
) -> list[str]:
    text_content = blacklist.read_text(encoding="utf-8")
    return URL_PATTERN.findall(text_content)

def ignore_blacklisted_jobs(
        jobs    :list[Job],
        *,
        verbose :bool
) -> list[Job]:
    return_jobs = []
    blacklisted_urls = _extract_urls_from_file()
    for j in jobs:
        if j["url"] not in blacklisted_urls:
            return_jobs.append(j)
        elif verbose:
            print(f"Removing blacklisted job \"{j["title"]}\" from jobs list")
    return return_jobs

all_jobs = load_all_jobs(JOBS_SAVE_DIR)
culled_jobs = ignore_blacklisted_jobs(all_jobs, verbose=True)
pass
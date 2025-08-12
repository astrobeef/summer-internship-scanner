from pathlib import Path
import re

BLACKLIST   = Path("./blacklist.md")
URL_PATTERN = re.compile(r"https://[^\s\)\]]+")

def extract_blacklist_urls(
        blacklist   :Path = BLACKLIST
) -> list[str]:
    text_content = blacklist.read_text(encoding="utf-8")
    return URL_PATTERN.findall(text_content)
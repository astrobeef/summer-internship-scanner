import re
from pathlib import Path

# Constants
SOURCE_TEXT_FILE        = Path("tmp_blacklist-these.txt")
OUTPUT_MARKDOWN_FILE    = Path("blacklist.md")
URL_PATTERN             = re.compile(r"https://[^\s\)\]]+")

def _extract_urls_from_text(text: str):
    return URL_PATTERN.findall(text)

def _append_urls_to_markdown(urls, markdown_file: Path):
    with markdown_file.open("a", encoding="utf-8") as md_file:
        for url in urls:
            md_file.write(f"- {url}\n")

def main():
    if not SOURCE_TEXT_FILE.exists():
        print(f"Source file not found: {SOURCE_TEXT_FILE}")
        return
    
    text_content = SOURCE_TEXT_FILE.read_text(encoding="utf-8")
    urls = _extract_urls_from_text(text_content)

    if urls:
        _append_urls_to_markdown(urls, OUTPUT_MARKDOWN_FILE)
        print(f"Appended {len(urls)} URLs to {OUTPUT_MARKDOWN_FILE}")
    else:
        print("No URLs found in the source file.")

if __name__ == "__main__":
    main()

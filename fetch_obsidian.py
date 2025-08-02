import requests
from bs4 import BeautifulSoup

URL = "https://www.obsidian.net/careers/internships#open-positions"
EXPECTED_TEXT = (
    "Unfortunately, there are no open summer internship positions. Check back soon!"
)

def check_for_internships():
    response = requests.get(URL, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.find("div", class_="job-filter")
    if not container:
        raise RuntimeError("job-filter container not found")
    span = container.find("span", class_="job-filter-item job-open-positions")
    if not span:
        raise RuntimeError("job-filter-item job-open-positions span not found")
    text = span.get_text(strip=True)
    if text != EXPECTED_TEXT:
        raise NotImplementedError(
            f"Internship listing found or expected message changed: '{text}'. "
            "Implementation required."
        )
    print("No internship positions available at Obsidian.")
    return
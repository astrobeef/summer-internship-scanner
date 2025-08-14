"""
Unified Greenhouse fetcher for multiple boards.
"""
from __future__ import annotations

# standard lib
from typing import Any, Iterable

# third-party
import requests

# local
from constants import (
    TIMEOUT,
    HITS_SAVE_DIR,
    JOBS_SAVE_DIR,
    Job,
)
from util_fetch_io import (
    save_hits,
    save_jobs,
    load_objects,
)

##########################
# Config & API constants #
##########################

BASE_GREENHOUSE_API: str = "https://boards-api.greenhouse.io/v1/boards"

# Centralized per-board configuration
GREENHOUSE_SOURCES: list[dict[str, Any]] = [
    {
        "source": "databricks",
        "board_token": "databricks",
        "internship_department": "University Recruiting",
        "department_metadata_key": "Career Page Posting Category",
    },
    {
        "source": "pinterest",
        "board_token": "pinterest",
        "internship_department": "University",
        "department_metadata_key": "Careers Page Department",
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) "
        "Gecko/20100101 Firefox/141.0"
    ),
    "Accept": "application/json",
    "Referer": "https://boards.greenhouse.io/",
}

# Location formatting tokens
LOCATION_COMMA_SEP      : str = ","
LOCATION_HYPHEN_SEP     : str = "-"
TOKEN_MULTIPLE_LOCATIONS: str = "multiple locations"
TOKEN_BLANK             : str = "blank"
TOKEN_REMOTE            : str = "remote"

#############
# Utilities #
#############

def _config_for_source(source: str) -> dict[str, Any]:
    needle = source.strip().lower()
    for cfg in GREENHOUSE_SOURCES:
        if cfg["source"].lower() == needle:
            return cfg
    raise ValueError(f"Unknown source '{source}'. Valid: {[c['source'] for c in GREENHOUSE_SOURCES]}")

def _endpoint(board_token: str) -> str:
    return f"{BASE_GREENHOUSE_API}/{board_token}/jobs"

def _parse_id(hit: dict[str, Any]) -> str:
    return str(hit.get("id", ""))

def _metadata_lookup(hit: dict[str, Any], key_name: str) -> Any:
    """
    Case-insensitive lookup for a metadata 'name' within hit['metadata'].
    Returns the raw 'value' if present, else ''.
    """
    if not key_name:
        return ""
    meta_list: Iterable[dict[str, Any]] = hit.get("metadata") or []
    target = key_name.strip().lower()
    for m in meta_list:
        name = (m.get("name") or "").strip().lower()
        if name == target:
            return m.get("value", "")
    return ""

def _value_as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]

def _is_internship(hit: dict[str, Any], *, dept_key: str, dept_value: str) -> bool:
    """
    Determines if a job is an internship by comparing the configured department metadata.
    Uses tolerant matching (string equality after strip+lower) and supports list-or-string values.
    """
    meta_value = _metadata_lookup(hit, dept_key)
    for v in _value_as_list(meta_value):
        if isinstance(v, str) and v.strip().lower() == dept_value.strip().lower():
            return True
    return False

def _format_location(loc_name: str | None) -> str:
    """
    Normalizes location text:
      - blank -> ""
      - "multiple locations" -> "Multiple Locations"
      - "City, State, Country" -> "City, Country"
      - "remote - region" kept as "remote - region"
    """
    if not loc_name:
        return ""
    raw = loc_name.strip()
    if not raw:
        return ""
    if raw.lower() == TOKEN_MULTIPLE_LOCATIONS:
        return "Multiple Locations"
    parts = [p.strip() for p in raw.split(LOCATION_COMMA_SEP)]
    parts = [p for p in parts if p.lower() != TOKEN_BLANK]
    if len(parts) >= 2:
        city = parts[0]
        country = parts[-1]
        return f"{city}{LOCATION_COMMA_SEP} {country}"
    single = parts[0] if parts else raw
    if LOCATION_HYPHEN_SEP in single:
        lhs, rhs = (s.strip() for s in single.split(LOCATION_HYPHEN_SEP, 1))
        if lhs.lower() == TOKEN_REMOTE and rhs:
            return f"{lhs} {LOCATION_HYPHEN_SEP} {rhs}"
    return single

#########
# FETCH #
#########

def _fetch_hits_for_source(
    cfg: dict[str, Any],
    timeout_seconds: int,
    *,
    save_local: bool,
    verbose: bool,
) -> list[dict[str, Any]]:
    endpoint = _endpoint(cfg["board_token"])
    try:
        response = requests.get(
            url=endpoint,
            headers=HEADERS,
            timeout=timeout_seconds,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout as exc:
        raise RuntimeError(f"{cfg['source']} request timed out") from exc
    except requests.HTTPError as exc:
        status = getattr(response, "status_code", "unknown")
        body = getattr(response, "text", "")
        raise RuntimeError(f"{cfg['source']} request failed: {status} {body}") from exc

    payload = response.json() or {}
    # Greenhouse schema: {"jobs": [ ... ]}
    hits: list[dict[str, Any]] = payload.get("jobs") or []
    # Filter internships using the per-board config
    hits = [
        h for h in hits
        if _is_internship(h, dept_key=cfg["department_metadata_key"], dept_value=cfg["internship_department"])
    ]

    if verbose:
        print(f"Fetched {len(hits)} jobs from Greenhouse ({cfg['source']} board)")

    if save_local and hits:
        save_hits(hits, source=cfg["source"], id_fn=_parse_id, verbose=verbose)

    return hits

#########
# Parse #
#########

def _parse_jobs_from_hits(
    hits: list[dict[str, Any]],
    *,
    cfg: dict[str, Any],
    save_local: bool,
    verbose: bool,
) -> list[Job]:
    jobs: list[Job] = []
    dept_value = cfg["internship_department"]
    for h in hits:
        # Shared fields are accessed directly
        loc_name = h["location"].get("name")
        company = h["company_name"]
        job: Job = {
            "source": cfg["source"],
            "id": _parse_id(h),
            "title": h["title"],
            "url": h["absolute_url"],
            "location": _format_location(loc_name),
            "contract_type": "",
            "unique_meta": {
                "department": dept_value,                         # already filtered to internships
                "company": company,
                "requisition_id": h["requisition_id"],
                "first_published": h["first_published"],
                "updated_at": h["updated_at"],
                "education": h.get("education", ""),
            },
        }
        jobs.append(job)
    if save_local:
        save_jobs(jobs, verbose=verbose)
    return jobs

##############
# Public API #
##############

def _all_source_names() -> list[str]:
    return [c["source"] for c in GREENHOUSE_SOURCES]

def _normalize_sources(sources: list[str]) -> list[str]:
    wanted = {s.strip().lower() for s in sources}
    valid = {c["source"].lower(): c["source"] for c in GREENHOUSE_SOURCES}
    unknown = wanted - set(valid.keys())
    if unknown:
        raise ValueError(f"Unknown sources {sorted(unknown)}. Valid: {sorted(valid.values())}")
    return [valid[s] for s in wanted]

def parse_jobs_fetch_hits(
    *,
    sources: list[str] | None = None,
    timeout_seconds: int = TIMEOUT,
    save_local: bool = True,
    verbose: bool = False,
) -> list[Job]:
    """
    Fetch from the network and parse into Job objects for the given sources.
    Defaults to all configured sources when sources=None.
    """
    if sources is None:
        sources = _all_source_names()
    jobs: list[Job] = []
    for src in _normalize_sources(sources):
        cfg = _config_for_source(src)
        hits = _fetch_hits_for_source(cfg, timeout_seconds, save_local=save_local, verbose=verbose)
        jobs.extend(_parse_jobs_from_hits(hits, cfg=cfg, save_local=save_local, verbose=verbose))
    return jobs

def parse_jobs_cached_hits(
    *,
    sources: list[str] | None = None,
    save_local: bool = True,
    verbose: bool = False,
) -> list[Job]:
    """
    Parse cached raw hits for the given sources (previously saved via save_hits).
    Defaults to all configured sources when sources=None.
    """
    if sources is None:
        sources = _all_source_names()
    jobs: list[Job] = []
    for src in _normalize_sources(sources):
        cfg = _config_for_source(src)
        hits = load_objects(source=cfg["source"], dir=HITS_SAVE_DIR, verbose=verbose) or []
        jobs.extend(_parse_jobs_from_hits(hits, cfg=cfg, save_local=save_local, verbose=verbose))
    return jobs

###########
# EXECUTE #
###########

if __name__ == "__main__":
    for job in parse_jobs_fetch_hits(verbose=True):
        print(f"[{job['source']}] {job['title']} | {job['location']} | {job['url']}")
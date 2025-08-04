# first-party
import glob, json, os
from pathlib import Path
import sys
# local
from constants import (
    HITS_SAVE_DIR,
    JOBS_SAVE_DIR,
    Job
    )

def _build_path(
        source      :str,
        identifier  :str,
        *,
        dir         :str,
        make_dir    :bool = True,
        verbose     :bool = False
) -> Path:
    if make_dir:
        os.makedirs(dir, exist_ok=True)
    elif not os.path.isdir(dir):
        raise ValueError(f"No directory found at \"{dir}\"")
    path = Path(dir) / f"{source}_{identifier}.json"
    verbose and print(f"built path \"{path}\". Absolute: \"{path.resolve()}\"")
    return path

def save_hits(
        hits    :list,
        source  :str,
        *,
        dir     :str = HITS_SAVE_DIR,
        id_fn   :callable,
        verbose :bool = False
) -> None:
    for h in hits:
        job_id = str(id_fn(h))
        if not job_id or job_id == "None":
            raise ValueError('Could not find id in hit')
        path = _build_path(source, job_id, dir=dir, make_dir=True, verbose=verbose)
        with path.open("w", encoding="utf-8") as f:
            json.dump(h, f, indent=2, ensure_ascii=False)
    verbose and print(f"Saved {len(hits)} raw hits for {source}")
    return

def save_jobs(
        jobs    :list[Job],
        *,
        dir     :str = JOBS_SAVE_DIR,
        verbose :bool = False
) -> None:
    for j in jobs:
        job_id = j["id"]
        path = _build_path(j["source"], job_id, dir=dir, make_dir=True, verbose=verbose)
        with path.open("w", encoding="utf-8") as f:
            json.dump(j, f, indent=2, ensure_ascii=False)
    if jobs and len(jobs) > 0:
        verbose and print(f"Saved {len(jobs)} structured jobs for {j["source"]}")
    return

def load_objects(
        *,
        source      :str,
        dir         :str,
        verbose     :bool = False
) -> list:
    """Load either hits or jobs for a given source."""
    elements = []
    pattern_path = _build_path(source, "*", dir=dir, make_dir=False, verbose=verbose)
    pattern_dir  = pattern_path.parent
    pattern_str  = pattern_path.name
    for path in pattern_dir.glob(pattern_str):
      with open(path, encoding="utf-8") as f:
          e = json.load(f)
      elements.append(e)
    verbose and print(f"Loaded {len(elements)} objects from pattern: \"{pattern_path}\"")
    return elements

def load_all_jobs(
        dir     :str
) -> list[Job]:
    """Load all job dictionaries from JSON files in the specified directory."""
    jobs = []
    for fname in os.listdir(dir):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    jobs.append(data)
                else:
                    jobs.extend(data)
        except Exception as e:
            print(f"[FAIL] Loading {fpath}: {e}", file=sys.stderr)
    return jobs
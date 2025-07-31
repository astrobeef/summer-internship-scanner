import os

TIMEOUT = 10#seconds
HITS_SAVE_DIR = "./data/hits"
JOBS_SAVE_DIR = "./data/jobs"

def build_path(
        source      :str,
        identifier  :str,
        *,
        dir         :str,
        make_dir    :bool = True,
) -> str:
    if make_dir:
        os.makedirs(dir, exist_ok=True)
    elif not os.path.isdir(dir):
        raise ValueError("No directory found at \"{dir}\"")
    return os.path.join(dir, f"{source}_{identifier}.json")
# first-party
import json
import re
# local
from openai_create_client import (build_cache_query_path)


def _load_response():
    """
    Loads and returns JSON data from the specified file.
    Returns the Python object (dict or list) or None if loading fails.
    """
    filepath = build_cache_query_path()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)["response"]
    except Exception as e:
        print(f"Failed to load JSON from {filepath}: {e}")
        return None

def _parse_json(response_str) -> dict | None:
    """
    Takes a string (OpenAI response) and tries to parse it as JSON.
    """
    try:
        return json.loads(response_str)
    except json.JSONDecodeError:
        pass
    match = re.search(r'({.*})', response_str, flags=re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    return None

def load_openai_response(date = None):
    response_str    = _load_response()
    response        = _parse_json(response_str)
    return response
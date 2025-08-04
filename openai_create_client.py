# imports -- third-party
from datetime import datetime, timezone
import json
from openai import OpenAI           # for calling the OpenAI API
import os                           # for getting API token from env variable OPENAI_API_KEY
import tiktoken                     # for counting tokens
# local
from constants import (GPT_MODELS)

OPENAI_API_KEY  = "<your OpenAI API key if not set as env var>"

def create_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY", OPENAI_API_KEY))

def num_tokens(
        text    :str,
        model   :str
) -> int:
    """Return the number of tokens in a string"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # tiktoken is not up-to-date on GPT-4.1 and its variants. This is a fallback method that estimates tokens (but is not accurate for 4.1 variants)
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

##########################
# LOAD DAILY TOKEN USAGE #
##########################
# Load local save of daily token usage

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DAILY_TOKENS_PATH_PREFIX = os.path.join(DATA_DIR, "tokens_")  # used with e.g. +date+".json"
DATE_PATH_FORMAT = "%Y_%m_%d"

ADVANCED_MODELS_TOKEN_LIMIT = 200000    # Actual is 250,000
BASIC_MODELS_TOKEN_LIMIT = 2000000      # Actual is 2,500,000

ADVANCED_MODELS = [GPT_MODELS[0], GPT_MODELS[1]]
BASIC_MODELS    = [GPT_MODELS[2], GPT_MODELS[3], GPT_MODELS[4]]

def _get_daily_tokens_path():
    date_str = datetime.now(timezone.utc).strftime(DATE_PATH_FORMAT)
    return f"{DAILY_TOKENS_PATH_PREFIX}{date_str}.json"

def save_add_daily_tokens_used(p_tokens_used):
    path = _get_daily_tokens_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            count = int(data)
    else:
        count = 0
    count += int(p_tokens_used)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(count, f)

def _load_daily_tokens_used() -> int:
    path = _get_daily_tokens_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data)
    return 0

def is_daily_token_limit_reached(
        model :str,
        ):
    if model in ADVANCED_MODELS:
        return _load_daily_tokens_used() > ADVANCED_MODELS_TOKEN_LIMIT
    if model in BASIC_MODELS:
        return _load_daily_tokens_used() > BASIC_MODELS_TOKEN_LIMIT
    else:
        raise ValueError(f"Model \"{model}\" is not categorized, so a limit cannot be found.")
# imports -- third-party
from openai import OpenAI           # for calling the OpenAI API
import os                           # for getting API token from env variable OPENAI_API_KEY
import tiktoken                     # for counting tokens

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
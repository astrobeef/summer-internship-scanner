# imports -- third-party
from openai import OpenAI           # for calling the OpenAI API
import os                           # for getting API token from env variable OPENAI_API_KEY
import json                         # for writing cached embedding to JSON

# imports -- local
from constants import (
    GPT_MODELS,
    GPT_CHEAPEST,
    CHAT_TEMPERATURE,
    ASK_TOKEN_BUDGET,
    Job,
    clean_filename,
    )
from util_fetch_io import (load_all_jobs)
from openai_create_client import (num_tokens, create_client, save_add_daily_tokens_used, is_daily_token_limit_reached)
from append_full_descriptions import DETAILED_JOBS_SAVE_DIR
from openai_prompt import *

DESC_MAX_LENGTH     = 2000#characters
CACHE_QUERY_PATH    = "./data/openai_response/"
QUERY_FILE_NAME_END = 20#characters

def _build_gpt_message(query_msg: str) -> list[dict[str,str]]:
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": query_msg
        }
    ]

# NOTE: Calls upon `_gen_query_embedding(..)`, which uses OpenAI query embedding
def _build_query_message(
        jobs            :list[Job],
        *,
        query           :str,
        model           :str,
        token_budget    :int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    question        :str            = f"\n\nQuestion: {query}"
    message         :str            = QUERY_INTRO
    message         += _compile_jobs_into_msg(
        jobs,
        message         =message,
        question        =question,
        model           =model,
        token_budget    =token_budget
    )
    return message + question

def _compile_jobs_into_msg(
        jobs            :list[Job],
        *,
        message         :str,
        question        :str,
        model           :str,
        token_budget    :int,
) -> str:
    message_addition :str = ''
    for j in jobs:
        next_entry = (
            f"source:{j["source"]}\n"
            f"id:{j["id"]}\n"
            f"title:{j["title"]}\n"
            f"url:{j["url"]}\n"
            f"location:{j["location"]}\n"
            f"contract_type:{j["contract_type"]}\n"
            f"unique_meta:{json.dumps(j["unique_meta"])}\n"
            f"unique_meta:{j["description"][:DESC_MAX_LENGTH]}\n"
            )
        if (token_budget < num_tokens(message + message_addition + next_entry + question, model=model)):
            break
        else:
            message_addition += next_entry
    return message_addition

############
# RESPONSE #
############

def _gen_response(
        client  :OpenAI,
        messages:list[dict[str,str]],
        model   :str
) -> str:
    if is_daily_token_limit_reached(model=model):
        if not is_daily_token_limit_reached(model=GPT_CHEAPEST):
            print(f"WARNING: Daily token limit reached for parameter model \"{model}\". Switching to cheapest model: \"{GPT_CHEAPEST}\"")
            model = GPT_CHEAPEST
        else:
            raise ValueError(f"Cannot generate response because the daily limit for model \"{model}\" has been reached. If this is an advanced model, basic models may still be available.")
    response            = client.chat.completions.create(
    model                   =model,
    messages                =messages,
    temperature             =CHAT_TEMPERATURE
)
    response_message    = response.choices[0].message.content
    save_add_daily_tokens_used(response.usage.total_tokens)
    return response_message

#######
# I/O #
#######

def _save_local_query_and_response(
        *,
        query           :str,
        query_messages  :list[dict[str,str]],
        response        :str = "OMITTED",
        verbose         :bool = False,
) -> None:
    file_path   = _build_query_path(query)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data        = {
        "query"         : query,
        "query_messages": query_messages,
        "response"      : response
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    if verbose:
        print(f'Saved query: "{file_path}"')
    return

def _build_query_path(query :str):
    return f"{CACHE_QUERY_PATH}{clean_filename(query)[0:QUERY_FILE_NAME_END]}.json"

###########
# EXECUTE #
###########

def filter_jobs(
        jobs            :list[Job],
        *,
        query           :str,
        model           :str    = GPT_CHEAPEST,
        token_budget    :int    = ASK_TOKEN_BUDGET,
        verbose         :bool   = False,
        save_local      :bool   = True
) -> list[dict[str,str]] | str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings.
    """
    client      = create_client()
    query_msg   = _build_query_message(
        jobs,
        query        =query,
        model        =model,
        token_budget =token_budget
    )
    if verbose:
        print(f"QUERY MESSAGE:{query_msg}")
    messages    = _build_gpt_message(query_msg)
    response    = _gen_response(client, messages, model)
    if save_local:
        _save_local_query_and_response(
            query           =query,
            query_messages  =messages,
            response        =response,
            verbose         =verbose
        )
    return response
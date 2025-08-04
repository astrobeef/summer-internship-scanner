# first-party
import traceback
import argparse
# local
from dispatch_email import (send_email)
from pipeline import fetch_all_jobs_and_dispatch
from constants import (GPT_MODELS)

ERROR_LOG_PATH = "./error.log"

def main():
    parser = argparse.ArgumentParser(description="Internship Scanner Pipeline CLI")
    parser.add_argument("--run", action="store_true", help="Run the daily internship scan and notification.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--model", type=str, default=GPT_MODELS[1], help="OpenAI model to use.")
    args = parser.parse_args()

    if args.run:
        fetch_all_jobs_and_dispatch(verbose=args.verbose)
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        tb = traceback.format_exc()
        with open(ERROR_LOG_PATH, "w", encoding="utf-8") as f:
            f.write(tb)
        send_email(
            subject         ="Internship Pipeline Error",
            plain_body      =f"An error occurred in the internship pipeline:\n\n{tb}",
            html_body       =None,
        )
    finally:
        input("\nInternship scanner finished. Press Enter to exit...")
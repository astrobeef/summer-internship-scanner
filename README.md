# Internship Scanner Pipeline

Automates the end-to-end process of discovering, filtering, and notifying me of new software engineering internships for Summer 2026 opportunities for undergraduate students in the US and Canada. In the future it could be easily customized for other focuses.
## Overview
- Aggregates job postings from major tech companies and job boards.
- Scrapes and parses full job descriptions.
- Filters postings using OpenAI models to categorize as "close match," "near match," or "non match" based on custom logic for CS/software internships.
- Sends automated email notifications with results.

## Features
- Multi-source job fetch: Amazon, Microsoft, Sony, Epic, Honeywell, Hitmarker, and more.
- Scrapes rendered HTML to handle dynamic job boards.
- Categorizes jobs using OpenAI's GPT models for filtering ambigious descriptions which are not always clear if an internship is for the summer or not.
- Email notifications for new or relevant matches.
- Command-line interface for scheduling and manual runs.

## Usage
- Install dependencies (see requirements.txt).
- Run the main pipeline:
    `python main.py --run`
    - Use -v for verbose logging.
- Configure email credentials in data/_keys/gmail_config.py.

### Automated Scheduling (Windows)
To run the internship scanner automatically on a schedule, use the provided `run_main.bat` file with Windows Task Scheduler.

Steps:
- Edit `run_main.bat` if needed
- Open Task Scheduler
    - Press Win + S, type Task Scheduler, and open it.
    - Create a New Task
        - Click `Create Task`.
        - General tab:
            - Set a name (`Summer 2026 Internship Scanner`)
            - (Optional) Set to Run only when user is logged in
            - Configure for: `Windows 10`
        - Triggers tab:
            - Add new trigger to begin task `on a schedule`
            - Choose your schedule (I use weekly with weekdays selected).
            - Set advanced settings (such as expiration after Summer 2026).
        - Actions tab:
            - New Action to `Start a program`
            - Program/script: Full path to run_main.bat (`C:\...\summer-internship-scanner\run_main.bat`)
            - Start in: Project directory (`C:\...\summer-internship-scanner`)
        - Conditions tab:
            - Under Network, check the box: `Start only if...` to ensure internet connection
        - Settings tab:
            - (Optional) Check box to `Run task as soon as possible after a scheduled start is missed`
            - (Optional) Check the box to `Stop the task if it runs longer than ...`
            - (Optional) Check the box to `If the running task does not end when requested, force it to stop`
    - Save the Task

Now, the internship scanner will run automatically on your chosen schedule.

## Customization
- To change OpenAI models or query logic, edit `constants.py` and `openai_prompt.py`.
- For custom filtering or notifications, modify `openai_filter.py` and `dispatch_email.py`.

## Structure
- `main.py`: CLI entry point.
- `pipeline.py`: Orchestrates job fetching, description augmentation, filtering, and notifications.
- `fetch.py`, `fetch_...py`, `append_full_descriptions.py`: Fetch and parse job postings and descriptions.
- `openai_filter.py`: Categorizes postings using OpenAI.
- `dispatch_email.py`: Formats and sends notification emails.

## Notes
- Data directories (./data/jobs, ./data/jobs_detailed, etc.) will be created as needed.
- OpenAI API key and email credentials are required.
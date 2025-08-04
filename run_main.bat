REM Set up through Windows Task Scheduler. Task Action set to start within project directory.

call .venv\Scripts\activate

python main.py --run -v

REM pause
QUERY_INTRO = (
    "You will receive a list of job postings. Each posting includes fields such as source, id, title, url, location, contract_type, and a job description. "
    "Your task: Identify postings that are internships for Summer 2026 specifically for current undergraduate (Bachelor's) students. "
    "Prefer postings that explicitly mention 'Summer 2026', 'internship', or similar terms, or that describe a paid internship for undergraduates during the summer months of 2026 (for example, 10–12 week roles beginning in May or June 2026). "
    "Exclude jobs targeting PhD or graduate students, or permanent/return offers. "
    "If a job posting lacks a sufficient description (or is otherwise very minimal), be more lenient and include it if the title and other fields indicate it is likely a Summer 2026 internship suitable for undergraduates. "
    "Return only the URLs of qualifying jobs, one per line. "
    "If none qualify, respond exactly with:\n"
    "Could not find any Summer 2026 Internships."
)

QUESTION = (
    "\n\nQuestion: Which of these jobs are internships for Summer 2026, intended for current undergraduate students (Bachelor's level)? "
    "Respond with only the URLs of matching jobs, one per line. "
    "If none qualify, respond exactly with:\n"
    "Could not find any Summer 2026 Internships."
)

SYSTEM_PROMPT = (
    "You are a detail-oriented job filtering assistant. "
    "Your goal is to select postings that are internships for Summer 2026, intended specifically for current undergraduate (Bachelor's) students. "
    "Use all available information—title, description, contract type, and duration. "
    "Accept postings if they explicitly state this, or if the duration, timing, and requirements strongly imply it (e.g., a 12-week internship starting May/June 2026 open to undergraduates). "
    "Do NOT include postings for PhD/graduate students, permanent roles, or full-time conversion/return offers. "
    "If a job is missing a description or has little detail, include it if the other fields (like the title) strongly suggest it fits. "
    "If no jobs qualify, respond exactly with: Could not find any Summer 2026 Internships. "
    "Otherwise, respond ONLY with the URLs of matching jobs, one per line."
    )
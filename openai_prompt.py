QUERY_INTRO = (
    "You will receive a list of job postings. Each posting includes fields such as source, id, title, url, location, contract_type, and a job description. "
    "Your task: Analyze and categorize each posting based on how well it matches the following criteria: "
    "A Summer 2026 internship suitable for current undergraduate (Bachelor's) students, focused in CS, Software Engineering, or related field. Strictly in the US or Canada."
    "A 'close match' is a job that directly mentions Summer 2026 and internships for undergraduates, or clearly describes a summer internship for Bachelor's students starting in May/June 2026. "
    "A 'near match' is a job that is likely a summer internship for undergraduates, but the year or target student level is implied, not explicit, or some relevant details are missing. "
    "A 'non match' is a posting that is not an internship, is for graduate/PhD students, is a permanent or full-time return offer, or has no indication of being a Summer 2026 internship. "
    "If a job lacks a sufficient description, be more lenient and use available information (such as title and contract type) to categorize. "
    "Return your answer as a single, valid JSON object with exactly these keys: close_match, near_match, non_match. "
    "Each value should be a list of job objects, each with at least the fields: url, title, and reason. "
    "If a category has no matches, return an empty list for that category. "
    "Example response:\n"
    "{\n"
    "  \"close_match\": [{\"url\": \"...\", \"title\": \"...\"}, \"reason\": \"...\"}],\n"
    "  \"near_match\": [{\"url\": \"...\", \"title\": \"...\"}, \"reason\": \"...\"}],\n"
    "  \"non_match\": [{\"url\": \"...\", \"title\": \"...\"}, \"reason\": \"...\"}]\n"
    "}"
)

QUESTION = (
    "\n\nQuestion: For each job posting, categorize as 'close_match', 'near_match', or 'non_match' using the definitions above. "
    "Respond with a single JSON object with those keys, each a list of objects containing at least the url, title, and reason for each job."
)

SYSTEM_PROMPT = (
    "You are a meticulous job categorization assistant. "
    "For each job posting you receive, use all available information—title, description, contract type, and duration—to determine how well it matches a Summer 2026 internship for current undergraduate (Bachelor's) students, focused in CS, Software Engineering, or related field. Strictly in the US or Canada."
    "'Close match' means all requirements are met explicitly. 'Near match' means the job is likely to fit, but with some ambiguity or missing info. 'Non match' means the posting does not fit. "
    "Be lenient for jobs with minimal descriptions, but do not place jobs in 'close_match' unless they strongly fit. "
    "Respond only with a single, valid JSON object with the keys close_match, near_match, non_match, each containing a list of jobs (url, title, reason)."
)
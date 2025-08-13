
# first-party
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from data._keys.gmail_config import CONFIG

# local
from openai_parse_response import load_openai_response
from constants import (
    Response
)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 465

def send_email(subject: str, plain_body: str, html_body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = CONFIG["sender_email"]
    msg["To"]      = CONFIG["recipient_email"]
    msg.set_content(plain_body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(CONFIG["sender_email"], CONFIG["sender_app_password"])
        smtp.send_message(msg)

def _build_section(title: str, items: list[dict]) -> tuple[str, str]:
    """Return (plain_text, html) for one match section."""
    if not items:
        return f"{title}: None\n\n", f"<h2>{title}</h2><p><em>None</em></p>"
    plain_lines = [f"{title} ({len(items)})"]
    html_lines  = [f"<h2>{title} ({len(items)})</h2><ul>"]
    for i, itm in enumerate(items, 1):
        plain_lines.append(
            f"{i}. {itm['title']}\n   {itm['url']}\n   Reason: {itm.get('reason','')}\n"
        )
        html_lines.append(
            f"<li><strong>{itm['title']}</strong><br>"
            f'<a href="{itm["url"]}">{itm["url"]}</a><br>'
            f"<em>{itm.get('reason','')}</em></li>"
        )
    html_lines.append("</ul>")
    return "\n".join(plain_lines) + "\n", "\n".join(html_lines)

def _notify_matches(response: Response):
    """Send email listing close, near, non matches in order."""
    if response is None:
        print("No response data to notify.")
        return
    plain_parts, html_parts = [], []
    for title, key in [
        ("Close Matches", "close_match"),
        ("Near Matches",  "near_match"),
        ("Non Matches",   "non_match"),
    ]:
        p, h = _build_section(title, response.get(key, []))
        plain_parts.append(p)
        html_parts.append(h)
    plain_body = "\n".join(plain_parts)
    html_body  = "<html><body>" + "<hr>".join(html_parts) + "</body></html>"
    subject = (
        f"Job Scan Results: {len(response['close_match'])} Close, {len(response['near_match'])} Near, {len(response['non_match'])} Non-Matches"
    )
    send_email(subject, plain_body, html_body)
    print("Notification sent.")

def _has_matches(response: Response):
    return len(response["close_match"]) > 0 or len(response["near_match"]) > 0

def dispatch_email(response: Response = None):
    if not response:
        response: Response = load_openai_response()
    if _has_matches(response):
        _notify_matches(response)
    else:
        print("Neglecting email since there are no matches")
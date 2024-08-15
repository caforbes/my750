from datetime import timedelta, date
import markdown
from markupsafe import escape


def date_before_today(days: int = 0) -> date:
    if days < 0:
        raise ValueError("Provide a number of days that is 0 or greater.")
    delta = timedelta(days=days)
    return date.today() - delta


def usertext_to_md(text: str) -> str:
    clean_text = escape(text)
    return markdown.markdown(clean_text)

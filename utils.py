from datetime import timedelta, date


def date_before_today(days: int = 0) -> date:
    # TODO: test
    today = date.today()
    delta = timedelta(days=days)
    return today - delta

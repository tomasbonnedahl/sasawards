from datetime import datetime, timedelta


def calculate_future_date(max_date, days_ahead):
    if max_date is not None:
        return datetime.strptime(max_date, "%Y%m%d").date()
    return datetime.now().date() + timedelta(days=days_ahead)

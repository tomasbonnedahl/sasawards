from datetime import datetime, timedelta


def calculate_max_date(max_date, days_ahead):
    if max_date is None:
        return datetime.now().date() + timedelta(days=days_ahead)
    else:
        return datetime.strptime(max_date, "%Y%m%d").date()

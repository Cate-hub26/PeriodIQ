from datetime import datetime, timedelta
from typing import List

def predict_next_period(start_dates: List[str]) -> str:
    """
    Predicts the next period start date based on average cycle length.
    Dates should be in 'YYYY-MM-DD' format.
    """
    if len(start_dates) < 2:
        return "Insufficient data"

    sorted_dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in start_dates])
    cycle_lengths = [
        (sorted_dates[i] - sorted_dates[i - 1]).days
        for i in range(1, len(sorted_dates))
    ]

    avg_length = sum(cycle_lengths) / len(cycle_lengths)
    last_date = sorted_dates[-1]
    predicted_date = last_date + timedelta(days=round(avg_length))

    return predicted_date.strftime("%Y-%m-%d")
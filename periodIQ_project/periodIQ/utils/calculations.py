from datetime import datetime
from typing import List, Dict

def calculate_period_duration(start_date: str, end_date: str) -> int:
    """
    Returns the duration of a period in days.
    Dates should be in 'YYYY-MM-DD' format.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return (end - start).days + 1  # Inclusive of start and end

def calculate_cycle_lengths(entries: List[Dict[str, str]]) -> List[int]:
    """
    Returns a list of cycle lengths based on period start dates.
    Each entry should be a dict with 'start_date' key.
    """
    start_dates = sorted([datetime.strptime(e['start_date'], "%Y-%m-%d") for e in entries])
    cycle_lengths = []

    for i in range(1, len(start_dates)):
        cycle_lengths.append((start_dates[i] - start_dates[i - 1]).days)

    return cycle_lengths

def average_cycle_length(cycle_lengths: List[int]) -> float:
    """
    Returns the average cycle length.
    """
    if not cycle_lengths:
        return 0.0
    return round(sum(cycle_lengths) / len(cycle_lengths), 2)
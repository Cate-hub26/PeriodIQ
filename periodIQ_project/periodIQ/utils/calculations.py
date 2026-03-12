from datetime import datetime
from typing import List, Dict, Union

def calculate_period_duration(start_date: str, end_date: str) -> Union[int, Dict[str, str]]:
    """
    Returns the duration of a period in days (inclusive).
    If dates are invalid, returns an error dict.
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if end < start:
            return {"error": "End date must be after start date."}
        return (end - start).days + 1
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

def calculate_cycle_lengths(entries: List[Dict[str, str]]) -> Union[List[int], Dict[str, str]]:
    """
    Calculates cycle lengths from a list of period start dates.
    Each entry must contain a valid 'start_date' in 'YYYY-MM-DD' format.
    """
    try:
        start_dates = sorted([
            datetime.strptime(e['start_date'], "%Y-%m-%d")
            for e in entries if 'start_date' in e
        ])
        if len(start_dates) < 2:
            return {"error": "At least two valid start dates are required."}

        return [
            (start_dates[i] - start_dates[i - 1]).days
            for i in range(1, len(start_dates))
        ]
    except ValueError:
        return {"error": "One or more dates are invalid. Use YYYY-MM-DD format."}

def average_cycle_length(cycle_lengths: List[int]) -> float:
    """
    Returns the average cycle length.
    """
    if not cycle_lengths:
        return 0.0
    return round(sum(cycle_lengths) / len(cycle_lengths), 2)

def detect_irregularity(cycle_lengths: List[int]) -> bool:
    """
    Flags irregular cycles if the range exceeds 5 days.
    """
    if not cycle_lengths:
        return False
    return (max(cycle_lengths) - min(cycle_lengths)) > 5                       
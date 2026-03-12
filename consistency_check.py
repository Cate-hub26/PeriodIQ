from datetime import datetime
from statistics import mean, stdev
from typing import List, Dict
from .utils.calculations import calculate_cycle_lengths
from django.contrib.auth import get_user_model

User = get_user_model()

# Thresholds

MAX_STD_DEV = 2.0 # days

MAX_GAP = 5 # days

MIN_EVENTS = 3 # minimum data points to assess

def check_consistency(timestamps: List[datetime]) -> Dict:
    
    """
    Evaluates consistency of cycle start dates.
    Returns metrics including average, min, max, std deviation,
    and a consistency flag.
    """
    if len(timestamps) < MIN_EVENTS:
        return {
            "status": "no_data",
            "average_cycle": None,
            "min_cycle": None,
            "max_cycle": None,
            "irregular_flag": None
        }
    
     # Convert datetime objects to dicts for reuse
    entries = [{"start_date": dt.strftime("%Y-%m-%d")} for dt in timestamps]
    gaps = calculate_cycle_lengths(entries)
    
    if len(gaps) < MIN_EVENTS - 1:
        return {
            "status": "insufficient_data",
            "average_cycle": None,
            "min_cycle": None,
            "max_cycle": None,
            "irregular_flag": None
        }
    
    avg_gap = mean(gaps)
    std_dev = stdev(gaps) if len(gaps) > 1 else 0
    max_gap = max(gaps)
    min_gap = min(gaps)
    
    gap_range = max_gap - min_gap
    irregular_flag = not (std_dev <= MAX_STD_DEV and gap_range <= MAX_GAP)
    
    return {
        "status": "ok",
        "average_cycle": avg_gap,
        "min_cycle": min_gap,
        "max_cycle": max_gap,
        "irregular_flag": irregular_flag
    }

        

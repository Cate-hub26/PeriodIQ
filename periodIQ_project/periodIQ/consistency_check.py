from datetime import datetime
from statistics import mean, stdev
from typing import List, Dict
from .utils.calculations import calculate_cycle_lengths

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
            "average_gap": None,
            "min_gap": None,
            "max_gap": None,
            "std_dev": None,
            "is_consistent": None
        }
    
     # Convert datetime objects to dicts for reuse
    entries = [{"start_date": dt.strftime("%Y-%m-%d")} for dt in timestamps]
    gaps = calculate_cycle_lengths(entries)
    
    if len(gaps) < MIN_EVENTS - 1:
        return {
            "status": "insufficient_data",
            "average_gap": None,
            "min_gap": None,
            "max_gap": None,
            "std_dev": None,
            "is_consistent": None
        }
    
    avg_gap = mean(gaps)
    std_dev = stdev(gaps) if len(gaps) > 1 else 0
    max_gap = max(gaps)
    min_gap = min(gaps)
    
    is_consistent = std_dev <= MAX_STD_DEV and max_gap <= MAX_GAP
    
    return {
        "status": "ok",
        "average_gap": avg_gap,
        "min_gap": min_gap,
        "max_gap": max_gap,
        "std_dev": std_dev,
        "is_consistent": is_consistent
    }

        

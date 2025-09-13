from datetime import datetime, timedelta
from typing import List, Dict, Union

def predict_next_period(cycle_data: List[int]) -> Dict[str, Union[str, float]]:
    """
    Predicts the next period start date based on average cycle length.
    
    Args:
        cycle_data (List[int]): List of cycle lengths in days.
    
    Returns:
        Dict[str, Union[str, float]]: Predicted next start date and average cycle length.
    
    """
    
    if not cycle_data or not all(isinstance(d, int) and d > 0 for d in cycle_data):
        return {"error": "Insufficient data"}

    average_cycle = sum(cycle_data) / len(cycle_data)
    today = datetime.today()
    predicted_date = today + timedelta(days=round(average_cycle))

    return {
        "next_period": predicted_date.strftime("%Y-%m-%d"),
    }
    
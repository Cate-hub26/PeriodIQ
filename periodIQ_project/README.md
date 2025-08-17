# PeriodIQ API Documentation

## Authentication
- All endpoints require authenticated access.
- This project currently uses Django REST Framework’s `IsAuthenticated` permission.
- Tokens must be sent in the request header.
- Format depends on your auth setup:
  - **JWT Authentication:**  
    `Authorization: Bearer <your_token>`
  - **DRF Token Authentication:**  
    `Authorization: Token <your_token>`

---

## Models

### CustomUser
- Extends Django’s `AbstractUser`.
- Additional fields:
  - `email` (unique)
  - `typical_cycle_length` (integer, default 28)

### PeriodEntry
- Tracks individual period start dates.
- Fields:
  - `user` - ForeignKey to `CustomUser` (owner)
  - `start_date` - Date of the period start
  - `end_date` - Date the period ends
### CycleStart
- Stores cycle statistics for a user.
- Fields:
  - `user` - ForeignKey to `CustomUser`
  - `average_cycle` - Integer
  - `min_cycle` - Integer
  - `max_cycle` - Integer
  - `irregular_flag` - Boolean (true if irregular cycles)

---

## API Endpoints

### 1. **List & Create Period Entries**
**GET** `/period/`  
Returns all period entries for the authenticated user.

**POST** `/period/`  
Creates a new period entry for the authenticated user.

### 2. **Retrieve, Update & Delete a Period Entry**
**GET** `/period/<id>/`  
Retrieves a specific period entry by its ID.

**PUT** `/period/<id>/`  
Updates all fields of a specific period entry.  

**POST body example**:
```json
{
  "start_date": "2025-08-15"
}

## PeriodIQ Backend Calculations

This backend module provides core logic for menstrual cycle tracking and prediction. It includes utilities for calculating period durations, cycle lengths, average cycle length, and predicting the next expected period.

---

## Module Structure

- `calculations.py`: Handles duration and cycle length calculations.
- `predictions.py`: Predicts the next period start date based on historical data.

---

## calculations.py

### 🔹 `calculate_period_duration(start_date: str, end_date: str) -> int`

Returns the duration of a period in days, inclusive of both start and end dates.

**Parameters**:
- `start_date`: Start date of the period (`'YYYY-MM-DD'`)
- `end_date`: End date of the period (`'YYYY-MM-DD'`)

**Returns**:
- `int`: Number of days in the period

**Example**:
```python
calculate_period_duration("2025-08-01", "2025-08-05")  # Returns 5

## File: `predictions.py`

### Function: `predict_next_period(start_dates: List[str]) -> str`

Predicts the next expected period start date using average cycle length derived from previous entries.

---

### Parameters

- `start_dates`: A list of strings representing past period start dates  
  Format: `'YYYY-MM-DD'`

---

### Returns

- `str`: Predicted next start date in `'YYYY-MM-DD'` format  
- Returns `"Insufficient data"` if fewer than two start dates are provided

---

### Example Usage

```python
from predictions import predict_next_period

dates = ["2025-07-01", "2025-07-29", "2025-08-26"]
next_period = predict_next_period(dates)
print(next_period)  # Output: "2025-09-23"

## cycle_summary

### Endpoint
`GET /cycle-summary/`

### Description
Returns a summary of the authenticated user's menstrual cycle data, including:

- Average cycle length
- Average period duration
- Total number of entries

### Authentication
- Required: Yes
- Method: Token-based

### Permissions
- Only accessible to authenticated users (`IsAuthenticated`)

---

### esponse Format

#### success (`200 OK`)
```json
{
  "average_cycle_length": 28.5,
  "average_period_duration": 4.2,
  "entry_count": 12
}
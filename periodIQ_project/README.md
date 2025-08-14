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
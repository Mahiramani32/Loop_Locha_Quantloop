# Episodic Intelligence Engine API Documentation

## Base URL

## Endpoints

### 1. Health Check

**GET** `/health`

Check if API is running.

**Response:**

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "environment": "development"
  },
  "message": "API is running",
  "timestamp": "2024-01-15T10:30:00Z",
  "status_code": 200
}
```

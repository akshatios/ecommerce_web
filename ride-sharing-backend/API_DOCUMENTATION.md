# Ride Sharing API Documentation

## Complete API Reference

### Base URLs
- Auth Service: `http://localhost:8001`
- User Service: `http://localhost:8002`
- Driver Service: `http://localhost:8003`
- Location Service: `http://localhost:8004`
- Trip Service: `http://localhost:8005`
- Payment Service: `http://localhost:8006`
- Notification Service: `http://localhost:8007`
- Pricing Service: `http://localhost:8008`

---

## 1. Auth Service (Port 8001)

### POST /api/v1/auth/signup
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true
}
```

### POST /api/v1/auth/login
Login and get JWT token.

**Request Body (form-data):**
```
username: user@example.com
password: securepassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 2. User Service (Port 8002)

### POST /api/v1/riders
Create a rider profile.

**Request Body:**
```json
{
  "user_id": 1,
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "phone": "+1234567890",
  "wallet_balance": 0.0,
  "rating": 5.0,
  "created_at": "2025-11-27T10:00:00"
}
```

### GET /api/v1/riders/{rider_id}
Get rider details.

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "phone": "+1234567890",
  "wallet_balance": 150.50,
  "rating": 4.8,
  "created_at": "2025-11-27T10:00:00"
}
```

---

## 3. Driver Service (Port 8003)

### POST /api/v1/drivers
Create a driver profile with vehicle.

**Request Body:**
```json
{
  "user_id": 2,
  "license_number": "DL123456",
  "vehicle": {
    "make": "Toyota",
    "model": "Camry",
    "plate_number": "ABC123",
    "color": "Black"
  }
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 2,
  "license_number": "DL123456",
  "is_verified": false,
  "rating": 5.0,
  "vehicle": {
    "id": 1,
    "make": "Toyota",
    "model": "Camry",
    "plate_number": "ABC123",
    "color": "Black"
  }
}
```

### GET /api/v1/drivers/{driver_id}
Get driver details.

---

## 4. Location Service (Port 8004)

### POST /api/v1/location/update
Update driver's current location.

**Request Body:**
```json
{
  "driver_id": 1,
  "latitude": 28.6139,
  "longitude": 77.2090
}
```

**Response:**
```json
{
  "status": "updated"
}
```

### GET /api/v1/location/nearby
Find nearby drivers.

**Query Parameters:**
- `latitude`: float (required)
- `longitude`: float (required)
- `radius_km`: float (default: 5.0)

**Example:**
```
GET /api/v1/location/nearby?latitude=28.6139&longitude=77.2090&radius_km=5
```

**Response:**
```json
{
  "drivers": [
    {
      "driver_id": 1,
      "distance_km": 2.5
    },
    {
      "driver_id": 3,
      "distance_km": 4.2
    }
  ]
}
```

---

## 5. Trip Service (Port 8005)

### POST /api/v1/trips/request
Request a new trip (auto-assigns nearest driver).

**Request Body:**
```json
{
  "rider_id": 1,
  "pickup_lat": 28.6139,
  "pickup_lng": 77.2090,
  "dropoff_lat": 28.7041,
  "dropoff_lng": 77.1025
}
```

**Response:**
```json
{
  "id": 1,
  "rider_id": 1,
  "driver_id": 1,
  "status": "ASSIGNED",
  "fare": null,
  "created_at": "2025-11-27T10:30:00"
}
```

### GET /api/v1/trips/{trip_id}
Get trip details.

**Response:**
```json
{
  "id": 1,
  "rider_id": 1,
  "driver_id": 1,
  "status": "COMPLETED",
  "fare": 250.50,
  "created_at": "2025-11-27T10:30:00"
}
```

**Trip Status Values:**
- `REQUESTED`: Trip requested, waiting for driver
- `ASSIGNED`: Driver assigned
- `STARTED`: Trip in progress
- `COMPLETED`: Trip completed
- `CANCELLED`: Trip cancelled

---

## 6. Payment Service (Port 8006)

### POST /api/v1/payments
Create a payment record.

**Request Body:**
```json
{
  "trip_id": 1,
  "rider_id": 1,
  "driver_id": 1,
  "amount": 250.50,
  "method": "CARD"
}
```

**Response:**
```json
{
  "id": 1,
  "trip_id": 1,
  "rider_id": 1,
  "driver_id": 1,
  "amount": 250.50,
  "method": "CARD",
  "status": "PENDING",
  "transaction_id": null,
  "created_at": "2025-11-27T11:00:00"
}
```

### POST /api/v1/payments/{payment_id}/process
Process a payment (simulated).

**Response:**
```json
{
  "id": 1,
  "trip_id": 1,
  "rider_id": 1,
  "driver_id": 1,
  "amount": 250.50,
  "method": "CARD",
  "status": "COMPLETED",
  "transaction_id": "txn_a1b2c3d4e5f6",
  "created_at": "2025-11-27T11:00:00"
}
```

### GET /api/v1/payments/{payment_id}
Get payment details.

### GET /api/v1/payments/trip/{trip_id}
Get payment by trip ID.

**Payment Methods:**
- `CARD`
- `WALLET`
- `UPI`
- `CASH`

**Payment Status:**
- `PENDING`
- `PROCESSING`
- `COMPLETED`
- `FAILED`
- `REFUNDED`

---

## 7. Notification Service (Port 8007)

### POST /api/v1/notifications/send
Send push notification (stub).

**Request Body:**
```json
{
  "device_token": "fcm_token_here",
  "title": "New Trip Request",
  "body": "You have a new trip request nearby",
  "data": {
    "trip_id": 1,
    "type": "trip_request"
  }
}
```

**Response:**
```json
{
  "status": "sent",
  "message": "Push notification stub"
}
```

---

## 8. Pricing Service (Port 8008)

### POST /api/v1/pricing/calculate
Calculate fare estimate.

**Request Body:**
```json
{
  "pickup_lat": 28.6139,
  "pickup_lng": 77.2090,
  "dropoff_lat": 28.7041,
  "dropoff_lng": 77.1025,
  "estimated_time_minutes": 0
}
```

**Response:**
```json
{
  "distance_km": 12.5,
  "estimated_time_minutes": 25.0,
  "base_fare": 50.0,
  "distance_fare": 187.5,
  "time_fare": 50.0,
  "surge_multiplier": 1.0,
  "total_fare": 287.5
}
```

**Pricing Formula:**
```
total_fare = (base_fare + distance_fare + time_fare) * surge_multiplier

where:
  base_fare = 50.0 (configurable)
  distance_fare = distance_km * 15.0
  time_fare = estimated_time_minutes * 2.0
  surge_multiplier = 1.0 (dynamic, based on demand)
```

---

## Complete User Journey

### 1. Rider Flow

```bash
# Step 1: Register
POST /api/v1/auth/signup
{
  "email": "rider@example.com",
  "password": "pass123",
  "full_name": "Alice"
}

# Step 2: Login
POST /api/v1/auth/login
username=rider@example.com&password=pass123

# Step 3: Create Rider Profile
POST /api/v1/riders
{
  "user_id": 1,
  "phone": "+1234567890"
}

# Step 4: Get Fare Estimate
POST /api/v1/pricing/calculate
{
  "pickup_lat": 28.6139,
  "pickup_lng": 77.2090,
  "dropoff_lat": 28.7041,
  "dropoff_lng": 77.1025
}

# Step 5: Request Trip
POST /api/v1/trips/request
{
  "rider_id": 1,
  "pickup_lat": 28.6139,
  "pickup_lng": 77.2090,
  "dropoff_lat": 28.7041,
  "dropoff_lng": 77.1025
}

# Step 6: Track Trip
GET /api/v1/trips/1

# Step 7: Complete Payment
POST /api/v1/payments
{
  "trip_id": 1,
  "rider_id": 1,
  "driver_id": 1,
  "amount": 287.5,
  "method": "CARD"
}

POST /api/v1/payments/1/process
```

### 2. Driver Flow

```bash
# Step 1: Register
POST /api/v1/auth/signup
{
  "email": "driver@example.com",
  "password": "pass123",
  "full_name": "Bob"
}

# Step 2: Login
POST /api/v1/auth/login

# Step 3: Create Driver Profile
POST /api/v1/drivers
{
  "user_id": 2,
  "license_number": "DL123456",
  "vehicle": {
    "make": "Toyota",
    "model": "Camry",
    "plate_number": "ABC123",
    "color": "Black"
  }
}

# Step 4: Go Online (Update Location)
POST /api/v1/location/update
{
  "driver_id": 1,
  "latitude": 28.6139,
  "longitude": 77.2090
}

# Step 5: Receive Trip Notification (via WebSocket/Push)
# (Automatic when trip is requested)

# Step 6: View Trip Details
GET /api/v1/trips/1
```

---

## Error Responses

All services return standard HTTP error codes:

**400 Bad Request:**
```json
{
  "detail": "Email already registered"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Incorrect email or password"
}
```

**404 Not Found:**
```json
{
  "detail": "Trip not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error"
}
```

---

## Authentication

Most endpoints (except signup/login) should include JWT token in headers:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

*(Note: Authentication middleware not yet implemented in MVP)*

---

## Rate Limiting

*(To be implemented in API Gateway)*

---

## WebSocket Events

*(To be implemented for real-time updates)*

Planned events:
- `trip.requested`
- `trip.assigned`
- `trip.started`
- `trip.completed`
- `driver.location.updated`

---

For interactive API testing, visit the Swagger UI for each service at `http://localhost:PORT/docs`.

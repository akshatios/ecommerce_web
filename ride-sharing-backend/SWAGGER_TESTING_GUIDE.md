# 🧪 Complete API Testing Guide - Swagger UI

## 🚀 **Step 1: Start All Services**

```bash
cd d:\New folder (3)\ride-sharing-backend
docker-compose up --build
```

**Wait for all services to start** (2-5 minutes first time)

You'll see messages like:
```
auth_service      | INFO:     Application startup complete.
user_service      | INFO:     Application startup complete.
driver_service    | INFO:     Application startup complete.
...
```

---

## 📍 **Step 2: Access Swagger UI for Each Service**

Open these URLs in your browser:

### **Individual Services (Direct Access)**

| Service | Swagger UI URL | Port |
|---------|---------------|------|
| **Auth Service** | http://localhost:8001/docs | 8001 |
| **User Service** | http://localhost:8002/docs | 8002 |
| **Driver Service** | http://localhost:8003/docs | 8003 |
| **Location Service** | http://localhost:8004/docs | 8004 |
| **Trip Service** | http://localhost:8005/docs | 8005 |
| **Payment Service** | http://localhost:8006/docs | 8006 |
| **Notification Service** | http://localhost:8007/docs | 8007 |
| **Pricing Service** | http://localhost:8008/docs | 8008 |

### **Via API Gateway (Recommended for Production)**

| Service | Gateway URL |
|---------|------------|
| **All Services** | http://localhost/api/v1/* |

---

## 🧪 **Step 3: Complete Testing Flow**

### **Test 1: Auth Service** (http://localhost:8001/docs)

#### **A. Register a Rider**

1. Click on **POST /api/v1/auth/signup**
2. Click **"Try it out"**
3. Enter this JSON:

```json
{
  "email": "rider@test.com",
  "password": "password123",
  "full_name": "Test Rider"
}
```

4. Click **"Execute"**
5. **Expected Response (200)**:

```json
{
  "id": 1,
  "email": "rider@test.com",
  "full_name": "Test Rider",
  "is_active": true,
  "role": "rider"
}
```

#### **B. Login with Email/Password**

1. Click on **POST /api/v1/auth/login**
2. Click **"Try it out"**
3. Enter:
   - **username**: `rider@test.com`
   - **password**: `password123`
4. Click **"Execute"**
5. **Expected Response (200)**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**⚠️ IMPORTANT: Copy the `access_token` - you'll need it for protected endpoints!**

#### **C. Test OTP Login**

1. Click on **POST /api/v1/auth/otp/request**
2. Click **"Try it out"**
3. Enter:

```json
{
  "phone": "+1234567890"
}
```

4. Click **"Execute"**
5. **Check your terminal/console** - you'll see:

```
[OTP] Sending OTP 123456 to +1234567890
```

6. Click on **POST /api/v1/auth/otp/verify**
7. Enter:

```json
{
  "phone": "+1234567890",
  "otp": "123456"
}
```

8. Click **"Execute"**
9. **Expected Response (200)**: Access token + Refresh token

#### **D. Refresh Token**

1. Click on **POST /api/v1/auth/refresh**
2. Enter:

```json
{
  "refresh_token": "paste_your_refresh_token_here"
}
```

3. Click **"Execute"**
4. **Expected Response**: New access token + New refresh token

---

### **Test 2: User Service** (http://localhost:8002/docs)

#### **A. Create Rider Profile**

1. Click on **POST /api/v1/riders**
2. Click **"Try it out"**
3. Enter:

```json
{
  "user_id": 1,
  "phone": "+1234567890"
}
```

4. Click **"Execute"**
5. **Expected Response (200)**:

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

#### **B. Get Rider Details**

1. Click on **GET /api/v1/riders/{rider_id}**
2. Enter **rider_id**: `1`
3. Click **"Execute"**
4. **Expected Response**: Rider details

---

### **Test 3: Driver Service** (http://localhost:8003/docs)

#### **A. Register a Driver**

First, create a driver user in Auth Service:

```json
{
  "email": "driver@test.com",
  "password": "password123",
  "full_name": "Test Driver"
}
```

Then create driver profile:

1. Click on **POST /api/v1/drivers**
2. Enter:

```json
{
  "user_id": 2,
  "license_number": "DL123456789",
  "vehicle": {
    "make": "Toyota",
    "model": "Camry",
    "plate_number": "ABC123",
    "color": "Black"
  }
}
```

3. Click **"Execute"**
4. **Expected Response (200)**:

```json
{
  "id": 1,
  "user_id": 2,
  "license_number": "DL123456789",
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

---

### **Test 4: Location Service** (http://localhost:8004/docs)

#### **A. Update Driver Location**

1. Click on **POST /api/v1/location/update**
2. Enter:

```json
{
  "driver_id": 1,
  "latitude": 28.6139,
  "longitude": 77.2090
}
```

3. Click **"Execute"**
4. **Expected Response (200)**:

```json
{
  "status": "updated"
}
```

#### **B. Find Nearby Drivers**

1. Click on **GET /api/v1/location/nearby**
2. Enter parameters:
   - **latitude**: `28.6139`
   - **longitude**: `77.2090`
   - **radius_km**: `5`
3. Click **"Execute"**
4. **Expected Response (200)**:

```json
{
  "drivers": [
    {
      "driver_id": 1,
      "distance_km": 0.0
    }
  ]
}
```

---

### **Test 5: Pricing Service** (http://localhost:8008/docs)

#### **A. Calculate Fare**

1. Click on **POST /api/v1/pricing/calculate**
2. Enter:

```json
{
  "pickup_lat": 28.6139,
  "pickup_lng": 77.2090,
  "dropoff_lat": 28.7041,
  "dropoff_lng": 77.1025,
  "estimated_time_minutes": 0
}
```

3. Click **"Execute"**
4. **Expected Response (200)**:

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

---

### **Test 6: Trip Service** (http://localhost:8005/docs)

#### **A. Request a Trip**

1. Click on **POST /api/v1/trips/request**
2. Enter:

```json
{
  "rider_id": 1,
  "pickup_lat": 28.6139,
  "pickup_lng": 77.2090,
  "dropoff_lat": 28.7041,
  "dropoff_lng": 77.1025
}
```

3. Click **"Execute"**
4. **Expected Response (200)**:

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

#### **B. Get Trip Details**

1. Click on **GET /api/v1/trips/{trip_id}**
2. Enter **trip_id**: `1`
3. Click **"Execute"**

#### **C. Start Trip**

1. Click on **POST /api/v1/trips/{trip_id}/start**
2. Enter **trip_id**: `1`
3. Click **"Execute"**

#### **D. Complete Trip**

1. Click on **POST /api/v1/trips/{trip_id}/complete**
2. Enter **trip_id**: `1`
3. Click **"Execute"**

---

### **Test 7: Payment Service** (http://localhost:8006/docs)

#### **A. Create Payment**

1. Click on **POST /api/v1/payments**
2. Enter:

```json
{
  "trip_id": 1,
  "rider_id": 1,
  "driver_id": 1,
  "amount": 287.50,
  "method": "CARD"
}
```

3. Click **"Execute"**
4. **Expected Response (200)**:

```json
{
  "id": 1,
  "trip_id": 1,
  "rider_id": 1,
  "driver_id": 1,
  "amount": 287.5,
  "method": "CARD",
  "status": "PENDING",
  "transaction_id": "pi_stub_28750",
  "created_at": "2025-11-27T11:00:00"
}
```

#### **B. Process Payment**

1. Click on **POST /api/v1/payments/{payment_id}/process**
2. Enter **payment_id**: `1`
3. Click **"Execute"**
4. **Expected Response**: Status changed to "COMPLETED"

---

### **Test 8: Notification Service** (http://localhost:8007/docs)

#### **A. Send Push Notification**

1. Click on **POST /api/v1/notifications/send**
2. Enter:

```json
{
  "device_token": "test_device_token_123",
  "title": "New Trip Request",
  "body": "You have a new trip request nearby",
  "data": {
    "trip_id": 1,
    "type": "trip_request"
  }
}
```

3. Click **"Execute"**
4. **Expected Response (200)**:

```json
{
  "status": "sent",
  "message": "FCM stub mode"
}
```

---

## 🌐 **Testing via API Gateway** (http://localhost)

Instead of using individual ports, you can test via the gateway:

```bash
# Auth
http://localhost/api/v1/auth/signup

# Riders
http://localhost/api/v1/riders

# Drivers
http://localhost/api/v1/drivers

# Location
http://localhost/api/v1/location/update

# Trips
http://localhost/api/v1/trips/request

# Payments
http://localhost/api/v1/payments

# Notifications
http://localhost/api/v1/notifications/send

# Pricing
http://localhost/api/v1/pricing/calculate
```

---

## 🔐 **Testing Protected Endpoints (Future)**

When you add authentication middleware to endpoints:

1. Get access token from login
2. Click **"Authorize"** button at top of Swagger UI
3. Enter: `Bearer your_access_token_here`
4. Click **"Authorize"**
5. Now all requests will include the token

---

## 🧪 **Complete Test Sequence**

**Copy-paste this sequence to test the entire flow:**

1. ✅ Register rider → `POST /auth/signup`
2. ✅ Login → `POST /auth/login`
3. ✅ Create rider profile → `POST /riders`
4. ✅ Register driver → `POST /auth/signup`
5. ✅ Create driver profile → `POST /drivers`
6. ✅ Update driver location → `POST /location/update`
7. ✅ Find nearby drivers → `GET /location/nearby`
8. ✅ Calculate fare → `POST /pricing/calculate`
9. ✅ Request trip → `POST /trips/request`
10. ✅ Start trip → `POST /trips/{id}/start`
11. ✅ Complete trip → `POST /trips/{id}/complete`
12. ✅ Create payment → `POST /payments`
13. ✅ Process payment → `POST /payments/{id}/process`
14. ✅ Send notification → `POST /notifications/send`

---

## 🐛 **Troubleshooting**

### **Service not responding?**

```bash
# Check if services are running
docker-compose ps

# Check logs
docker-compose logs -f auth-service
```

### **Database connection error?**

```bash
# Restart database
docker-compose restart db

# Wait for health check
docker-compose ps
```

### **Port already in use?**

```bash
# Stop all containers
docker-compose down

# Start again
docker-compose up
```

---

## 📱 **Testing WebSocket (Advanced)**

Open browser console and run:

```javascript
const ws = new WebSocket('ws://localhost:8005/ws/user_123');

ws.onopen = () => {
  console.log('Connected!');
  ws.send(JSON.stringify({
    type: 'subscribe_trip',
    trip_id: 1
  }));
};

ws.onmessage = (event) => {
  console.log('Received:', JSON.parse(event.data));
};
```

---

## ✅ **Success Indicators**

You'll know everything is working when:

- ✅ All 8 Swagger UIs load
- ✅ Signup returns user ID
- ✅ Login returns access token
- ✅ OTP shows in console
- ✅ Location update succeeds
- ✅ Nearby drivers found
- ✅ Trip gets assigned
- ✅ Payment processes
- ✅ Notifications send

---

**Happy Testing! 🚀**

# 🚀 Quick Start - Backend Testing (Hindi)

## Step 1: Services Start Karo

```bash
cd "d:\New folder (3)\ride-sharing-backend"
docker-compose up --build
```

**Wait karo 2-5 minutes** - Pehli baar thoda time lagega

---

## Step 2: Browser Me Swagger UI Kholo

### **Sabhi Services ke Swagger UI:**

1. **Auth Service**: http://localhost:8001/docs
2. **User Service**: http://localhost:8002/docs
3. **Driver Service**: http://localhost:8003/docs
4. **Location Service**: http://localhost:8004/docs
5. **Trip Service**: http://localhost:8005/docs
6. **Payment Service**: http://localhost:8006/docs
7. **Notification Service**: http://localhost:8007/docs
8. **Pricing Service**: http://localhost:8008/docs

---

## Step 3: Testing Shuru Karo

### **Test 1: User Register Karo**

1. **Auth Service** kholo: http://localhost:8001/docs
2. **POST /api/v1/auth/signup** pe click karo
3. **"Try it out"** button pe click karo
4. Yeh data enter karo:

```json
{
  "email": "test@example.com",
  "password": "password123",
  "full_name": "Test User"
}
```

5. **"Execute"** button pe click karo
6. **Response** me user ID milega

### **Test 2: Login Karo**

1. **POST /api/v1/auth/login** pe click karo
2. **"Try it out"** pe click karo
3. Enter karo:
   - **username**: `test@example.com`
   - **password**: `password123`
4. **"Execute"** pe click karo
5. **Response** me `access_token` milega - **isko copy kar lo!**

### **Test 3: OTP Test Karo**

1. **POST /api/v1/auth/otp/request** pe click karo
2. Enter karo:

```json
{
  "phone": "+1234567890"
}
```

3. **Execute** karo
4. **Terminal/Console** me OTP dikhega (example: `123456`)
5. **POST /api/v1/auth/otp/verify** pe click karo
6. OTP enter karo:

```json
{
  "phone": "+1234567890",
  "otp": "123456"
}
```

7. **Execute** karo - Token milega

### **Test 4: Location Update Karo**

1. **Location Service** kholo: http://localhost:8004/docs
2. **POST /api/v1/location/update** pe click karo
3. Enter karo:

```json
{
  "driver_id": 1,
  "latitude": 28.6139,
  "longitude": 77.2090
}
```

4. **Execute** karo

### **Test 5: Nearby Drivers Dhundo**

1. **GET /api/v1/location/nearby** pe click karo
2. Parameters enter karo:
   - **latitude**: `28.6139`
   - **longitude**: `77.2090`
   - **radius_km**: `5`
3. **Execute** karo
4. Nearby drivers ki list milegi

### **Test 6: Fare Calculate Karo**

1. **Pricing Service** kholo: http://localhost:8008/docs
2. **POST /api/v1/pricing/calculate** pe click karo
3. Enter karo:

```json
{
  "pickup_lat": 28.6139,
  "pickup_lng": 77.2090,
  "dropoff_lat": 28.7041,
  "dropoff_lng": 77.1025
}
```

4. **Execute** karo
5. Total fare milega

### **Test 7: Trip Request Karo**

1. **Trip Service** kholo: http://localhost:8005/docs
2. **POST /api/v1/trips/request** pe click karo
3. Enter karo:

```json
{
  "rider_id": 1,
  "pickup_lat": 28.6139,
  "pickup_lng": 77.2090,
  "dropoff_lat": 28.7041,
  "dropoff_lng": 77.1025
}
```

4. **Execute** karo
5. Trip create hogi aur driver assign hoga

---

## 🎯 **Quick URLs**

**Sabhi Swagger UIs ek saath kholo:**

- Auth: http://localhost:8001/docs
- User: http://localhost:8002/docs
- Driver: http://localhost:8003/docs
- Location: http://localhost:8004/docs
- Trip: http://localhost:8005/docs
- Payment: http://localhost:8006/docs
- Notification: http://localhost:8007/docs
- Pricing: http://localhost:8008/docs

---

## 🔧 **Agar Problem Aaye**

### **Services start nahi ho rahi?**

```bash
# Sab band karo
docker-compose down

# Phir se start karo
docker-compose up --build
```

### **Port already in use?**

```bash
# Pehle sab containers band karo
docker-compose down

# Phir start karo
docker-compose up
```

### **Logs dekhne ke liye:**

```bash
# Sabhi services ke logs
docker-compose logs -f

# Ek specific service ke logs
docker-compose logs -f auth-service
```

---

## ✅ **Sab Kaam Kar Raha Hai Agar:**

- ✅ Sabhi 8 Swagger UIs khul rahe hain
- ✅ Signup karne pe user ID mil raha hai
- ✅ Login karne pe token mil raha hai
- ✅ OTP console me dikh raha hai
- ✅ Location update ho raha hai
- ✅ Nearby drivers mil rahe hain
- ✅ Trip create ho rahi hai
- ✅ Payment process ho raha hai

---

**Testing shuru karo! 🚀**

**Detailed guide ke liye**: `SWAGGER_TESTING_GUIDE.md` file dekho

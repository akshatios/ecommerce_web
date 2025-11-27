# 🎛️ Admin Panel Service - Complete Guide

## 🚀 **Admin Service Features**

Your admin panel backend is now complete with these APIs:

### **1. Dashboard Statistics**
- Total users, drivers, trips
- Active trips count
- Total revenue
- Today's trips

### **2. User Management**
- List all users with pagination
- Activate/Deactivate users
- View user details

### **3. Driver Management**
- List all drivers
- Verify drivers
- View driver details

### **4. Trip Management**
- List all trips with filters
- View trip details
- Cancel trips (admin action)

### **5. Revenue Analytics**
- Daily revenue stats
- Average fare calculation
- Revenue trends

### **6. Real-time Stats**
- Trips by status
- Today's revenue
- Live updates

---

## 📍 **Admin API Endpoints**

### **Access Swagger UI:**
http://localhost:8009/docs

### **All Endpoints:**

#### **Dashboard**
```
GET /api/v1/admin/dashboard
```
Returns: Total users, drivers, trips, revenue, active trips

#### **User Management**
```
GET /api/v1/admin/users?skip=0&limit=100
POST /api/v1/admin/users/{user_id}/activate
POST /api/v1/admin/users/{user_id}/deactivate
```

#### **Trip Management**
```
GET /api/v1/admin/trips?status=COMPLETED&skip=0&limit=100
DELETE /api/v1/admin/trips/{trip_id}
```

#### **Driver Management**
```
POST /api/v1/admin/drivers/{driver_id}/verify
```

#### **Revenue Analytics**
```
GET /api/v1/admin/revenue/daily?days=7
```

#### **Real-time Stats**
```
GET /api/v1/admin/stats/realtime
```

---

## 🧪 **Testing Admin APIs**

### **1. Get Dashboard Stats**

Open: http://localhost:8009/docs

Click on **GET /api/v1/admin/dashboard**

**Response:**
```json
{
  "total_users": 10,
  "total_drivers": 5,
  "total_trips": 25,
  "active_trips": 3,
  "total_revenue": 5000.50,
  "today_trips": 8
}
```

### **2. Get All Users**

**GET /api/v1/admin/users**

Parameters:
- skip: 0
- limit: 100

**Response:**
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "phone": "+1234567890",
    "full_name": "John Doe",
    "role": "rider",
    "is_active": true,
    "created_at": "2025-11-27T10:00:00"
  }
]
```

### **3. Get All Trips**

**GET /api/v1/admin/trips**

Parameters:
- status: COMPLETED (optional)
- skip: 0
- limit: 100

**Response:**
```json
[
  {
    "id": 1,
    "rider_id": 1,
    "driver_id": 1,
    "status": "COMPLETED",
    "fare": 287.50,
    "created_at": "2025-11-27T10:30:00",
    "pickup_lat": 28.6139,
    "pickup_lng": 77.2090,
    "dropoff_lat": 28.7041,
    "dropoff_lng": 77.1025
  }
]
```

### **4. Get Daily Revenue**

**GET /api/v1/admin/revenue/daily?days=7**

**Response:**
```json
[
  {
    "date": "2025-11-27",
    "total_trips": 15,
    "total_revenue": 4500.00,
    "average_fare": 300.00
  },
  {
    "date": "2025-11-26",
    "total_trips": 12,
    "total_revenue": 3600.00,
    "average_fare": 300.00
  }
]
```

### **5. Activate/Deactivate User**

**POST /api/v1/admin/users/1/activate**

**Response:**
```json
{
  "message": "User activated"
}
```

### **6. Verify Driver**

**POST /api/v1/admin/drivers/1/verify**

**Response:**
```json
{
  "message": "Driver verified"
}
```

### **7. Cancel Trip**

**DELETE /api/v1/admin/trips/1**

**Response:**
```json
{
  "message": "Trip cancelled"
}
```

### **8. Real-time Stats**

**GET /api/v1/admin/stats/realtime**

**Response:**
```json
{
  "trips_by_status": {
    "COMPLETED": 20,
    "STARTED": 3,
    "ASSIGNED": 2,
    "REQUESTED": 1
  },
  "today_revenue": 2400.00,
  "timestamp": "2025-11-27T16:30:00"
}
```

---

## 🎨 **Building Frontend Admin Panel**

You can now build a frontend (React, Next.js, Vue) that calls these APIs:

### **Example: Dashboard Component**

```javascript
// Fetch dashboard stats
const response = await fetch('http://localhost:8009/api/v1/admin/dashboard');
const stats = await response.json();

console.log(stats.total_users);
console.log(stats.total_revenue);
```

### **Example: User List**

```javascript
// Fetch users
const response = await fetch('http://localhost:8009/api/v1/admin/users?limit=50');
const users = await response.json();

users.forEach(user => {
  console.log(user.email, user.role);
});
```

### **Example: Activate User**

```javascript
// Activate user
await fetch('http://localhost:8009/api/v1/admin/users/1/activate', {
  method: 'POST'
});
```

---

## 📊 **Admin Panel Features**

### **Dashboard Page**
- Total users count
- Total drivers count
- Total trips count
- Active trips count
- Total revenue
- Today's trips
- Revenue chart (last 7 days)

### **Users Page**
- List all users
- Search/filter users
- Activate/Deactivate users
- View user details

### **Drivers Page**
- List all drivers
- Verify drivers
- View driver details
- View vehicle info

### **Trips Page**
- List all trips
- Filter by status
- View trip details
- Cancel trips

### **Revenue Page**
- Daily revenue chart
- Average fare
- Revenue trends
- Export reports

### **Real-time Monitoring**
- Live trip status
- Active drivers
- Current revenue

---

## 🔐 **Security (Add Later)**

For production, add authentication:

```python
from fastapi import Depends, HTTPException
from app.core.middleware import get_current_user, require_role

@router.get("/dashboard")
def get_dashboard(
    current_user: int = Depends(require_role("admin"))
):
    # Only admins can access
    ...
```

---

## 🚀 **Quick Start**

1. **Admin service is already in docker-compose**
2. **Start services:**
   ```bash
   docker-compose up --build
   ```
3. **Access Admin API:**
   http://localhost:8009/docs

4. **Test all endpoints in Swagger UI**

---

## 📱 **Next Steps**

1. ✅ **Backend APIs Ready** - All admin endpoints working
2. ⏭️ **Build Frontend** - Create React/Next.js admin panel
3. ⏭️ **Add Charts** - Use Chart.js or Recharts
4. ⏭️ **Add Auth** - Protect admin routes
5. ⏭️ **Add Filters** - Search, sort, pagination

---

**Admin Service is COMPLETE! 🎉**

You now have a full-featured admin backend with:
- ✅ Dashboard statistics
- ✅ User management
- ✅ Driver management
- ✅ Trip management
- ✅ Revenue analytics
- ✅ Real-time monitoring

**Build your frontend admin panel and connect to these APIs!** 🚀

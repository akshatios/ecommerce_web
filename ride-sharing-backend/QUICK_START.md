# Ride Sharing Backend - Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Docker Desktop installed and running
- ✅ Docker Compose installed (comes with Docker Desktop)
- ✅ At least 4GB RAM available for Docker
- ✅ Ports 5432, 6379, 8001-8008, 9092 available

## Step 1: Start the Backend

```bash
cd ride-sharing-backend
docker-compose up --build
```

**First-time build will take 5-10 minutes.** Subsequent starts will be faster.

## Step 2: Verify Services are Running

Open your browser and check these URLs (all should show Swagger UI):

1. Auth Service: http://localhost:8001/docs
2. User Service: http://localhost:8002/docs
3. Driver Service: http://localhost:8003/docs
4. Location Service: http://localhost:8004/docs
5. Trip Service: http://localhost:8005/docs
6. Payment Service: http://localhost:8006/docs
7. Notification Service: http://localhost:8007/docs
8. Pricing Service: http://localhost:8008/docs

## Step 3: Test the Complete Flow

### A. Create a Rider

**1. Register User (Auth Service)**
```bash
curl -X POST http://localhost:8001/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "rider@example.com",
    "password": "password123",
    "full_name": "Alice Rider"
  }'
```

**2. Create Rider Profile (User Service)**
```bash
curl -X POST http://localhost:8002/api/v1/riders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "phone": "+1234567890"
  }'
```

### B. Create a Driver

**1. Register Driver User (Auth Service)**
```bash
curl -X POST http://localhost:8001/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "driver@example.com",
    "password": "password123",
    "full_name": "Bob Driver"
  }'
```

**2. Create Driver Profile (Driver Service)**
```bash
curl -X POST http://localhost:8003/api/v1/drivers \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "license_number": "DL123456",
    "vehicle": {
      "make": "Toyota",
      "model": "Camry",
      "plate_number": "ABC123",
      "color": "Black"
    }
  }'
```

**3. Driver Goes Online (Location Service)**
```bash
curl -X POST http://localhost:8004/api/v1/location/update \
  -H "Content-Type: application/json" \
  -d '{
    "driver_id": 1,
    "latitude": 28.6139,
    "longitude": 77.2090
  }'
```

### C. Request a Trip

**1. Get Fare Estimate (Pricing Service)**
```bash
curl -X POST http://localhost:8008/api/v1/pricing/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_lat": 28.6139,
    "pickup_lng": 77.2090,
    "dropoff_lat": 28.7041,
    "dropoff_lng": 77.1025
  }'
```

**2. Request Trip (Trip Service)**
```bash
curl -X POST http://localhost:8005/api/v1/trips/request \
  -H "Content-Type: application/json" \
  -d '{
    "rider_id": 1,
    "pickup_lat": 28.6139,
    "pickup_lng": 77.2090,
    "dropoff_lat": 28.7041,
    "dropoff_lng": 77.1025
  }'
```

**3. Check Trip Status**
```bash
curl http://localhost:8005/api/v1/trips/1
```

### D. Process Payment

**1. Create Payment (Payment Service)**
```bash
curl -X POST http://localhost:8006/api/v1/payments \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 1,
    "rider_id": 1,
    "driver_id": 1,
    "amount": 287.50,
    "method": "CARD"
  }'
```

**2. Process Payment**
```bash
curl -X POST http://localhost:8006/api/v1/payments/1/process
```

## Step 4: Using Swagger UI (Recommended for Testing)

Instead of curl, you can use the interactive Swagger UI:

1. Go to http://localhost:8001/docs (or any service)
2. Click on an endpoint (e.g., POST /api/v1/auth/signup)
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"
6. See the response

## Common Commands

### Start Services
```bash
docker-compose up
```

### Start in Background
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### View Specific Service Logs
```bash
docker-compose logs -f auth-service
```

### Rebuild Services
```bash
docker-compose up --build
```

### Reset Everything (Delete Data)
```bash
docker-compose down -v
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8001 (example)
netstat -ano | findstr :8001

# Kill the process (Windows)
taskkill /PID <PID> /F
```

### Service Won't Start
```bash
# Check logs
docker-compose logs <service-name>

# Example
docker-compose logs auth-service
```

### Database Connection Issues
```bash
# Ensure database is healthy
docker-compose ps

# Restart database
docker-compose restart db
```

### Clear Docker Cache
```bash
docker system prune -a
```

## Database Access

### Connect to PostgreSQL
```bash
docker exec -it ride_sharing_db psql -U postgres -d ride_sharing
```

### Useful SQL Commands
```sql
-- List all tables
\dt

-- View users
SELECT * FROM users;

-- View trips
SELECT * FROM trips;

-- Exit
\q
```

### Connect to Redis
```bash
docker exec -it ride_sharing_redis redis-cli
```

### Useful Redis Commands
```bash
# View all driver locations
GEORADIUS drivers_geo 77.2090 28.6139 100 km WITHDIST

# Get all keys
KEYS *

# Exit
exit
```

## Next Steps

1. ✅ **Test all APIs** using Swagger UI
2. ✅ **Read API_DOCUMENTATION.md** for complete API reference
3. ✅ **Build mobile apps** (React Native) to consume these APIs
4. ✅ **Add API Gateway** (Kong/NGINX) for production
5. ✅ **Implement WebSockets** for real-time updates
6. ✅ **Add monitoring** (Prometheus + Grafana)
7. ✅ **Deploy to cloud** (AWS/GCP/Azure)

## Support

For issues or questions:
1. Check the logs: `docker-compose logs -f`
2. Review API_DOCUMENTATION.md
3. Check PROJECT_SUMMARY.md for architecture details

---

**Happy Coding! 🚀**

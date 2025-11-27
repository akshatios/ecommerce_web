# Ride Sharing Backend - Microservices Architecture

A complete production-ready ride-sharing backend built with **FastAPI microservices**, following industry best practices for scalability, reliability, and maintainability.

## 🏗️ Architecture Overview

```
Mobile Apps (React Native) 
    ↓
API Gateway (Future: Kong/NGINX)
    ↓
┌─────────────────────────────────────────────────────────┐
│                    Microservices                         │
├─────────────────────────────────────────────────────────┤
│ • Auth Service      • User Service     • Driver Service │
│ • Location Service  • Trip Service     • Payment Service│
│ • Notification Svc  • Pricing Service                   │
└─────────────────────────────────────────────────────────┘
    ↓                    ↓                    ↓
PostgreSQL+PostGIS    Redis (Geo)        Kafka (Events)
```

## 📦 Services

| Service | Port | Description |
|---------|------|-------------|
| **Auth Service** | 8001 | User authentication, JWT tokens |
| **User Service** | 8002 | Rider profile management |
| **Driver Service** | 8003 | Driver & vehicle management |
| **Location Service** | 8004 | Real-time location tracking (Redis Geo) |
| **Trip Service** | 8005 | Trip requests, matching, lifecycle |
| **Payment Service** | 8006 | Payment processing (Stripe/Razorpay stub) |
| **Notification Service** | 8007 | Push notifications (FCM/APNs stub) |
| **Pricing Service** | 8008 | Dynamic fare calculation |

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Run All Services

```bash
cd ride-sharing-backend
docker-compose up --build
```

This will start:
- ✅ PostgreSQL with PostGIS (Port 5432)
- ✅ Redis (Port 6379)
- ✅ Kafka + Zookeeper (Port 9092)
- ✅ All 8 microservices (Ports 8001-8008)

### Access Services

- Auth Service: http://localhost:8001/docs
- User Service: http://localhost:8002/docs
- Driver Service: http://localhost:8003/docs
- Location Service: http://localhost:8004/docs
- Trip Service: http://localhost:8005/docs
- Payment Service: http://localhost:8006/docs
- Notification Service: http://localhost:8007/docs
- Pricing Service: http://localhost:8008/docs

Each service has auto-generated **Swagger UI** documentation at `/docs`.

## 📋 API Flow Examples

### 1. User Registration & Login

```bash
# Register a new user
curl -X POST http://localhost:8001/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "rider@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }'

# Login
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=rider@example.com&password=password123"
```

### 2. Create Rider Profile

```bash
curl -X POST http://localhost:8002/api/v1/riders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "phone": "+1234567890"
  }'
```

### 3. Create Driver Profile

```bash
curl -X POST http://localhost:8003/api/v1/drivers \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "license_number": "DL12345",
    "vehicle": {
      "make": "Toyota",
      "model": "Camry",
      "plate_number": "ABC123",
      "color": "Black"
    }
  }'
```

### 4. Update Driver Location

```bash
curl -X POST http://localhost:8004/api/v1/location/update \
  -H "Content-Type: application/json" \
  -d '{
    "driver_id": 1,
    "latitude": 28.6139,
    "longitude": 77.2090
  }'
```

### 5. Find Nearby Drivers

```bash
curl "http://localhost:8004/api/v1/location/nearby?latitude=28.6139&longitude=77.2090&radius_km=5"
```

### 6. Calculate Fare

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

### 7. Request a Trip

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

### 8. Create Payment

```bash
curl -X POST http://localhost:8006/api/v1/payments \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 1,
    "rider_id": 1,
    "driver_id": 1,
    "amount": 250.50,
    "method": "CARD"
  }'
```

## 🗄️ Database Schema

### Auth Service
- **users**: id, email, hashed_password, full_name, is_active

### User Service
- **riders**: id, user_id, phone, wallet_balance, rating

### Driver Service
- **drivers**: id, user_id, license_number, is_verified, rating
- **vehicles**: id, driver_id, make, model, plate_number, color

### Trip Service
- **trips**: id, rider_id, driver_id, pickup_lat/lng, dropoff_lat/lng, status, fare

### Payment Service
- **payments**: id, trip_id, rider_id, driver_id, amount, method, status, transaction_id

### Location Service
- Uses **Redis GEOADD** for real-time driver positions
- Key: `drivers_geo`

## 🔧 Technology Stack

- **Framework**: FastAPI (Python 3.10)
- **Database**: PostgreSQL 15 + PostGIS
- **Cache**: Redis (with Geo support)
- **Message Broker**: Apache Kafka
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Containerization**: Docker & Docker Compose

## 📁 Project Structure

```
ride-sharing-backend/
├── services/
│   ├── auth-service/
│   │   ├── app/
│   │   │   ├── api/v1/        # API routes
│   │   │   ├── core/          # Config, DB, security
│   │   │   ├── models/        # SQLAlchemy models
│   │   │   ├── schemas/       # Pydantic schemas
│   │   │   ├── crud/          # Database operations
│   │   │   └── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── user-service/
│   ├── driver-service/
│   ├── location-service/
│   ├── trip-service/
│   ├── payment-service/
│   ├── notification-service/
│   └── pricing-service/
├── docker-compose.yml
└── README.md
```

## 🔐 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ Token expiration (30 minutes)
- ✅ Database connection pooling
- ✅ Environment variable configuration
- ✅ Health check endpoints

## 🚦 Service Communication

- **Synchronous**: HTTP/REST (via httpx)
- **Asynchronous**: Kafka events (future implementation)
- **Real-time**: WebSocket support (future)

## 📊 Monitoring & Health Checks

Each service exposes:
- `/health` - Health check endpoint
- `/docs` - Swagger UI documentation
- `/openapi.json` - OpenAPI schema

## 🔄 Next Steps (Production Readiness)

### Infrastructure
- [ ] Add API Gateway (Kong/NGINX)
- [ ] Implement service mesh (Istio)
- [ ] Add load balancing
- [ ] Set up Kubernetes deployment
- [ ] Configure auto-scaling

### Observability
- [ ] Add Prometheus metrics
- [ ] Set up Grafana dashboards
- [ ] Implement distributed tracing (Jaeger)
- [ ] Configure centralized logging (ELK/Loki)

### Security
- [ ] Implement refresh tokens
- [ ] Add OTP-based login
- [ ] Set up rate limiting
- [ ] Add API key management
- [ ] Implement RBAC (Role-Based Access Control)

### Features
- [ ] WebSocket support for real-time updates
- [ ] Kafka event consumers
- [ ] Real FCM/APNs integration
- [ ] Stripe/Razorpay payment integration
- [ ] Driver matching algorithm improvements
- [ ] Surge pricing logic
- [ ] Trip history & analytics

### Testing
- [ ] Unit tests for each service
- [ ] Integration tests
- [ ] Load testing (k6/Locust)
- [ ] E2E testing

## 🤝 Contributing

This is a production-grade template. Feel free to:
1. Fork the repository
2. Add features
3. Submit pull requests

## 📝 License

MIT License - feel free to use this for your projects!

## 👨‍💻 Author

Built with ❤️ for scalable ride-sharing platforms.

---

**Note**: This is an MVP backend. For production use, implement proper authentication middleware, add comprehensive error handling, set up monitoring, and follow security best practices.

# Ride Sharing Backend - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   ┌──────────────────┐              ┌──────────────────┐            │
│   │   Rider App      │              │   Driver App     │            │
│   │  (React Native)  │              │  (React Native)  │            │
│   └────────┬─────────┘              └────────┬─────────┘            │
│            │                                  │                      │
└────────────┼──────────────────────────────────┼──────────────────────┘
             │                                  │
             └──────────────┬───────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (Future)                            │
│                    Kong / NGINX / AWS ALB                            │
│                  (Load Balancing, Rate Limiting)                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      MICROSERVICES LAYER                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │Auth Service  │  │User Service  │  │Driver Service│              │
│  │   :8001      │  │   :8002      │  │   :8003      │              │
│  │              │  │              │  │              │              │
│  │• JWT Auth    │  │• Rider       │  │• Driver      │              │
│  │• Signup      │  │  Profile     │  │  Profile     │              │
│  │• Login       │  │• Wallet      │  │• Vehicle     │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                       │
│  ┌──────┴──────────────────┴─────────────────┴────────┐            │
│  │                                                      │            │
│  ▼                  ▼                  ▼               ▼            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │Location Svc  │  │Trip Service  │  │Pricing Svc   │              │
│  │   :8004      │  │   :8005      │  │   :8008      │              │
│  │              │  │              │  │              │              │
│  │• Update Loc  │  │• Request     │  │• Calculate   │              │
│  │• Find Nearby │  │• Matching    │  │  Fare        │              │
│  │• Redis Geo   │  │• Lifecycle   │  │• Haversine   │              │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘              │
│         │                 │                                         │
│  ┌──────┴─────────────────┴──────────┐                             │
│  │                                    │                             │
│  ▼                  ▼                 ▼                             │
│  ┌──────────────┐  ┌──────────────┐                                │
│  │Payment Svc   │  │Notification  │                                │
│  │   :8006      │  │Service :8007 │                                │
│  │              │  │              │                                │
│  │• Process     │  │• Push (FCM)  │                                │
│  │• Stripe/     │  │• WebSocket   │                                │
│  │  Razorpay    │  │  (Future)    │                                │
│  └──────┬───────┘  └──────────────┘                                │
│         │                                                           │
└─────────┼───────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────────────────────────────────────────┐         │
│  │           PostgreSQL + PostGIS (:5432)                 │         │
│  │                                                         │         │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │         │
│  │  │  users   │  │  riders  │  │ drivers  │            │         │
│  │  │  table   │  │  table   │  │ vehicles │            │         │
│  │  └──────────┘  └──────────┘  └──────────┘            │         │
│  │                                                         │         │
│  │  ┌──────────┐  ┌──────────┐                           │         │
│  │  │  trips   │  │ payments │                           │         │
│  │  │  table   │  │  table   │                           │         │
│  │  └──────────┘  └──────────┘                           │         │
│  └────────────────────────────────────────────────────────┘         │
│                                                                       │
│  ┌────────────────────────────────────────────────────────┐         │
│  │              Redis (:6379)                             │         │
│  │                                                         │         │
│  │  • drivers_geo (GEOADD/GEORADIUS)                     │         │
│  │  • Session cache                                       │         │
│  │  • Rate limiting                                       │         │
│  └────────────────────────────────────────────────────────┘         │
│                                                                       │
│  ┌────────────────────────────────────────────────────────┐         │
│  │         Kafka + Zookeeper (:9092)                      │         │
│  │                                                         │         │
│  │  Topics:                                               │         │
│  │  • driver.location.updated                             │         │
│  │  • trip.requested                                      │         │
│  │  • trip.assigned                                       │         │
│  │  • payment.processed                                   │         │
│  └────────────────────────────────────────────────────────┘         │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

## Data Flow: Trip Request

```
1. Rider App
   │
   ├─► POST /api/v1/trips/request
   │   (pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
   │
   ▼
2. Trip Service
   │
   ├─► Create trip record (status: REQUESTED)
   │   Store in PostgreSQL
   │
   ├─► Call Location Service
   │   GET /api/v1/location/nearby?lat=X&lng=Y&radius=5km
   │
   ▼
3. Location Service
   │
   ├─► Query Redis GEORADIUS
   │   Find drivers within 5km
   │
   ├─► Return list of nearby drivers
   │   [driver_id: 1, distance: 2.5km]
   │
   ▼
4. Trip Service
   │
   ├─► Select nearest driver (simple matching)
   │   Update trip: driver_id = 1, status = ASSIGNED
   │
   ├─► (Future) Publish to Kafka
   │   Topic: trip.assigned
   │
   ▼
5. Notification Service (Future)
   │
   ├─► Consume Kafka event
   │   Send push notification to driver
   │
   ▼
6. Driver App
   │
   └─► Receive notification
       Display trip details
```

## Service Dependencies

```
Auth Service
  └─► PostgreSQL

User Service
  └─► PostgreSQL

Driver Service
  └─► PostgreSQL

Location Service
  ├─► Redis (GEOADD, GEORADIUS)
  └─► Kafka (publish location events)

Trip Service
  ├─► PostgreSQL
  ├─► Location Service (HTTP)
  ├─► Redis
  └─► Kafka

Payment Service
  ├─► PostgreSQL
  └─► Stripe/Razorpay API (future)

Notification Service
  ├─► Redis
  ├─► Kafka (consume events)
  └─► FCM/APNs (future)

Pricing Service
  └─► (Stateless - no DB)
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND SERVICES                          │
├─────────────────────────────────────────────────────────────┤
│  Language:        Python 3.10                               │
│  Framework:       FastAPI                                   │
│  Server:          Uvicorn (ASGI)                            │
│  Validation:      Pydantic                                  │
│  ORM:             SQLAlchemy                                │
│  Auth:            JWT (python-jose)                         │
│  Password:        bcrypt (passlib)                          │
│  HTTP Client:     httpx                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DATABASES                                 │
├─────────────────────────────────────────────────────────────┤
│  Primary DB:      PostgreSQL 15 + PostGIS                   │
│  Cache:           Redis (Alpine)                            │
│  Message Broker:  Apache Kafka + Zookeeper                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE                            │
├─────────────────────────────────────────────────────────────┤
│  Containerization: Docker                                   │
│  Orchestration:    Docker Compose                           │
│  Future:           Kubernetes, Helm, Terraform              │
└─────────────────────────────────────────────────────────────┘
```

## Scalability Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                  HORIZONTAL SCALING                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Each service can scale independently:                      │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ Trip Svc │  │ Trip Svc │  │ Trip Svc │                 │
│  │ Instance │  │ Instance │  │ Instance │                 │
│  │    1     │  │    2     │  │    3     │                 │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘                 │
│        └─────────────┼─────────────┘                       │
│                      │                                      │
│                      ▼                                      │
│              ┌───────────────┐                             │
│              │ Load Balancer │                             │
│              └───────────────┘                             │
│                                                              │
│  Shared State:                                              │
│  • PostgreSQL (with read replicas)                         │
│  • Redis (with clustering)                                 │
│  • Kafka (with partitions)                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. API Gateway Layer (Future)                              │
│     • Rate limiting                                         │
│     • DDoS protection                                       │
│     • IP whitelisting                                       │
│                                                              │
│  2. Authentication Layer                                    │
│     • JWT tokens (30 min expiry)                           │
│     • Password hashing (bcrypt)                            │
│     • Refresh tokens (future)                              │
│                                                              │
│  3. Authorization Layer (Future)                            │
│     • RBAC (rider, driver, admin)                          │
│     • Endpoint-level permissions                           │
│                                                              │
│  4. Data Layer                                              │
│     • Encrypted connections (TLS)                          │
│     • Encrypted at rest                                    │
│     • PII protection                                       │
│                                                              │
│  5. Network Layer                                           │
│     • VPC isolation                                        │
│     • Private subnets for databases                        │
│     • Security groups                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Monitoring & Observability (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY STACK                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Metrics: Prometheus                                        │
│  ├─► Scrape /metrics from each service                     │
│  ├─► Store time-series data                                │
│  └─► Alert on thresholds                                   │
│                                                              │
│  Visualization: Grafana                                     │
│  ├─► Dashboards for each service                           │
│  ├─► Real-time metrics                                     │
│  └─► Custom alerts                                         │
│                                                              │
│  Tracing: Jaeger                                            │
│  ├─► Distributed tracing                                   │
│  ├─► Request flow visualization                            │
│  └─► Performance bottlenecks                               │
│                                                              │
│  Logging: ELK Stack / Loki                                  │
│  ├─► Centralized log aggregation                           │
│  ├─► Log search & analysis                                 │
│  └─► Error tracking                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

This architecture is designed for:
- ✅ **Scalability**: Each service scales independently
- ✅ **Reliability**: Fault isolation, health checks
- ✅ **Maintainability**: Clear separation of concerns
- ✅ **Performance**: Redis for fast geo-queries, Kafka for async
- ✅ **Security**: JWT auth, encrypted data, rate limiting

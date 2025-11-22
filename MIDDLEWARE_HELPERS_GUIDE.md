# 🛠️ Middleware & Helper Functions Guide

## 📁 New Folder Structure

```
app/
├── middleware/                    # ✨ NEW: Middleware modules
│   ├── __init__.py
│   ├── allowedHostsMiddleware.py
│   ├── checkUserExistsMiddleware.py
│   ├── timeMeasureMiddleware.py
│   └── tokenAuthentication.py
│
└── helper_function/               # ✨ NEW: Helper utilities
    ├── __init__.py
    ├── apis_requests.py
    ├── Creating_and_Verifing_Password.py
    └── tokenCreator.py
```

---

## 🔒 Middleware Documentation

### 1. **allowedHostsMiddleware.py**

**Purpose**: Prevent host header injection attacks

**Features**:
- ✅ Validates incoming request hosts
- ✅ Configurable allowed hosts list
- ✅ Wildcard support for development

**Usage**:
```python
from app.middleware.allowedHostsMiddleware import AllowedHostsMiddleware

app.add_middleware(
    AllowedHostsMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "yourdomain.com"]
)
```

**Example**:
```python
# Allow all hosts (development)
app.add_middleware(AllowedHostsMiddleware, allowed_hosts=["*"])

# Production - specific hosts only
app.add_middleware(
    AllowedHostsMiddleware,
    allowed_hosts=[
        "ecommerce-web-vpma.onrender.com",
        "ecommerce-web-lemon.vercel.app"
    ]
)
```

---

### 2. **checkUserExistsMiddleware.py**

**Purpose**: Verify authenticated users still exist in database

**Features**:
- ✅ Checks user existence for protected routes
- ✅ Validates user is active
- ✅ Configurable excluded paths
- ✅ Prevents deleted user access

**Usage**:
```python
from app.middleware.checkUserExistsMiddleware import CheckUserExistsMiddleware

app.add_middleware(CheckUserExistsMiddleware)
```

**Custom excluded paths**:
```python
app.add_middleware(
    CheckUserExistsMiddleware,
    excluded_paths=["/", "/health", "/docs", "/register", "/login"]
)
```

---

### 3. **timeMeasureMiddleware.py**

**Purpose**: Measure and log request processing time

**Features**:
- ✅ Logs all request processing times
- ✅ Adds `X-Process-Time` header to responses
- ✅ Warns on slow requests
- ✅ Configurable slow request threshold

**Usage**:
```python
from app.middleware.timeMeasureMiddleware import TimeMeasureMiddleware

app.add_middleware(
    TimeMeasureMiddleware,
    log_slow_requests=True,
    slow_threshold=1.0  # seconds
)
```

**Output Example**:
```
INFO: GET /products - Status: 200 - Time: 0.0234s
WARNING: ⚠️  SLOW REQUEST: POST /orders - Status: 201 - Time: 1.2456s
```

---

### 4. **tokenAuthentication.py**

**Purpose**: JWT token authentication middleware

**Features**:
- ✅ Validates JWT tokens
- ✅ Attaches user to request state
- ✅ Configurable excluded paths
- ✅ Bearer token support

**Usage**:
```python
from app.middleware.tokenAuthentication import TokenAuthenticationMiddleware

app.add_middleware(TokenAuthenticationMiddleware)
```

**Access user in routes**:
```python
@router.get("/profile")
def get_profile(request: Request):
    user = request.state.user
    return {"username": user["username"]}
```

---

## 🔧 Helper Functions Documentation

### 1. **apis_requests.py**

**Purpose**: Make external API requests

**Features**:
- ✅ Async HTTP client
- ✅ GET, POST, PUT, DELETE methods
- ✅ Header management
- ✅ Token authentication support
- ✅ Error handling

**Usage**:
```python
from app.helper_function.apis_requests import APIRequest

# Initialize
api = APIRequest(base_url="https://api.example.com")

# Set auth token
api.set_auth_token("your_token_here")

# Make requests
result = await api.get("/users", params={"page": 1})
result = await api.post("/users", json_data={"name": "John"})
result = await api.put("/users/1", json_data={"name": "Jane"})
result = await api.delete("/users/1")
```

**Example - External API Integration**:
```python
# Payment gateway integration
payment_api = APIRequest(base_url="https://payment.gateway.com")
payment_api.set_header("API-Key", "your_api_key")

result = await payment_api.post(
    "/charge",
    json_data={
        "amount": 1000,
        "currency": "USD",
        "customer_id": "cust_123"
    }
)
```

---

### 2. **Creating_and_Verifing_Password.py**

**Purpose**: Password hashing and validation

**Features**:
- ✅ Bcrypt password hashing
- ✅ Password verification
- ✅ Strength validation (strict & simple)
- ✅ Create and verify in one step

**Usage**:
```python
from app.helper_function.Creating_and_Verifing_Password import PasswordManager

# Hash password
hashed = PasswordManager.hash_password("MyPassword123!")

# Verify password
is_valid = PasswordManager.verify_password("MyPassword123!", hashed)

# Validate password strength
is_valid, message = PasswordManager.validate_password_strength("weak")
# Returns: (False, "Password must be at least 8 characters long")

# Create and verify in one step
is_valid, message, hashed = PasswordManager.create_and_verify(
    "MyPassword123!",
    use_strict_validation=True
)
```

**Password Requirements (Strict)**:
- ✅ At least 8 characters
- ✅ One uppercase letter
- ✅ One lowercase letter
- ✅ One digit
- ✅ One special character

**Example in Registration**:
```python
@router.post("/register")
def register(user: UserCreate):
    # Validate password
    is_valid, message, hashed = PasswordManager.create_and_verify(
        user.password,
        use_strict_validation=True
    )
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    # Save user with hashed password
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed
    }
    db.users.insert_one(new_user)
```

---

### 3. **tokenCreator.py**

**Purpose**: JWT token creation and verification

**Features**:
- ✅ Access token creation
- ✅ Refresh token creation
- ✅ Token verification
- ✅ Expiry checking
- ✅ Random token generation

**Usage**:
```python
from app.helper_function.tokenCreator import TokenCreator

# Initialize
token_creator = TokenCreator()

# Create access token (30 min expiry)
access_token = token_creator.create_access_token({"sub": "username"})

# Create refresh token (7 days expiry)
refresh_token = token_creator.create_refresh_token({"sub": "username"})

# Verify token
payload = token_creator.verify_token(access_token)
if payload:
    username = payload["sub"]

# Check if expired
is_expired = token_creator.is_token_expired(access_token)

# Get expiry time
expiry = token_creator.get_token_expiry(access_token)

# Generate random token (for password reset)
reset_token = TokenCreator.generate_random_token(length=32)
```

**Example - Login with Refresh Token**:
```python
@router.post("/login")
def login(credentials: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_creator = TokenCreator()
    
    # Create both tokens
    access_token = token_creator.create_access_token({"sub": user["username"]})
    refresh_token = token_creator.create_refresh_token({"sub": user["username"]})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

---

## 🚀 Complete Integration Example

### Update `main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.routes import register_routes

# Import middlewares
from app.middleware.timeMeasureMiddleware import TimeMeasureMiddleware
from app.middleware.allowedHostsMiddleware import AllowedHostsMiddleware
from app.middleware.checkUserExistsMiddleware import CheckUserExistsMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middlewares
app.add_middleware(TimeMeasureMiddleware, log_slow_requests=True, slow_threshold=1.0)
app.add_middleware(AllowedHostsMiddleware, allowed_hosts=["*"])
app.add_middleware(CheckUserExistsMiddleware)

# Register routes
register_routes(app)
```

---

## 📊 Middleware Execution Order

**Important**: Middlewares execute in reverse order of addition!

```
Request Flow:
1. TimeMeasureMiddleware (starts timer)
2. AllowedHostsMiddleware (checks host)
3. CheckUserExistsMiddleware (validates user)
4. Your Route Handler
5. CheckUserExistsMiddleware (response)
6. AllowedHostsMiddleware (response)
7. TimeMeasureMiddleware (adds time header)
```

---

## 🧪 Testing Examples

### Test Password Manager:
```python
from app.helper_function.Creating_and_Verifing_Password import PasswordManager

# Test hashing
password = "TestPass123!"
hashed = PasswordManager.hash_password(password)
print(f"Hashed: {hashed}")

# Test verification
is_valid = PasswordManager.verify_password("TestPass123!", hashed)
print(f"Valid: {is_valid}")  # True

# Test strength validation
is_valid, message = PasswordManager.validate_password_strength("weak")
print(f"Valid: {is_valid}, Message: {message}")
```

### Test Token Creator:
```python
from app.helper_function.tokenCreator import TokenCreator

token_creator = TokenCreator()

# Create token
token = token_creator.create_access_token({"sub": "testuser"})
print(f"Token: {token}")

# Verify token
payload = token_creator.verify_token(token)
print(f"Payload: {payload}")

# Check expiry
is_expired = token_creator.is_token_expired(token)
print(f"Expired: {is_expired}")  # False
```

### Test API Requests:
```python
from app.helper_function.apis_requests import APIRequest

api = APIRequest(base_url="https://jsonplaceholder.typicode.com")

# Test GET
result = await api.get("/posts/1")
print(result)

# Test POST
result = await api.post("/posts", json_data={"title": "Test", "body": "Content"})
print(result)
```

---

## 📝 Best Practices

### 1. **Middleware Order**
```python
# Correct order (most specific last)
app.add_middleware(TimeMeasureMiddleware)      # Logging
app.add_middleware(AllowedHostsMiddleware)     # Security
app.add_middleware(CheckUserExistsMiddleware)  # Authentication
```

### 2. **Password Validation**
```python
# Use strict validation for production
is_valid, message, hashed = PasswordManager.create_and_verify(
    password,
    use_strict_validation=True  # Enforce strong passwords
)
```

### 3. **Token Expiry**
```python
# Short-lived access tokens
access_token = token_creator.create_access_token(
    {"sub": username},
    expires_delta=timedelta(minutes=15)
)

# Long-lived refresh tokens
refresh_token = token_creator.create_refresh_token(
    {"sub": username},
    expires_delta=timedelta(days=30)
)
```

---

## 🎯 Summary

| Module | Purpose | Key Feature |
|--------|---------|-------------|
| `allowedHostsMiddleware` | Security | Host validation |
| `checkUserExistsMiddleware` | Auth | User validation |
| `timeMeasureMiddleware` | Monitoring | Performance tracking |
| `tokenAuthentication` | Auth | JWT validation |
| `apis_requests` | Integration | External API calls |
| `Creating_and_Verifing_Password` | Security | Password management |
| `tokenCreator` | Auth | Token generation |

---

**All modules are production-ready and fully documented!** 🎉

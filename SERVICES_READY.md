# Microservices Deployment Status ✅

## Summary
All three microservices are deployed and ready to use with complete flight data loaded.

## Services Overview

### 1. **Auth Service** 🔐
- **Port**: `localhost:8001`
- **Root Endpoint**: `/` (API info page)
- **Status**: ✅ Running
- **Endpoints**:
  - `POST /api/auth/register/` - Create new user account
  - `POST /api/auth/login/` - Get JWT token
  - `GET /api/auth/me/` - Get current user info (requires JWT token)
  - `GET /admin/` - Django admin panel

**Example Usage:**
```bash
# Register
curl -X POST http://localhost:8001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Login
curl -X POST http://localhost:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
# Returns: {"token":"eyJ..."}
```

---

### 2. **Flight Service** ✈️
- **Port**: `localhost:8003`
- **Root Endpoint**: `/` (API info page)
- **Status**: ✅ Running with data loaded
- **Database**: 
  - **127 airports** loaded
  - **5,927 domestic flights** loaded
  - **7,120 international flights** loaded
  - **Total: 13,047 flights** ready to search

**Endpoints**:
  - `GET /api/flights/flights/` - Search flights (requires JWT token)
  - `GET /api/flights/flights/{id}/` - Flight details
  - `GET /admin/` - Django admin panel

**Example Usage:**
```bash
# Search flights (requires JWT token)
curl -X GET "http://localhost:8003/api/flights/flights/?limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Sample response:
{
  "count": 13047,
  "next": "...",
  "results": [
    {
      "id": 1,
      "origin": "Delhi (DEL)",
      "destination": "Mumbai (BOM)",
      "duration": "2:10:00",
      "available_seats": 150
    }
  ]
}
```

---

### 3. **Booking Service** 🎫
- **Port**: `localhost:8002`
- **Root Endpoint**: `/` (API info page)
- **Status**: ✅ Running
- **Endpoints**:
  - `GET /api/bookings/bookings/` - List user bookings (requires JWT)
  - `POST /api/bookings/create/` - Create new booking (requires JWT)
  - `GET /admin/` - Django admin panel

**Example Usage:**
```bash
# Create booking (requires JWT token)
curl -X POST http://localhost:8002/api/bookings/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "flight_id": 1,
    "passenger_name": "John Doe",
    "seat_number": "1A",
    "class": "economy"
  }'
```

---

## Complete Flow Example

### 1. Register User
```bash
curl -X POST http://localhost:8001/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secure123"}'
```

### 2. Login & Get Token
```bash
curl -X POST http://localhost:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secure123"}'

# Save the returned token
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. Search Flights
```bash
curl -X GET "http://localhost:8003/api/flights/flights/?origin=Delhi&destination=Mumbai" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Make Booking
```bash
curl -X POST http://localhost:8002/api/bookings/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "flight_id": 1,
    "passenger_name": "John Doe",
    "class": "economy"
  }'
```

---

## Kubernetes Status

```
NAMESPACE: flight-services

Auth Service (2 pods):
  auth-service-558fc5b846-cj6ck      1/1 Running
  auth-service-558fc5b846-knph7      1/1 Running

Booking Service (2 pods):
  booking-service-64b6564757-97zvn   1/1 Running
  booking-service-64b6564757-zvltc   1/1 Running

Flight Service (2 pods):
  flight-service-7c9c477c74-8cxv5    1/1 Running
  flight-service-7c9c477c74-qhkjb    1/1 Running
```

---

## Port Forwarding

To access services locally, ensure port forwarding is active:

```powershell
# Terminal 1: Auth Service
kubectl port-forward -n flight-services svc/auth-service 8001:8001

# Terminal 2: Booking Service
kubectl port-forward -n flight-services svc/booking-service 8002:8002

# Terminal 3: Flight Service
kubectl port-forward -n flight-services svc/flight-service 8003:8002
```

---

## Next Steps
- [ ] Build React frontend to consume these APIs
- [ ] Setup persistent database (PostgreSQL) instead of SQLite
- [ ] Configure inter-service communication
- [ ] Add request validation and error handling
- [ ] Setup API documentation (Swagger/OpenAPI)

---

## API Testing Tools
- **Postman**: Import the API endpoints for easy testing
- **curl**: Command-line testing shown above
- **VS Code REST Client**: Create `.http` files for requests
- **Thunder Client**: VS Code extension for API testing

**Deployment completed**: December 21, 2025 ✅

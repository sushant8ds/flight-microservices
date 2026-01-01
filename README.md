# Flight Microservices

A microservices-based flight booking system with authentication, booking, and flight management services.

## Architecture

- **Auth Service** (Port 8001) - User authentication and authorization
- **Booking Service** (Port 8002) - Booking management
- **Flight Service** (Port 8002) - Flight information and management

## Prerequisites

- Docker and Docker Desktop
- Kubernetes (Minikube for local development or cloud cluster)
- kubectl CLI
- Python 3.12+

## Local Development with Docker Compose

### 1. Build and Run Services

```bash
docker-compose up --build
```

This will start all three services:
- Auth Service: http://localhost:8001
- Booking Service: http://localhost:8002
- Flight Service: http://localhost:8003

### 2. Stop Services

```bash
docker-compose down
```

## Kubernetes Deployment

### Option 1: Using the Deploy Script (Recommended)

```bash
# Make the script executable (Linux/Mac)
chmod +x deploy.sh

# Run the deployment
./deploy.sh
```

### Option 2: Manual Deployment

#### 1. Set up Docker Images

```bash
# Build images locally
docker build -t sushant8ds/auth-service:latest ./auth-service
docker build -t sushant8ds/booking-service:latest ./booking-service
docker build -t sushant8ds/flight-service:latest ./flight-service

# Or push to registry (if using Docker Hub)
# docker push sushant8ds/auth-service:latest
# docker push sushant8ds/booking-service:latest
# docker push sushant8ds/flight-service:latest
```

#### 2. Create Namespace and Deploy

```bash
# Create namespace
kubectl create namespace flight-services

# Apply all deployments at once
kubectl apply -f k8s/all-services.yaml

# Or apply individually
kubectl apply -f k8s/auth-deployment.yaml -n flight-services
kubectl apply -f k8s/booking-deployment.yaml -n flight-services
kubectl apply -f k8s/flight-deployment.yaml -n flight-services
```

#### 3. Verify Deployment

```bash
# Check deployments
kubectl get deployments -n flight-services

# Check services
kubectl get services -n flight-services

# Check pods
kubectl get pods -n flight-services

# View logs
kubectl logs -n flight-services deployment/auth-service
kubectl logs -n flight-services deployment/booking-service
kubectl logs -n flight-services deployment/flight-service
```

### Port Forwarding (Local Access)

```bash
# Terminal 1: Forward Auth Service
kubectl port-forward -n flight-services svc/auth-service 8001:8001

# Terminal 2: Forward Booking Service
kubectl port-forward -n flight-services svc/booking-service 8002:8002

# Terminal 3: Forward Flight Service
kubectl port-forward -n flight-services svc/flight-service 8002:8002
```

Then access:
- Auth Service: http://localhost:8001
- Booking Service: http://localhost:8002
- Flight Service: http://localhost:8003

## Configuration

### Environment Variables

Update these in the deployment files as needed:

- `DEBUG` - Set to 0 for production
- `ALLOWED_HOSTS` - Configure allowed hosts
- `SECRET_KEY` - Django secret key (must be set in production)

### Database Configuration

Current setup uses SQLite. For production, configure:

```yaml
DATABASES:
  default:
    ENGINE: django.db.backends.postgresql
    NAME: microservice_db
    USER: postgres
    PASSWORD: <password>
    HOST: postgres-service
    PORT: 5432
```

## Service Communication

Services communicate via Kubernetes Service DNS:

```python
# From booking-service to auth-service
auth_url = "http://auth-service:8001"

# From flight-service to booking-service
booking_url = "http://booking-service:8002"
```

## Scaling

Increase replicas:

```bash
kubectl scale deployment auth-service --replicas=3 -n flight-services
kubectl scale deployment booking-service --replicas=3 -n flight-services
kubectl scale deployment flight-service --replicas=3 -n flight-services
```

## Cleanup

```bash
# Delete all deployments
kubectl delete namespace flight-services

# Or delete individual services
kubectl delete -f k8s/all-services.yaml
```

## Troubleshooting

### Pods not starting

```bash
kubectl describe pod <pod-name> -n flight-services
kubectl logs <pod-name> -n flight-services
```

### Image pull errors

- Ensure images are built locally or pushed to registry
- Check image names in deployment files match your registry
- Update `imagePullPolicy` in deployments

### Port already in use

Change port mappings in port-forward or service definitions

### Service discovery issues

- Verify services are in the same namespace
- Check service DNS: `kubectl exec -it <pod> -n flight-services -- nslookup auth-service`

## Next Steps

1. Add database services (PostgreSQL)
2. Set up Ingress for external access
3. Configure persistent volumes for data
4. Add health check endpoints
5. Implement logging and monitoring (ELK, Prometheus)
6. Set up CI/CD pipeline

# Kubernetes Deployment - Flight Microservices

## ✅ Deployment Status

Successfully deployed to Kubernetes:

### Running Services ✅

| Service | Status | Replicas | Port | Cluster IP |
|---------|--------|----------|------|------------|
| Booking Service | ✅ Running | 2/2 | 8002 | 10.110.183.26:8002 |
| Flight Service | ✅ Running | 2/2 | 8002 | 10.104.0.121:8002 |

### Local Access (Port Forwarding)

Port forwarding is active:
- **Booking Service**: `http://localhost:8002`
- **Flight Service**: `http://localhost:8003`

## Test the Services

```bash
# Test Booking Service
curl http://localhost:8002/

# Test Flight Service
curl http://localhost:8003/
```

## Verify Deployment

```bash
# Check pods
kubectl get pods -n flight-services

# Check services
kubectl get services -n flight-services

# View logs
kubectl logs -n flight-services deployment/booking-service
kubectl logs -n flight-services deployment/flight-service

# Check resource usage
kubectl top pods -n flight-services
```

## Scaling Services

```bash
# Scale booking service to 3 replicas
kubectl scale deployment booking-service --replicas=3 -n flight-services

# Scale flight service to 4 replicas
kubectl scale deployment flight-service --replicas=4 -n flight-services
```

## Port Forwarding Commands

If port forwarding stops, restart with:

```powershell
# Booking Service
kubectl port-forward -n flight-services svc/booking-service 8002:8002

# Flight Service  
kubectl port-forward -n flight-services svc/flight-service 8003:8002
```

## Service Communication (Internal)

Services can communicate via Kubernetes DNS:

```python
# From flight-service to booking-service (within cluster)
booking_url = "http://booking-service:8002"

# External (via port-forward)
booking_url = "http://localhost:8002"
```

## Next Steps

1. Fix auth-service Django settings (remove corsheaders dependency or install it)
2. Add database services (PostgreSQL)
3. Implement inter-service communication
4. Set up Ingress for external access
5. Add monitoring and logging (Prometheus, ELK)
6. Configure CI/CD pipeline

## Troubleshooting

### Services not responding

```bash
# Check if pods are running
kubectl get pods -n flight-services

# Check pod logs
kubectl logs -n flight-services <pod-name>

# Describe pod for events
kubectl describe pod -n flight-services <pod-name>
```

### Port already in use

Kill the port-forward process and restart:

```powershell
# Find and kill port forwarding process
Get-Process | Where-Object {$_.ProcessName -like "*kubectl*"} | Stop-Process -Force

# Restart port forwarding
kubectl port-forward -n flight-services svc/booking-service 8002:8002
```

---

**Deployment Date**: 21 Dec 2025  
**Cluster**: Minikube  
**Namespace**: flight-services

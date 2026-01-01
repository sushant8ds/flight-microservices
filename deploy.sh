#!/bin/bash

# Flight Microservices Kubernetes Deployment Script
# This script deploys all microservices to Kubernetes

set -e

echo "🚀 Starting Flight Microservices Deployment..."

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if minikube is running (optional - for local development)
if command -v minikube &> /dev/null; then
    echo "✓ Setting Docker context to minikube..."
    eval $(minikube docker-env)
fi

echo ""
echo "📦 Building Docker Images..."

# Build images
docker build -t sushant8ds/auth-service:latest ./auth-service
docker build -t sushant8ds/booking-service:latest ./booking-service
docker build -t sushant8ds/flight-service:latest ./flight-service

echo "✓ Docker images built successfully"

echo ""
echo "☸️  Applying Kubernetes Manifests..."

# Create namespace
kubectl create namespace flight-services || true
echo "✓ Namespace created/exists"

# Apply deployments
kubectl apply -f k8s/auth-deployment.yaml -n flight-services
kubectl apply -f k8s/booking-deployment.yaml -n flight-services
kubectl apply -f k8s/flight-deployment.yaml -n flight-services
echo "✓ All services deployed"

echo ""
echo "📊 Deployment Status..."
kubectl get deployments -n flight-services
kubectl get services -n flight-services

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "Access your services:"
echo "  - Auth Service: http://auth-service:8001"
echo "  - Booking Service: http://booking-service:8002"
echo "  - Flight Service: http://flight-service:8002"
echo ""
echo "To port-forward and access locally:"
echo "  kubectl port-forward -n flight-services svc/auth-service 8001:8001"
echo "  kubectl port-forward -n flight-services svc/booking-service 8002:8002"

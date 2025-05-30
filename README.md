# Task Service Deployment to Azure Kubernetes

## Step 1: Build Docker Image

```bash
docker build -t task-service .
```

## Step 2: Push to Registry

```bash
docker tag task-service <registry>/task-service:latest
docker push <registry>/task-service:latest
```

## Step 3: Apply Kubernetes Manifests

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## What’s missing / next steps

- Replace <registry> in `deployment.yaml` with the actual registry name
- Wait for team confirmation (Azure / GCP) before deploying
- Integrate with service discovery / ingress when infrastructure is ready


## Notes

- Ensure your AKS cluster is running and kubectl is configured.
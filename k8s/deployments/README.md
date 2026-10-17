# Kubernetes Deployments with Minikube

This example runs three `demo-app` replicas using a rolling-update strategy,
with readiness and liveness probes on port `5000`.

## Build and publish

```shell
docker build . -t sazzadr/demo-app:v2
docker push sazzadr/demo-app:v2
```

## Deploy

```shell
minikube start
kubectl apply -f k8s.yaml
kubectl rollout status deployment/demo-app
kubectl get pods -l app=demo-app
```

Forward a local port to one of the replicas and test it:

```shell
kubectl port-forward deployment/demo-app 5000:5000
```

```shell
curl http://localhost:5000
```

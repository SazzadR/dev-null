# Kubernetes Services with Minikube

This example runs three `demo-app` replicas behind a NodePort Service and an
NGINX pod behind an internal ClusterIP Service.

## Build and publish

```shell
docker build . -t sazzadr/demo-app:v5
docker push sazzadr/demo-app:v5
```

## Deploy

```shell
minikube start
kubectl apply -f k8s.yaml
kubectl get pods,services
kubectl get endpoints demo-app-service nginx-service
```

Open the demo app through its Service:

```shell
minikube service demo-app-service --url
```

Use the printed URL with `curl` or a browser. The Service routes new network
connections across the ready demo-app pods. `kubectl port-forward` selects one
pod, so it should not be used to check load distribution.

## Test in-cluster Service discovery

From a demo-app pod, access NGINX by its Kubernetes Service name:

```shell
kubectl exec deployment/demo-app-deployment -- curl http://nginx-service:80
```

This works because Kubernetes DNS resolves `nginx-service`, and the Service
forwards the request to the NGINX pod.

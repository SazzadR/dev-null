# Kubernetes Pods with Minikube

This example runs a single Apache HTTP Server pod.

## Deploy

```shell
minikube start
kubectl apply -f k8s.yaml
kubectl get pod apache
```

Forward a local port to the pod and test it:

```shell
kubectl port-forward pod/apache 8080:80
```

```shell
curl http://localhost:8080
```

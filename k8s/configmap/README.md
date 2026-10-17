# Kubernetes ConfigMap with Traefik and Minikube

This example uses host-based Traefik rules to route `nginx.local.dev/` to an
NGINX Service and `api.local.dev/api` to three `demo-app` replicas. A ConfigMap
provides the `MESSAGE` environment variable used by the demo application.

## Build and publish

```shell
docker build . -t sazzadr/demo-app:v7
docker push sazzadr/demo-app:v7
```

## Deploy

```shell
minikube start
minikube addons disable ingress
minikube addons enable traefik
kubectl apply -f k8s.yaml
kubectl rollout status deployment/demo-app-deployment
kubectl rollout status deployment/nginx-deployment
kubectl get configmap,pods,services,ingress
kubectl get ingressclass
```

The Ingress should use the `traefik` class. The NGINX ingress add-on is disabled
because it cannot run alongside the Traefik add-on on ports `80` and `443`.

## Test the Ingress

Forward a local port to Traefik and keep the command running:

```shell
kubectl --namespace kube-system port-forward service/traefik 8080:80
```

From another terminal, test both routes:

```shell
curl --header "Host: nginx.local.dev" http://127.0.0.1:8080/
curl --header "Host: api.local.dev" http://127.0.0.1:8080/api
```

The `Host` header selects the matching Ingress rule. The first request returns
the NGINX welcome page, while the second returns the demo application response
with its pod hostname, for example:

```text
[v6] ConfigMap is working! Host: demo-app-deployment-...
```

## Update the ConfigMap

Change `MESSAGE` in `k8s.yaml`, apply it, and restart the Deployment because
ConfigMap values injected as environment variables do not update running pods:

```shell
kubectl apply -f k8s.yaml
kubectl rollout restart deployment/demo-app-deployment
kubectl rollout status deployment/demo-app-deployment
curl --header "Host: api.local.dev" http://127.0.0.1:8080/api
```

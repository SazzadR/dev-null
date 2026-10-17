# Kubernetes Secrets with Traefik and Minikube

This example injects ConfigMap and Secret values into three `demo-app` replicas.
Traefik routes `nginx.local.dev/` to NGINX and `api.local.dev/api` to the app.

## Build and publish

```shell
docker build . -t sazzadr/demo-app:v8
docker push sazzadr/demo-app:v8
```

## Start Minikube

```shell
minikube start
minikube addons disable ingress
minikube addons enable traefik
```

## Create the Secret

Copy the safe example, replace `<change-this>`, and keep the resulting file
local. `k8s-secrets.yaml` is excluded by `.gitignore`.

```shell
cp k8s-secrets.example.yaml k8s-secrets.yaml
kubectl apply -f k8s-secrets.yaml
```

## Deploy

```shell
kubectl apply -f k8s.yaml
kubectl rollout status deployment/demo-app-deployment
kubectl rollout status deployment/nginx-deployment
kubectl get configmap,secret,pods,services,ingress
```

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

The second response includes the ConfigMap value, Secret value, and pod
hostname:

```text
[v8] ConfigMap: ConfigMap is working!, Secret: <your-secret>, Host: demo-app-deployment-...
```

## Update the Secret

After changing `k8s-secrets.yaml`, apply it and restart the Deployment. Secret
values injected as environment variables do not update running containers.

```shell
kubectl apply -f k8s-secrets.yaml
kubectl rollout restart deployment/demo-app-deployment
kubectl rollout status deployment/demo-app-deployment
```

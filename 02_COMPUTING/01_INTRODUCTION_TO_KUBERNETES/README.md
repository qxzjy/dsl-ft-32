# Getting started
1. Start/create cluster :
```shell
minikube start
```

2. Load deployment configuration : 
```shell
kubectl apply -f mlflow-deployment.yaml

# If using a Kubernetes Secrets file
kubectl apply -f mlflow-deployment-with-secrets-file.yaml
```

3. Load service configuration :
```shell
kubectl apply -f mlflow-service.yaml
```

4. Load secrets configuration :
```shell
# If using a Kubernetes Secrets file
kubectl apply -f secrets.yaml
```

5. Launch service :
```shell
minikube service mlflow-service
```

6. Stop cluster :
```shell
minikube stop
```

7. Delete cluster :
```shell
minikube delete
```

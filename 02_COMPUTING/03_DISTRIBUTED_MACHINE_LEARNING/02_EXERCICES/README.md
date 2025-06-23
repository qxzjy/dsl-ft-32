In case the local ray cluster is still in use, let's stop it.
```shell
ray stop 
```

As a reminder, here are the commands you may use to start your cluster on minikube (feel free to change the resources setup according to your machine): 

```shell
minikube start --cpus=5 --memory=7995
```

```shell
minikube dashboard
```

```shell
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
```

```shell
helm install kuberay-operator kuberay/kuberay-operator --version 1.0.0
```

You may create a file called `ray-cluster.yaml` like :
```yaml
head:
  enableInTreeAutoscaling: true
  resources:
    limits:
      cpu: "3"
      memory: "4G"
    requests:
      cpu: "3"
      memory: "4G"

worker:
  replicas: 1
  resources:
    limits:
      cpu: "2"
      memory: "3G"
    requests:
      cpu: "2"
      memory: "3G"
```

```shell
helm install raycluster kuberay/ray-cluster --version 1.3.0 --set 'image.tag=2.41.0-aarch64' -f ray-cluster.yaml
```

```shell
kubectl port-forward --address 0.0.0.0 service/raycluster-kuberay-head-svc 8265:8265
```

```shell
ray job submit --working-dir=. --runtime-env=runtime-env.json --address="http://127.0.0.1:8265" -- python ray_train.py
```


3. Install Chart cluster :
```shell
helm install psql bitnami/postgresql -f config.yaml
# See STDOUT further on this documentation
```

4. Test/use DB :
```shell
export POSTGRES_PASSWORD=$(kubectl get secret --namespace default psql-postgresql -o jsonpath="{.data.password}" | base64 -d)

kubectl run psql-postgresql-client --rm --tty -i --restart='Never' --namespace default \
--image docker.io/bitnami/postgresql:17.5.0-debian-12-r12 --env="PGPASSWORD=$POSTGRES_PASSWORD" \
--command -- psql --host psql-postgresql -U qxzjy -d mlflow -p 5432

# \dt => show table
# \db => show db
# \du => show user
# SELECT * FROM table;
```

5. Load deployment configuration : 
```shell
kubectl apply -f mlflow-deployment.yaml
```

6. Load service configuration :
```shell
kubectl apply -f mlflow-service.yaml
```

7. Load secrets configuration :
```shell
kubectl apply -f secrets.yaml
```

8. Launch service :
```shell
minikube service mlflow-service
```
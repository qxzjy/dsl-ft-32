In case the local ray cluster is still in use, let's stop it.
```shell
ray stop 
```

As a reminder, here are the commands you may use to start your cluster on minikube (feel free to change the resources setup according to your machine): 

```shell
minikube start --cpus=5 --memory=7995
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
ray job submit --runtime-env=ray/exec/runtime-env.yaml --address="http://127.0.0.1:8265" -- python ray/exec/train_ray_cluster.py 
```
# python-beam-kafka
A boilerplate project for running Kafka-consuming Python Beam pipelines on Flink Runners over Kubernetes


## How to Run

Assuming you have `minikube` and `kubectl` and `docker` and `python` installed...


```
# Start the kubernetes services
minikube start
kubectl apply -f k8s/

# Forward 8081 to see the JobManager Web UI
kubectl port-forward $(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep jobmanager | head -n 1) 8081:8081

# Run the simple non-Kafka pipeline
python test-beam/simple-beam.py

# You should see the job submitted, run, and successfully exited.

# Run the simple Kafka pipeline
python test-beam/simple-kafka-beam.py

# This breaks, seemingly because the TaskManager is looking in /tmp/ for the packaged artifacts.

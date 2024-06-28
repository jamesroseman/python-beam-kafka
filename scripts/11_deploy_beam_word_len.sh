#!/bin/bash

# Check if the FlinkDeployment "word-len-cluster" exists
if kubectl get flinkdeployments.flink.apache.org word-len-cluster &> /dev/null; then
    kubectl delete flinkdeployments.flink.apache.org word-len-cluster
fi

# Create the FlinkDeployment
kubectl create -f beam/word_len_cluster.yml

# Check if the Job "word-len-job" exists
if kubectl get jobs.batch word-len-job &> /dev/null; then
    kubectl delete jobs.batch word-len-job
fi

# Create the Job
kubectl create -f beam/word_len_job.yml
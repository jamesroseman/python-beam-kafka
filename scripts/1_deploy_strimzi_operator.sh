#!/bin/bash

## Download and deploy the Strimzi operator.
STRIMZI_VERSION="0.39.0"

## Optional: If downloading a different version, include this step.
DOWNLOAD_URL=https://github.com/strimzi/strimzi-kafka-operator/releases/download/$STRIMZI_VERSION/strimzi-cluster-operator-$STRIMZI_VERSION.yaml
curl -L -o k8s/strimzi-cluster-operator-$STRIMZI_VERSION.yaml \
  ${DOWNLOAD_URL} &&

# Update the namespace from myproject to default.
sed -i 's/namespace: .*/namespace: default/' k8s/strimzi-cluster-operator-$STRIMZI_VERSION.yaml &&

## Deploy the Strimzi cluster operator.
kubectl create -f k8s/strimzi-cluster-operator-$STRIMZI_VERSION.yaml
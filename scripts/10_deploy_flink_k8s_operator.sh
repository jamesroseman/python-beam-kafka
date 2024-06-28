#!/bin/bash

helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-1.8.0/ &&

helm upgrade --install flink-kubernetes-operator flink-operator-repo/flink-kubernetes-operator &&

helm list

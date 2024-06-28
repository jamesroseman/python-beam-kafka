#!/bin/bash

curl -L -o k8s/cert-manager.yaml https://github.com/jetstack/cert-manager/releases/download/v1.8.2/cert-manager.yaml &&

kubectl create -f k8s/cert-manager.yaml

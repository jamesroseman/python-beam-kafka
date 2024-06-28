#!/bin/bash

eval $(minikube docker-env) &&
docker build -t beam-python-example:1.16 beam/ &&
docker build -t beam-python-harness:2.56.0 -f beam/Dockerfile-python-harness beam/
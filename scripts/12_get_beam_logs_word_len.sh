#!/bin/bash

kubectl logs  $(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep word-len-job | head -n 1) -f
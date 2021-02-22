#!/bin/bash
# BASH CALL TO BUILD AND RUN LOCAL  DRAGON BEAR CLASSIFIER CLIENT
#Bash call to build TF Serving model locally and client to interface with it
bash run_servable_model.sh
cd client/
docker build -t dragonfinderclientapi:latest .
docker run -p 5000:5000 --link dragon_bear_classifier_mobilenetv2_server dragonfinderclientapi:latest
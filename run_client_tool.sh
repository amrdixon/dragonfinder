#!/bin/bash
# BASH CALL TO BUILD AND RUN DRAGON BEAR CLASSIFIER CLIENT
cd client/
docker build -t dragonfinderclientapi:latest .
docker run -p 5000:5000 dragonfinderclientapi:latest
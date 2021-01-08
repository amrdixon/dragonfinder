#!/bin/bash
# BASH CALL TO BUILD AND RUN DRAGON BEAR CLASSIFIER CLIENT
cd client/
docker build -t dragon_bear_client .
docker run -it --network=host dragon_bear_client
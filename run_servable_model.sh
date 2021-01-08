#!/bin/bash
# BASH CALL TO BUILD DRAGON BEAR CLASSIFIER SERVING MODEL
model_name=dragon_bear_classifier_mobilenetv2
model_dir=$(pwd)/models

docker pull tensorflow/serving
docker run -d --name serving_base_${model_name} tensorflow/serving
docker cp ${model_dir}/${model_name} serving_base_${model_name}:/models/${model_name}
docker commit --change "ENV MODEL_NAME ${model_name}" serving_base_${model_name} ${model_name}
docker kill serving_base_${model_name}
docker run -p 8501:8501 \
		-e MODEL_NAME=dragon_bear_classifier_mobilenetv2 \
		-t dragon_bear_classifier_mobilenetv2
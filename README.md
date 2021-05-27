# Dragon Finder

The dragon finder project is a deep learning image classifier that identifies the presence of dragons. Alas, dragons are fickle creatures and rarely seen in the wild. So, in this phase of the project, the classifier predicts whether an image is a plush dragon or plush bear.

![](client/data_sample/dragondragon_sample.jpg)

The focus of this work is the process of deploying a TensorFlow model to be incorporated in an app. This repo supports the use of three different kinds of model inference servers:
1. Local TensorFlow Serving
2. Cloud AWS SageMaker Inference Endpoint
3. Cloud REST API

A locally deployed REST API client capable of interfacing with each server type is also included.

## Project Directory
- client: Client tool directory
- cloud_deployment: Deployment of model in cloud directory
- models: Model development directory
- run_client_tool.sh
- run_servable_model.sh
- run_server_client_local.sh

## Run Instructions (Mac/Linux)

The project package is composed of three different types of servers and their corresponding clients. This repo come fully equipped to deploy the local Docker TF-Serving model on the local machine and contains instructions for model server cloud deployment for use with this repo.

### Local Server

 In order to run both the local server and client, you must have Docker installed and run the following command:

    bash run_server_client_local.sh
    
This should deploy two linked Docker containers: one serving the model and one acting as a REST API client. The local server inference model is contained in a Docker container and requests to the model are made via a REST API. The Docker serving image was developed using TensorFlow Serving and the container publishes the REST API to our host's port 8501. The client Docker container provides a consistent interface for all server types. The client container publishes the client REST API to the host's port 5000. Once the server and client API is built and running, you can interface with it via HTTP POST method. A sample real world dataset has been provided in the client/data_sample directory. An example of how to classify an image would be to enter the following command in your terminal:

    curl -v -H "Content-Type: multipart/form-data" -F "file=@client/data_sample/bear/IMG_5079.jpg" http://0.0.0.0:5000/classify
    
### Cloud Server

The two types of cloud servers developed in this project are an AWS SageMaker inference endpoint and a cloud REST API using Amazon API Gateway. The SageMaker deployment of the model requires your own AWS credentials and this repo contains instructions to assist you in your own deployment. The cloud REST API server is an extension of the SageMaker inference model deployment that provides better interfacing for the app. Instructions for deploying both types of cloud servers are found in the cloud_deployment directory. Once the servers are deployed and the setup has been completed, run the following command to deploy the client:

    bash run_client_tool.sh
    
Just as with the local server/client deployment, you can interface with it via HTTP POST method. A sample real world dataset has been provided in the client/data_sample directory. An example of classifying an image is as follows:

    curl -v -H "Content-Type: multipart/form-data" -F "file=@client/data_sample/bear/IMG_5079.jpg" http://0.0.0.0:5000/classify?server_type=<SERVER_TYPE>
    
where SERVER_TYPE is either 'SageMaker', 'RESTAPIPublic' or 'RESTAPIPrivate' depending on desired server.

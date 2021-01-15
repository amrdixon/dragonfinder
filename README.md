# Dragon Finder

The dragon finder project is a deep learning image classifier that identifies the presence of dragons. Alas, dragons are fickle creatures and rarely seen in the wild. So, in this phase of the project, the classifier predicts whether an image is a plush dragon or plush bear.

## Project Directory
- client: Client tool directory
- models: Model development directory
- run_servable_model.sh
- run_client_tool.sh


## Run Instructions
The project package is composed of a server and a client. It is essential to first build and run the server before the client.

### Server

There are two different types of server: Docker TF-Serving container and an AWS SageMaker inference endpoint. The Docker TF-Serving model is deployed on the local machine. This repo contains all necessary components to run the current model in a local server. The AWS SageMaker model is a cloud-based endpoint for serving predictions. The SageMaker deployment of the model requires your own AWS credentials and this repo contains instructions to assist you in your own deployment.

#### Docker TF-Serving (Local)

The local server inference model is contained in a Docker container and requests to the model are made via a REST API. The Docker serving image was developed using TensorFlow Serving and the container publishes the REST API to our host's port 8501.

To build and run the server:

    bash run_servable_model.sh
    
#### AWS SageMaker Endpoint

The cloud-based inference model was deployed using AWS SageMaker. Instructions to deploy the model using SageMaker are located in the cloud_deployment directory.

### Client
The client is a CLI tool run in a separate Docker container. 

To build and run the client:

    bash run_client_tool.sh

Once inside the Docker container, you can connect to the tool and classify an image using the following:

    python3 main_application.py <image_path>

A sample real world dataset has been provided in the /data_sample directory. An example running the tool is as follows:

    python3 main_application.py data_sample/bear/IMG_5077.jpg
    
By default, the client works with the local Docker server set up by the bash run_servable_model.sh script. In order to use a SageMaker inference endpoint instead, you must first gather key details about your deployment (i.e. endpoint name and yoru AWS credentials) as outlined by the instructions in the cloud_deployment directory, and then add the following arguments to the client tool command:

    python3 main_application.py <image_path> --server_type SageMaker --endpoint <sagemaker_endpoint> --creds <aws_creds_file> 

# Dragon Finder

The dragon finder project is a deep learning image classifier that identifies the presence of dragons. Alas, dragons are fickle creatures and rarely seen in the wild. So, in this phase of the project, the classifier predicts whether an image is a plush dragon or plush bear.

## Project Directory
- client: CLI tool client tool directory
- models: Model development directory
- run_servable_model.sh
- run_client_tool.sh


## Run Instructions
The project package is composed of a server and a client. It is important to build and run the server before the client. This project currently runs 

### Server
The server inference model is contained in a Docker container and requests to the model are made via a REST API. The Docker serving image was developed using TensorFlow Serving and the container publishes the REST API to our host's port 8501.

To build and run the server:

    bash run_servable_model.sh

### Client
The client is a CLI tool run in a separate Docker container. 

To build and run the client:

    bash run_client_tool.sh

Once inside the Docker container, you can connect to the tool and classify an image using the following:

    dragon_bear_client classify-image <image_path>

A sample real world dataset has been provided in the /data_sample directory. An example of the tool run command is as follows:

    dragon_bear_client classify-image data_sample/bear/IMG_5077.jpg

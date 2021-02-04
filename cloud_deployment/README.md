# TensorFlow Inference Endpoint Deployment on AWS SageMaker

This directory contains all scripts and documentation needed to take an already trained and saved TF model and deploy it as an inference endpoint in AWS SageMaker.

## Directory Contents
- aws_model_deploy.py: Main (entry point) script
- aws_model_util.py: AWS TF model deployment functions
- aws_sm_config_template.json: AWS SageMaker config file template

## Run Instructions

In order to deploy the inference endpoint, do the following steps:

1. Set up a virtual environment virtualenv
2. Create and activate AWS account
3. Address SageMaker prerequisites: IAM role and S3 model upload
5. Deploy SageMaker inference endpoint

Each of these steps is explained in more detail below.

### Set up a virtual environment virtualenv

In order to set up all the dependencies to run the Python code, you will need to first ensure you have all the correct dependencies. In order to do this, we are going to create a virtual environment. If you don't already have virtualenv installed, do so now using the following command:

	python3 -m pip install --user virtualenv

Once you have virtualenv installed, you will create a virtual environment for this project with the following steps:

1. Find out where your default Python3 installation is located:
	which python3
2. Create a new virtual environment set up your virtual environment:
	virtualenv -p /path/to/python3 venv

Be sure to replace /path/to/python3 with the result of the 'which python3' command.

Next, activate the virtual environment:

	source venv/bin/activate
	
Once inside your virtual environment, you will install the dependencies:

	pip3 install -r requirements.txt
	
### Create and activate AWS account

If you do not already have an AWS account, you will need to create and activate one now. The best way to set up your account, is to follow the instructions provided [here](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).

Once the AWS account is set up, you will also need to set up your machine for AWS development. One way to do this is to set your AWS credentials profile on yoru local system located at ~/.aws/credentials on Linus, macOS and Unix. If that file doesn't already exist, create it. The file should have the following format:

	[default]
	aws_access_key_id = your_access_key_id
	aws_secret_access_key = your_secret_access_key
	region = your_aws_region

You will need to substitute you own AWS credentials for the values aws_access_key_id, aws_secret_access_key and region. For region, put the region name that is selected by default for your account (e.g. us-east-1). For the aws_access_key_id and aws_secret_access_key, go to the [security credentials page](https://console.aws.amazon.com/iam/home?#/security_credentials) and select the "Access keys (access key ID and secret access key)" option. Select the "Create New Access Key" and download the file containing your keys when prompted. Copy the AWS access key id and secret access key from the downloaded file and paste them in their respective places in the local credentials file ( ~/.aws/credentials).

Further guidance for setting your AWS credentials can be found [here](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).

### Create AWS IAM role and upload trained and saved model to S3

Before SageMaker can deploy the endpoint, we have to create a IAM role to authorize its' actions and upload the model to S3. The model is presumed to be already trained and saved in Tensorflow SavedModel format. It is also imperative that the saved model be compressed to the .tar.gz format.

If this is the first time deploying any SageMaker endpoints, it is easiest to run the following:

	python3
	from aws_model_util import write_new_sm_config
	write_new_sm_config(config_file, model_path)
	exit()

where config_file is the string name of the config file and model_path is the string local path to the model being uploaded to S3. An example would be:

	python3
	from aws_model_util import write_new_sm_config
	write_new_sm_config('aws_sm_config.json', './models/dragon_bear_classifier_mobilenetv2/dragon_bear_classifier_mobilenetv2.tar.gz')
	exit()
	
### Deploy SageMaker inference endpoint

To deploy, run the following code:

	python3 aws_model_deploy.py <config_file>
	
where config file is the path to the config file just created. If you ran teh example code as written above, the command would be:

	python3 aws_model_deploy.py aws_sm_config.json
	
It takes a few minutes for AWS to complete the request and then you should have a real-time inference endpoint!

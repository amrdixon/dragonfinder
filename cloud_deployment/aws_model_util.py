from sagemaker.tensorflow.model import TensorFlowModel
import boto3
import sagemaker
from datetime import datetime, timezone
import json
from pathlib import Path
import re

def deploy_smtf_endpoint(model_data_s3=None, iam_arn=None, framework_version='2.3.0'):
    """
    Deploys TensorFlow model to SageMaker endpoint
    
    args:
    model_data_s3 (str, defaul None): S3 URI for compressed TF model to be deployed
    iam_arn (str, default None): AWS IAM ARN with appropriate SageMaker and S3 permissions
    framework_version (str, default '2.3.0'): TensorFlow Serving version
    
    returns:
    SageMaker Endpoint ARN (str)
    
    """
    
    try:            
        model = TensorFlowModel(model_data=model_data_s3,\
        role=iam_arn,\
        framework_version=framework_version)
        #TODO: add option to specify deploy kwargs
        predictor = model.deploy(initial_instance_count=1, instance_type='ml.c5.xlarge')
        sm_inference_arn = predictor.endpoint_name
        print('Successfully deployed Sagemaker TF inference endpoint to: {}'.format(sm_inference_arn))
    except Exception as e:
        print("Unable to deploy Sagemaker TF model inference endpoint: {}".format(str(e)))
        
    return sm_inference_arn
    
    
def add_sm_iam_role(update_config_file=None):
    """
    Adds an IAM role to AWS account for SageMaker principal with attached policies for SageMaker and S3.
    If update_config_file parameter specified, new IAM rold ARN is written to the JSON file as 'iam_arn'
    value.
    
    args:
    update_config_file (str, default None): path for JSON config file
    
    returns:
    IAM Role ARN
    
    """
    
    iam = boto3.resource('iam')
    iam_role_name = 'smtf_role_' + datetime.now(timezone.utc).isoformat().replace(':', '')
    
    trust_relationship_policy_sm = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "sagemaker.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    
    iam.create_role(AssumeRolePolicyDocument=json.dumps(trust_relationship_policy_sm), RoleName=iam_role_name)
    iam_role = iam.Role(iam_role_name)
    #attach policies for sagemaker and s3
    iam_role.attach_policy(PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess')
    iam_role.attach_policy(PolicyArn='arn:aws:iam::aws:policy/AmazonSageMakerFullAccess')
    
    #Write IAM arn to config file
    if update_config_file:
        #read in
        #check if config file exists
        config_file_exists = Path(update_config_file).is_file()
        if config_file_exists:
            config_f = open(update_config_file)
            config = json.loads(config_f.read())
            config_f.close()
        else:
            config = {}
        config['iam_arn'] = iam_role.arn
        
        with open(update_config_file, 'w') as f:
            json.dump(config, f)
    
    return iam_role.arn
 

def upload_model_s3(model_path, update_config_file=None):
    """
    Uploads local saved Tensrflow model to AWS S3. A bucket is created and teh model is uploaded to that bucket.
    If update_config_file parameter specified, new S3 URI is written to the JSON file as 'model_data_s3'
    value.
    
    args:
    model_path (str): path fo model to upload
    update_config_file (str, default None): path for JSON config file
    
    returns:
    IAM Role ARN
    
    """
    
    #create new bucket
    try:
        s3 = boto3.client('s3')

        #if bucket 'sagemaker_models' not present, add it
        model_name = Path(model_path).name.split('.')[0]
        bucket_name = model_name + '-sagemaker-model'
        bucket_name = re.sub(r'[^A-Za-z0-9]', '', bucket_name)
        print(bucket_name)
        list_buckets_resp = s3.list_buckets()
        if bucket_name not in [x['Name'] for x in list_buckets_resp['Buckets']]:
            s3.create_bucket(Bucket=bucket_name)
    except Exception as e:
        print('Could not create new s3 bucket: ', e)

    #add file to bucket
    try:
        s3_object_key = Path(model_path).name
        boto3.resource('s3').Bucket(bucket_name).upload_file(model_path, s3_object_key)
        s3_uri = 's3://' + bucket_name + '/' + s3_object_key
        
        #Write IAM arn to config file
        if update_config_file:
            #read in
            #check if config file exists
            config_file_exists = Path(update_config_file).is_file()
            if config_file_exists:
                config_f = open(update_config_file)
                config = json.loads(config_f.read())
                config_f.close()
            else:
                config = {}
            config['model_data_s3'] = s3_uri
        
            with open(update_config_file, 'w') as f:
                json.dump(config, f)
        
        
    except Exception as e:
        print('Could not upload model to S3: ', e)
        
    return s3_uri
    
def write_new_sm_config(update_config_file, model_path):
    """
    Initiates the SageMaker config file by creating a IAM role and uploading the model to S3.
    
    args:
    update_config_file (str, default None): path for JSON config file
    model_path (str): path fo model to upload
    
    returns:
    None
    
    """
    add_sm_iam_role(update_config_file)
    upload_model_s3(model_path, update_config_file)

    
    
    
    
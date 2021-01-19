from sagemaker.tensorflow.model import TensorFlowModel
import boto3
import sagemaker

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
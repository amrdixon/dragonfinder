from sagemaker.tensorflow import TensorFlowModel, predictor
import boto3
import sagemaker



class SageMakerTFInference:
    
    def __init__(self, sm_inference_arn=None, model_data_s3=None, iam_arn=None, framework_version='2.3.0'):
        
        #if calling existing sagemaker tf endpoint
        if sm_inference_arn:
            try:
                self._sm_inference_arn = sm_inference_arn
                self._predictor = predictor.Predictor(sm_inference_arn)
                print("Connection to Sagemaker TF inference endpoint successful.")
            except Excetption as e:
                print("Connection to Sagemaker TF inference endpoint failed: {}".format(str(e)))
        else:
            try:
                model = TensorFlowModel(model_data=model_data_s3,\
                role=iam_arn,\
                framework_version=framework_version)
                #TODO: add option to specify deploy kwargs
                self._predictor = model.deploy(initial_instance_count=1, instance_type='ml.c5.xlarge')
                self._sm_inference_arn = self._predictor.endpoint_name
                print('Successfully deployed Sagemaker TF inference endpoint to: {}'.format(self._sm_inference_arn))
            except Exception as e:
                print("Unable to deploy Sagemaker TF model inference endpoint: {}".format(str(e)))
                
                
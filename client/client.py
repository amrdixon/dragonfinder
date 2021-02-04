import numpy as np
from PIL import Image
import requests
import json
import os
import boto3
from abc import ABC, abstractmethod


class ImageBinaryClassifierDriver(ABC):
    """
    Inmage Binary Classification Client interface    
    """
    
    @abstractmethod
    def classify_image(self, image_path):
        pass
        
        
class ImageBinaryClassifierRESTAPIDriver(ImageBinaryClassifierDriver):
    """
    Image Binary Classifier - REST API
    
    This client class works with a model taht has been fully deployed as a REST API.
    
    """
    
    def __init__(self, url_post, api_key=None, input_tensor_shape=[None,160,160]):
        """
        Client Instantiation
        
        args:
        url_post (str): POST URL
        key (str): API key
        input_tensor_shape: input tensor shape for model, must have len(input_tensor_shape)=3
        
        returns:
        None
        
        """
        
        self._url_post = url_post
        self._api_key = api_key
        
        #classifier parameters
        self._input_tensor_shape = input_tensor_shape
    
        
    def classify_image(self, image_path=None, pil_image=None):
        """
        Performs inference on image
        
        args:
        image_path (string, pathlib.Path object or a file object): path for image to classify
        pil_image (pil.Image): Pillow Image, required if image_path is not specified
        
        returns:
        predicted class label (str)
        
        """
        
        #open image and format for Sagemaker endpoint
        if image_path:
            input_img = Image.open(image_path)
        else:
            input_img = pil_image
        input_img = input_img.resize(self._input_tensor_shape[-2:])
        img_batch_arr = np.array([np.array(input_img)])
        
        body = json.dumps({'instances':img_batch_arr.tolist()})
        if self._api_key:
            headers = {"content-type": "application/json", "x-api-key": self._api_key}
        else:
            headers = {"content-type": "application/json"}
        
        try:
            x = requests.post(self._url_post, data=body, headers=headers)
            if x.status_code == 200:
                print('Successfully completed inference.')
                response = x.json()
                print('Model Prediction: {}'.format(response['prediction']))                
            else:
                print('Could not run inference using this connection.')
        except Exception as e:
            print('Running model inference failed: {}'.format(str(e)))
    
        
        
        
class ImageBinaryClassifierTFSageMakerDriver(ImageBinaryClassifierDriver):
    """
    Image Binary Classifier Client - AWS Sagemaker
    """
    
    def __init__(self, creds, endpoint, labels=['0','1'], input_tensor_shape=[None,160,160]):
        """
        Client instantiation
        
        args:
        creds (dict): AWS credentials to call Sagemaker endpoint
        endpoint (str): AWS Sagemaker endpoint
        label ([label0, label1]): classifier output label names
        input_tensor_shape: input tensor shape for model, must have len(input_tensor_shape)=3
        returns:
        None
        """
        
        self._boto3_client = boto3.Session().client('sagemaker-runtime', **creds)
        
        #Connection parameters
        self._endpoint = endpoint
        self._conect_ok = False
        
        #classifier parameters
        self._class_labels = labels
        self._input_tensor_shape = input_tensor_shape
        
    def classify_image(self, image_path=None, pil_image=None):
        """
        Performs inference on image
        
        args:
        image_path (string, pathlib.Path object or a file object): path for image to classify
        pil_image (pil.Image): Pillow Image, required if image_path is not specified
        
        returns:
        predicted class label (str)
        
        """
        
        #open image and format for Sagemaker endpoint
        if image_path:
            input_img = Image.open(image_path)
        else:
            input_img = pil_image
        input_img = input_img.resize(self._input_tensor_shape[-2:])
        img_batch_arr = np.array([np.array(input_img)])
        
        body = json.dumps({'instances':img_batch_arr.tolist()})
        
        
        try:
            resp = self._boto3_client.invoke_endpoint(EndpointName=self._endpoint,\
            ContentType='application/json', Body=body)
            
            #check status code
            if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('Successfully completed inference.')
                result = json.loads(resp['Body'].read().decode())
                res_logit = result["predictions"][0][0]
                res_class_int = int(res_logit>=0.0)
                print('Model Predictions \n{} : {}'.format(image_path, self._class_labels[res_class_int]))                
            else:
                print('Could not run inference using this connection.')
        except Exception as e:
            print('Running model inference failed: {}'.format(str(e)))
            
        return self._class_labels[res_class_int]
                            
        

class ImageBinaryClassifierTFServingDriver(ImageBinaryClassifierDriver):
    """
    Image Binary Classifier Client - TF Serving
    """
    
    
    def __init__(self, endpoint, labels=['0','1'], input_tensor_shape=[None,160,160]):
        """
        Client instantiation
        """
        
        #Connection parameters
        self._endpoint = endpoint
        self._conect_ok = False
        
        #classifier parameters
        self._class_labels = labels
        self._input_tensor_shape = input_tensor_shape
        
        #start connection
        try:
            connect_resp = requests.get(self._endpoint)
            if connect_resp.status_code == 200:
                print("Connection to server successful.")
                self._conect_ok = True
            else:
                print("Could not connect to server.")
        except Exception as e:
            print('Connection to server failed: {}'.format(str(e)))
        
        
    def classify_image(self, image_path=None, pil_image=None):
        """
        Performs inference on image
        
        args:
        image_path (string, pathlib.Path object or a file object): path for image to classify
        
        returns:
        predicted class label (str)
        
        """
        
        input_img = Image.open(image_path)

        input_img = input_img.resize(self._input_tensor_shape[-2:])
        img_batch_arr = np.array([np.array(input_img)])
        
        headers = {"content-type": "application/json"}
        data = json.dumps({"signature_name": "serving_default", "instances": img_batch_arr.tolist()})
        
        try:
            post_url = self._endpoint + ':predict'
            x = requests.post(post_url, data=data, headers=headers)
            if x.status_code == 200:
                print('Successfully completed inference.')
                response = x.json()
                res_logit = response["predictions"][0][0]
                res_class_int = int(res_logit>=0.0)
                print('Model Predictions \n{} : {}'.format(image_path, self._class_labels[res_class_int]))                
            else:
                print('Could not run inference using this connection.')
        except Exception as e:
            print('Running model inference failed: {}'.format(str(e)))
            
        return self._class_labels[res_class_int]

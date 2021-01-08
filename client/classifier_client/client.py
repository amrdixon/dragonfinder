import numpy as np
from PIL import Image
import requests
import json
import os


class ImageBinaryClassifierClient:
    """
    Image Binary Classifier Client
    """
    
    
    def __init__(self, model_server_url, class_labels=['0','1'], input_tensor_shape=[None,160,160]):
        """
        Client instantiation
        """
        
        #Connection parameters
        self._server_url = model_server_url
        self._conect_ok = False
        
        #classifier parameters
        self._class_labels = class_labels
        self._input_tensor_shape = input_tensor_shape
        
        #start connection
        try:
            connect_resp = requests.get(model_server_url)
            if connect_resp.status_code == 200:
                print("Connection to server successful.")
                self._conect_ok = True
            else:
                print("Could not connect to server.")
        except Exception as e:
            print('Connection to server failed: {}'.format(str(e)))
        
        
    def classify_image_from_path(self, image_path):
        """
        Classifies an image given an image path
        
        args:
        image_path (str or path)
        
        returns:
        class label (str)
        """
        
        input_img = Image.open(image_path)
        input_img = input_img.resize(self._input_tensor_shape[-2:])
        img_batch_arr = np.array([np.array(input_img)])
        
        headers = {"content-type": "application/json"}
        data = json.dumps({"signature_name": "serving_default", "instances": img_batch_arr.tolist()})
        
        try:
            post_url = self._server_url + ':predict'
            x = requests.post(post_url, data=data, headers=headers)
            if x.status_code == 200:
                print('Successfully completed inference.')
                response = x.json()
                res_logit = response["predictions"][0][0]
                print('The model classifies the image at {} as {}'.format(image_path, self._class_labels[int(res_logit>=0.0)]))
                
            else:
                print('Could not run inference using this connection.')
        except Exception as e:
            print('Running model inference failed: {}'.format(str(e)))
            
            
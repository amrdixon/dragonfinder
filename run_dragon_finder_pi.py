import time
import picamera
import requests
import json
import logging


def capture_image(img_filepath='picamera_image.jpg'):
    """
    Starts pi camera, takes photo and saves to file
    
    args:
    img_filepath (str, default='picamera_image.jpg'): filepath to write
    returns:
    img_filepath
    
    """
    
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(2)
        camera.capture('picamera_image.jpg')
        
    return img_filepath
        
def run_inference_restapi(img_filepath):
    """
    Runs inference using local Docker client running on pi
    args:
    img_filepath (str): filepath to local image to run inference on
    returns:
    prediction (str)
    
    """
    
    headers = {"content-type": "multipart/form-data"}
    local_client_url = 'http://0.0.0.0:5000/classify?server_type=RestAPIPublic'
    x = requests.post(local_client_url, file=img_filepath, headers=headers)
    response = x.json()
     
    logging.debug('Model Prediction of picture taken: {}'.format(response['prediction']))
     
    return response['prediction']
        
        
if __name__ == "__main__":
    img_filepath = capture_image()
    prediction = run_inference_restapi(img_filepath)
    

    
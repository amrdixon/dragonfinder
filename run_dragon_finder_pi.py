import time
import picamera
import requests
import json


def capture_image(img_filepath='picamera_image.jpg'):
    
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
    	#camera.annotate_text = 'Hello world!'
        # Camera warm-up time
        time.sleep(2)
        camera.capture('picamera_image.jpg')
        
    return img_filepath
        
def run_inference_restapi(img_filepath):
     headers = {"content-type": "multipart/form-data"}
     local_client_url = 'http://0.0.0.0:5000/classify?server_type=RestAPIPublic'
     x = requests.post(local_client_url, data=img_filepath, headers=headers)
     response = x.json()
     
     logging.debug('Model Prediction of picture taken: {}'.format(response['prediction']))
     
     return response['prediction']
        
        
if __name__ == "__main__":
    img_filepath = capture_image()
    prediction = run_inference_restapi(img_filepath)
    

    
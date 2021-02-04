import client
import argparse
import json

parser = argparse.ArgumentParser(description='Dragon Bear Classifier Client')

#image path and config file are mandatory
parser.add_argument('image_path', metavar='image_path', help='input image')
parser.add_argument('--config_path', dest='config_path', default='config/tfserving_config.json', help='config file')

args = parser.parse_args()

def main():
    #capture args
    # endpoint = args.endpoint
    # labels = args.labels
    image_path = args.image_path
    
    config_f = open(args.config_path)
    config_dict = json.loads(config_f.read())
    server_type = config_dict['server_type']
    del config_dict['server_type']
    
    #instantiate right type of client
    if server_type == 'TFServing':
        driver = client.ImageBinaryClassifierTFServingDriver(**config_dict)
    elif server_type =='SageMaker':
        #reads in AWS credentials
        creds_f = open(config_dict['creds_filepath'])
        creds = json.loads(creds_f.read())
        del config_dict['creds_filepath']
        driver = client.ImageBinaryClassifierTFSageMakerDriver(creds, **config_dict)
    elif server_type == 'RESTAPI':
        driver = client.ImageBinaryClassifierRESTAPIDriver(**config_dict)
        
    
    #classify image
    driver.classify_image(image_path)

if __name__ == '__main__':
	main()
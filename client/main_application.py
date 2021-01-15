import client
import argparse
import json

parser = argparse.ArgumentParser(description='Dragon Bear Classifier Client')

#image path is mandatory
parser.add_argument('image_path', metavar='image_path', help='input image')
#options for defining wihch server, local Docker TF-Serving is default
parser.add_argument('--server_type', dest='server_type', default='TFServing')
parser.add_argument('--endpoint', dest='endpoint', default='http://localhost:8501/v1/models/dragon_bear_classifier_mobilenetv2')
parser.add_argument('--creds', dest='creds', default=None)
parser.add_argument('--labels', dest='labels', default=['Bear', 'Dragon'])

args = parser.parse_args()

def main():
    #capture args
    endpoint = args.endpoint
    labels = args.labels
    image_path = args.image_path
    
    #instantiate right type of client
    if args.server_type == 'TFServing':
        driver = client.ImageBinaryClassifierTFServingDriver(endpoint=endpoint, labels=labels)
    elif args.server_type =='SageMaker':
        #reads in AWS credentials
        creds_f = open(args.creds)
        creds = json.loads(creds_f.read())
        driver = client.ImageBinaryClassifierTFSageMakerDriver(creds, endpoint=endpoint, labels=labels)
    
    #classify image
    driver.classify_image(image_path)

if __name__ == '__main__':
	main()
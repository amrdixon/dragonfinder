import argparse
import json
from aws_model_util import write_new_sm_config

parser = argparse.ArgumentParser(description='AWS SageMaker Endpoint Deployment - Setup')

#config file is mandatory
parser.add_argument('config_file', metavar='config_file', help='Config file to write to with AWS IAM and S3 info.')
parser.add_argument('model_path', metavar='model_path', help='Model to be uploaded to S3.')

args = parser.parse_args()

def main():
    
    write_new_sm_config(args.config_file, args.model_path)


if __name__ == '__main__':
	main()
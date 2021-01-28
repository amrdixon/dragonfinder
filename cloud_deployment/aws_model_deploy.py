import argparse
import json
from aws_model_util import deploy_smtf_endpoint

parser = argparse.ArgumentParser(description='AWS SageMaker Endpoint Deployment')

#config file is mandatory
parser.add_argument('config_file', metavar='config_file', help='Config file with AWS IAM and S3 info.')

args = parser.parse_args()

def main():
    
    config_f = open(args.config_file)
    config = json.loads(config_f.read())
    sm_arn = deploy_smtf_endpoint(**config)


if __name__ == '__main__':
	main()
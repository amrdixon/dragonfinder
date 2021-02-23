import argparse
import json
from aws_model_util import deploy_smtf_endpoint

parser = argparse.ArgumentParser(description='AWS SageMaker Endpoint Deployment')

#config file is mandatory
parser.add_argument('config_file', metavar='config_file', help='Config file with AWS IAM and S3 info.')
parser.add_argument('--write_sm_client', dest='write_sm_client', default=False, help='Writes SageMaker conifg info for client')

args = parser.parse_args()

def main():
    
    config_f = open(args.config_file)
    config = json.loads(config_f.read())
    sm_arn = deploy_smtf_endpoint(**config)
    
    if args.write_sm_client:
        client_config_template_f = open('../client/config/sagemaker_config_template.json')
        client_config = json.loads(client_config_template_f.read())
        client_config['endpoint'] = sm_arn
        #write to output file
        with open('../client/config/sagemaker_config.json', 'w') as outfile:
            json.dump(client_config, outfile)
        


if __name__ == '__main__':
	main()
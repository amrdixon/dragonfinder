from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import client
from PIL import Image
import json
import werkzeug
import io


# Initialize Flask
app = Flask(__name__)
api = Api(app)


class ClassifyImage(Resource):
    def post(self):
        
        #gather all the args sent by POST method
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
        parse.add_argument('server_type', type=str, location='args', required=False)
        args = parse.parse_args()
        image_file = args['file']
        server_type = args['server_type']
        
        #read image into memory
        in_memory_file = io.BytesIO()
        image_file.save(in_memory_file)
        pil_image = Image.open(in_memory_file)
        
        def load_config_dict(config_path):
            config_f = open(config_path)
            config_dict = json.loads(config_f.read())
            server_type = config_dict['server_type']
            del config_dict['server_type']
            return config_dict

        #choose which server type this client is connecting to
        if server_type:
            if server_type == 'TFServing':
                config_path = 'config/tfserving_config.json'
                config_dict = load_config_dict(config_path)
                driver = client.ImageBinaryClassifierTFServingDriver(**config_dict)
            elif server_type =='SageMaker':
                config_path = 'config/sagemaker_config.json'
                config_dict = load_config_dict(config_path)
                #reads in AWS credentials
                creds_f = open(config_dict['creds_filepath'])
                creds = json.loads(creds_f.read())
                del config_dict['creds_filepath']
                driver = client.ImageBinaryClassifierTFSageMakerDriver(creds, **config_dict)
            elif server_type == 'RESTAPIPublic':
                config_path = 'config/rest_public_config.json'
                config_dict = load_config_dict(config_path)
                driver = client.ImageBinaryClassifierRESTAPIDriver(**config_dict)
            elif server_type == 'RESTAPIPrivate':
                print('here')
                config_path = 'config/rest_private_config.json'
                config_dict = load_config_dict(config_path)
                driver = client.ImageBinaryClassifierRESTAPIDriver(**config_dict)
        
        #default to TF serving
        else:
            config_path = 'config/tfserving_config.json'
            config_dict = load_config_dict(config_path)
            driver = client.ImageBinaryClassifierTFServingDriver(**config_dict)


        prediction = driver.classify_image(pil_image=pil_image)

        return {'prediction': prediction}, 201

        
api.add_resource(ClassifyImage, '/classify')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
        
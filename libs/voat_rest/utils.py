import os

from flask_restful import Resource

class GetPublicKey(Resource):
    def get(self):
        key_path = '/etc/voat/config/public_key'

        if os.path.exists(key_path):
            with open(key_path, 'r') as public_key:

                return {'result':public_key.read()}


        else:
            return {'error':'no public key'}




import uuid
import datetime

from flask_restful import Resource, reqparse


class Register(Resource):
    def __init__(self, **kwargs):
        self.user_utils = kwargs['user_utils']

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()
    
        status, result = self.user_utils.add_user(password=args.get('password'), username=args.get('username'))

        if status == True:
            return {'result': result}

        return {'error':result}

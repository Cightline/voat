import uuid
import datetime

from flask_restful    import Resource, Api, reqparse
from Crypto.PublicKey import RSA
from Crypto           import Random

from passlib.apps import custom_app_context as pwd_context

from voat_sql.utils.user import UserUtils
from voat_sql.utils.db   import get_db


class Register(Resource):
    def post(self):

        user_utils = UserUtils()
        db         = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')


        args = parser.parse_args()

        #schema = Schema({
        #    Required('username
    
        # FIX: make this into a schema
        if 'username' not in args:
            return {'error':'no username given'}

        elif 'password' not in args:
            return {'error':'no password given'}

        elif args['password'] == None or args['password'] == '':
            return {'error':'password has no length'}


    
        status, result = user_utils.add_user(password=args['password'], username=args['username'])

        if status == True:
            return {'success': result}

        return {'error':result}

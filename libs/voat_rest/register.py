import uuid
import datetime

from flask_restful    import Resource, Api, reqparse
from Crypto.PublicKey import RSA
from Crypto           import Random

from passlib.apps import custom_app_context as pwd_context

from voat_sql.utils.user import UserUtils
from voat_sql.utils.db   import get_db


class Register(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self):

        user_utils = UserUtils(self.db)
        db         = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')


        args = parser.parse_args()

    
        status, result = user_utils.add_user(password=args.get('password'), username=args.get('username'))

        if status == True:
            return {'success': result}

        return {'error':result}

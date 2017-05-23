import uuid
import datetime

from flask_restful import Resource, Api, reqparse

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

        if 'username' not in args:
            return {'error':'no username given'}

        elif 'password' not in args:
            return {'error':'no password given'}

        elif args['password'] == None or args['password'] == '':
            return {'error':'password has no length'}


    
        # check to make sure doesn't exist
        
        if user_utils.get_user(args['username']):
            return {'error':'user already exists'}

       
        


        # initilize the user
        u_password  = args['password']
        u_username  = args['username']
        u_hash      = pwd_context.encrypt(u_password)
        u_api_token = str(uuid.uuid4())
        
        new_user = user_utils.create_user_object(password_hash=u_hash,
                                                 username=u_username,
                                                 # make this UTC
                                                 creation_time=datetime.datetime.now(),
                                                 api_token=u_api_token)


        db.session.add(new_user)

        # prob need some error handling here
        db.session.commit()

        return {'success':'user created'}


from flask_restful import Resource, Api, reqparse

from passlib.apps import custom_app_context as pwd_context

from voat_sql.utils.user import UserUtils

class Authenticate(Resource):


    def post(self):
        user_utils = UserUtils()
        parser     = reqparse.RequestParser()
        
        # prob need some sort of max length limit
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()


        if 'username' not in args:
            return {'error':'no username given'}

        elif 'password' not in args:
            return {'error':'no password given'}

        elif args['password'] == None or args['password'] == '':
            return {'error':'password has no length'}


        # see if the user even exists

        user = user_utils.get_user(username=args['username'])

        if not user:
            return {'error':'user does not exist'}


        if not pwd_context.verify(args['password'], user.password_hash):
            return {'error':'incorrect password'}


        return {'result':{'api_token':user.api_token, 'username':user.username}}



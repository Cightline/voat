from flask_restful import Resource, reqparse

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

        elif args['username'] == None or args['username'] == '':
            return {'error':'username has no length'}


        user = user_utils.authenticate_by_password(args['username'], args['password'])

        if not user:
            return {'error':'incorrect login'}


        return {'result':{'api_token':user.api_token, 'username':user.username}}



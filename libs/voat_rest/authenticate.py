from flask_restful import Resource, reqparse

class Authenticate(Resource):
    def __init__(self, **kwargs):
        self.user_utils = kwargs['user_utils']

    def post(self):
        parser     = reqparse.RequestParser()
        
        # prob need some sort of max length limit
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()


        result, user = self.user_utils.authenticate_by_password(args.get('username'), args.get('password'))

        if result == False:
            return {'error':'incorrect login'}
        
        return {'result':{'api_token':user.api_token, 'username':user.username}}



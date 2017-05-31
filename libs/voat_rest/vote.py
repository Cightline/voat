
from flask_restful import Resource, reqparse

class VoteThread(Resource):
    def __init__(self, **kwargs):
        self.user_utils    = kwargs['user_utils']
        self.subvoat_utils = kwargs['subvoat_utils']

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('thread_uuid')
        parser.add_argument('direction')
        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()

        uuid_ = args.get('thread_uuid')

        user = self.user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))

        if not user:
            return {'error':'incorrect login'}

        try:
            direction = int(args.get('direction'))

        except Exception as e:
            return {'error':'incorrect direction'}
        
        status, result  = self.subvoat_utils.vote_thread(thread_uuid=uuid_, 
                                                         direction=direction, 
                                                         user_id=user.id)

        if status == True:
            return {'result':result}

    
        return {'error':result}

        
class VoteComment(Resource):
    def __init__(self, **kwargs):
        self.subvoat_utils = kwargs['subvoat_utils']
        self.user_utils    = kwargs['user_utils']

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('comment_uuid')
        parser.add_argument('direction')
        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()


        uuid_ = args.get('comment_uuid')
        user  = self.user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))

        if not user:
            return {'error':'incorrect login'}

        try:
            direction = int(args.get('direction'))

        except Exception as e:
            return {'error':'incorrect direction'}

        status, result = self.subvoat_utils.vote_comment(comment_uuid=uuid_, direction=direction, user_id=user.id)

        if status == True:
            return {'result':result}

        return {'error':result}

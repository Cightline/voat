
from flask_restful import Resource, reqparse

from voat_sql.utils.user    import UserUtils
from voat_sql.utils.subvoat import SubvoatUtils

class VoteThread(Resource):
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('thread_uuid')
        parser.add_argument('direction')
        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()

        user_utils    = UserUtils()
        subvoat_utils = SubvoatUtils()

        uuid_ = args.get('thread_uuid')

        user = user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))

        if not user:
            return {'error':'incorrect login'}

        try:
            direction = int(args.get('direction'))

        except Exception as e:
            return {'error':'incorrect direction'}
        
        status, result  = subvoat_utils.vote_thread(thread_uuid=args.get('thread_uuid'), 
                                                    direction=direction, 
                                                    user_id=user.id)

        if status == True:
            return {'result':result}

    
        elif status == False:
            return {'error': result}

        


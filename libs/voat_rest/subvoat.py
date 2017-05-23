import datetime

from flask_restful import Resource, reqparse

from voat_sql.utils.subvoat import SubvoatUtils
from voat_sql.utils.user    import UserUtils


class AddSubvoat(Resource):
    def post(self):
        subvoat_utils = SubvoatUtils()
        user_utils    = UserUtils()
        parser        = reqparse.RequestParser()

        parser.add_argument('subvoat_name')
        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()

        # authenticate first

        if 'username' not in args:
            return {'error':'no username given'}

        elif 'api_token' not in args:
            return {'error':'no api_token given'}

        elif 'subvoat_name' not in args:
            return {'error':'no subvoat_name given'}

        elif args['subvoat_name'] == None or args['subvoat_name'] == '':
            return {'error':'no subvoat_name given'}

       
        user = user_utils.authenticate_by_token(args['username'], args['api_token'])

        if not user:
            return {'error':'incorrect login'}

    
        # should validate the subvoat here


    
        # See if the subvoat exists
        if subvoat_utils.get_subvoat(args['subvoat_name']):
            return {'error':'subvoat already exists'}

    
        # If not create it (should probably add some rate-limiting or something around here)
        new_subvoat = subvoat_utils.create_subvoat_object(name=args['subvoat_name'],
                                                          owner_id=user.id,
                                                          creator_id=user.id,
                                                          creation_date=datetime.datetime.utcnow())
                                                          
                                                          
        if not subvoat_utils.add_subvoat(new_subvoat):
            return {'success':'subvoat created'}

        return {'error':'could not create subvoat'}
        



class ListSubvoats(Resource):
    def post(self):
        subvoat_utils = SubvoatUtils()
        parser        = reqparse.RequestParser()
        subvoats      = []
   
        # probably not gonna keep this
        data = subvoat_utils.get_all_subvoats()

        for s in data:
            subvoats.append(s.name)

        return {'result':subvoats}

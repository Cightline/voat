import datetime

from flask_restful import Resource, reqparse

from voluptuous import Schema, Required, All, Length, MultipleInvalid

from voat_sql.utils.subvoat import SubvoatUtils
from voat_sql.utils.user    import UserUtils
from voat_utils.config      import get_config

class AddSubvoat(Resource):
    def post(self):
        subvoat_utils = SubvoatUtils()
        user_utils    = UserUtils()
        parser        = reqparse.RequestParser()
        config        = get_config()

        parser.add_argument('subvoat_name')
        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()

        # authenticate first

        schema = Schema({

            Required('username'):     All(str, Length(min=config['min_length_username'])),
            Required('api_token'):    All(str, Length(min=config['min_length_api_token'])),
            Required('subvoat_name'): All(str, Length(min=config['min_length_subvoat_name'])),

            })

        
        try:
            # Just try the ones we need. 
            schema({'username':args.get('username'),
                    'api_token':args.get('api_token'),
                    'subvoat_name':args.get('subvoat_name')})

        except MultipleInvalid as e:
            # NEED BETTER ERROR MESSAGES, FIX THIS
            return {'error':'%s %s' % (e.msg, e.path)}

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
    def get(self):
        subvoat_utils = SubvoatUtils()
        parser        = reqparse.RequestParser()
        subvoats      = []
   
        # probably not gonna keep this
        data = subvoat_utils.get_all_subvoats()

        for s in data:
            subvoats.append(s.name)

        return {'result':subvoats}


class SubmitPost(Resource):
    def post(self):

        config = get_config()

        parser.add_argument('subvoat_name')
        parser.add_argument('title')
        parser.add_argument('body')
        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()


        schema = Schema({ 
            Required('subvoat_name'): All(str, Length(min=config['min_length_subvoat_name'])),
            
            # FIX ME: make this pull from the correct location (it should read the specific subvoat settings from the database)
            # So if there is a subvoat /v/test, it should read the settings out of the database, because that will be mod controlled. 
            Required('title'):        All(str, Length(min=5)),
            # Same here
            Required('body'):         All(str, Length(min=5))})


        

class GetPosts(Resource):
    def post(self):  
        config        = get_config()
        subvoat_utils = SubvoatUtils()
        parser        = reqparse.RequestParser()
        return_data   = []

        parser.add_argument('subvoat_name')

        args = parser.parse_args()

        schema = Schema({ Required('subvoat_name'): All(str, Length(min=config['min_length_subvoat_name']))})

        try:
            schema({'subvoat_name':args.get('subvoat_name')})

        except MultipleInvalid as e:
            return {'error':'%s %s' % (e.msg, e.path)}

        posts = subvoat_utils.get_posts(args['subvoat_name'])

        
        for p in posts:
            return_data.append(p)

        
        return {'result':return_data}

class GetComments(Resource):
    pass


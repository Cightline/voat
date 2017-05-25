import datetime

from flask_restful import Resource, reqparse

from voluptuous import Schema, Required, All, Length, MultipleInvalid

from voat_sql.utils.subvoat import SubvoatUtils
from voat_sql.utils.servers import ServerUtils
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
        user = user_utils.authenticate_by_token(args['username'], args['api_token'])
    
    
        if not user:
            return {'error':'incorrect login'}


        # should validate the subvoat here
        schema = Schema({Required('subvoat_name'): All(str, Length(min=config['min_length_subvoat_name']))})
        
        try:
            # Just try the ones we need. 
            schema({'subvoat_name':args.get('subvoat_name')})

        except MultipleInvalid as e:
            # NEED BETTER ERROR MESSAGES, FIX THIS
            return {'error':'%s %s' % (e.msg, e.path)}

    


    
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
        
        server_utils  = ServerUtils()
        subvoat_utils = SubvoatUtils()
        config        = get_config()
        parser        = reqparse.RequestParser()

        parser.add_argument('subvoat_name')
        parser.add_argument('title')
        parser.add_argument('body')
        parser.add_argument('username')
        parser.add_argument('api_token')
       
        args = parser.parse_args()

    
        
        result, message = subvoat_utils.add_post(args['subvoat_name'],
                                                 args['title'],
                                                 args['body'],
                                                 args['username'])


        if not result:
            return {'error':message}

        return {'result':message}


        

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


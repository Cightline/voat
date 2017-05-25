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

        config = get_config()

        parser.add_argument('subvoat_name')
        parser.add_argument('title')
        parser.add_argument('body')
        parser.add_argument('username')
        parser.add_argument('api_token')
        parser.add_argument('original_instance_address')
       
        args = parser.parse_args()

        # Data needs to be signed from whatever instance its coming from

        # at startup, we need to fetch the public keys if we do not already have them
        # contact server, ask for users public key
        # encrypt some random hash, send to server
        # original server sends back unencrypted hash 
        # server also sends users public key (data should be signed by server)
        # user is allowed to post
        # users message must be signed


        # check to see if original instance is whitelisted

        if not args['original_instance_address'] in whitelisted_instances:
            return {'error':'server is not whitelisted'}



        # see if we already have their public key, if not get it (this should be done at startup)



        # check to see if the message is signed by the original server






        # check to see if the users public key is banned


        # check to see if the message is signed by the user

    
        # post to board 



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


import datetime
import uuid

from flask_restful import Resource, reqparse

from voluptuous import Schema, Required, All, Length, MultipleInvalid

from voat_sql.utils.subvoat import SubvoatUtils
from voat_sql.utils.servers import ServerUtils
from voat_sql.utils.user    import UserUtils
from voat_utils.config      import get_config

from voat_sql.schemas import *

class AddSubvoat(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']


    def post(self):
        subvoat_utils = SubvoatUtils(self.db)
        user_utils    = UserUtils(self.db)
        parser        = reqparse.RequestParser()
        config        = get_config()

        parser.add_argument('subvoat_name')
        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()


        # authenticate first
        user = user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))
    
    
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
        if subvoat_utils.get_subvoat(args.get('subvoat_name')):
            return {'error':'subvoat already exists'}

    
        # If not create it (should probably add some rate-limiting or something around here)
        new_subvoat = subvoat_utils.create_subvoat_object(name=args.get('subvoat_name'),
                                                          owner_id=user.id,
                                                          creator_id=user.id,
                                                          creation_date=datetime.datetime.utcnow())
                                                          
                                                          
        if not subvoat_utils.add_subvoat(new_subvoat):
            return {'success':'subvoat created'}

        return {'error':'could not create subvoat'}
        



class ListSubvoats(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self):
        subvoat_utils = SubvoatUtils(self.db)
        parser        = reqparse.RequestParser()
        subvoats      = []
   
        # probably not gonna keep this
        data = subvoat_utils.get_all_subvoats()

        for s in data:
            subvoats.append(s.name)

        return {'result':subvoats}


class SubmitThread(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db'] 

    def post(self):
        subvoat_utils = SubvoatUtils(self.db)
        config        = get_config()
        parser        = reqparse.RequestParser()

        parser.add_argument('subvoat_name')
        parser.add_argument('title')
        parser.add_argument('body')
        parser.add_argument('username')
        parser.add_argument('api_token')
       
        args = parser.parse_args()

    
        
        result, message = subvoat_utils.add_thread(args['subvoat_name'],
                                                 args['title'],
                                                 args['body'],
                                                 args['username'])


        if not result:
            return {'error':message}

        return {'result':message}


        

class GetThreads(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self):  
        config        = get_config()
        subvoat_utils = SubvoatUtils(self.db)
        user_utils    = UserUtils(self.db)
        parser        = reqparse.RequestParser()
        return_data   = []

        parser.add_argument('subvoat_name')

        args   = parser.parse_args()
        schema = Schema({ Required('subvoat_name'): All(str, Length(min=config['min_length_subvoat_name']))})

        try:
            schema({'subvoat_name':args.get('subvoat_name')})

        except MultipleInvalid as e:
            return {'error':'%s %s' % (e.msg, e.path)}

        
        threads = subvoat_utils.get_all_threads(args['subvoat_name'])

       
        # see the thread schema in voat_sql/schemas/subvoat_schema.py
        # I convert the user_id to username
        for t in threads:
            user_status, user_result = user_utils.get_user_by_id(t.user_id)

            if user_status:
                username = user_result.username

            else:
                # NEED TO LOG THIS
                continue

            c = 0

            for v in t.votes:
                c += v.direction

            return_data.append({'uuid':t.uuid, 
                                'title':t.title,
                                'body':t.body,
                                'username':username,
                                'creation_date':t.creation_date.isoformat(),
                                'votes':c})

        
        return {'result':return_data}
    

class GetComments(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self):
        subvoat_utils = SubvoatUtils(self.db)
        user_utils    = UserUtils(self.db)
        parser = reqparse.RequestParser()

        parser.add_argument('thread_uuid')

        args        = parser.parse_args()
        return_data = []
    
        # check UUID length
        schema = Schema({ Required('thread_uuid'): All(str, Length(min=36, max=36))})
    
        try:
            schema({'thread_uuid':args.get('thread_uuid')})

        except MultipleInvalid as e:
            return {'error':'%s %s' % (e.msg, e.path)}


        comments = subvoat_utils.get_comments(args.get('thread_uuid'))

        # append the data to a list and return it. Also change the user_id to username.
        for comment in comments:
            u_status, u_result = user_utils.get_user_by_id(comment.user_id)

            c = 0
            
            if not u_status:
                # NEED TO LOG THIS 
                continue 
         
            # FIX: make this native SQL or something
            for v in comment.votes:
                c += v.direction
                
            
            return_data.append({'uuid':comment.uuid, 
                                'body':comment.body,
                                'username':u_result.username,
                                'creation_date':comment.creation_date.isoformat(),
                                'votes':c})


            
    
        return {'result':return_data}


class SubmitComment(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self):
        config        = get_config()
        parser        = reqparse.RequestParser()
        user_utils    = UserUtils(self.db)
        subvoat_utils = SubvoatUtils(self.db)

        parser.add_argument('username')
        parser.add_argument('api_token')
        parser.add_argument('body')
        parser.add_argument('thread_uuid')
        parser.add_argument('reply_to_uuid')

        args = parser.parse_args()

        # Validation setup
        uuid_schema = Schema({ Required('reply_to_uuid'): All(str, Length(min=36, max=36))})
        schema      = Schema({ Required('body'):          All(str, Length(min=config['min_length_comment_body'], 
                                                                          max=config['max_length_comment_body']))})


        # Validation
        try:
            schema({'body':args.get('body')})

            if args.get('reply_to_uuid'):
                uuid_schema({'reply_to_uuid': args.get('reply_to_uuid')})

        except MultipleInvalid as e:
            return {'error':'%s %s' % (e.msg, e.path)}



        user = user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))

        if not user:
            return {'error':'incorrect login'}

      
        # See if we are replying to a comment
        if args.get('reply_to_uuid'):
            status, result = subvoat_utils.add_comment(thread_uuid=args.get('thread_uuid'),     
                                                       reply_uuid=args.get('reply_to_uuid'),
                                                       body=args.get('body'), 
                                                       user_obj=user)

        else:
            status, result = subvoat_utils.add_comment(thread_uuid=args.get('thread_uuid'), 
                                                       body=args.get('body'), 
                                                       user_obj=user)

        if status == True:
            return {'result':'comment added'}

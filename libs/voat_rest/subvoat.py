import datetime
import uuid

from flask_restful import Resource, reqparse

from voat_sql.schemas import *


class AddSubvoat(Resource):
    def __init__(self, **kwargs):
        self.db            = kwargs['db']
        self.subvoat_utils = kwargs['subvoat_utils']
        self.user_utils    = kwargs['user_utils']
        self.config        = kwargs['cfg']
        self.validate      = kwargs['validate']


    def post(self):
        parser  = reqparse.RequestParser()

        parser.add_argument('subvoat_name')
        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()


        # authenticate first
        u_status, u_result = self.user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))

        if not u_status:
            return {'error':u_result}
    
    
        v_result, v_status = self.validate.subvoat_name(args.get('subvoat_name'))

        if not v_result:
            return {'error':v_status}

        # See if the subvoat exists
        if self.subvoat_utils.get_subvoat(args.get('subvoat_name')):
            return {'error':'subvoat already exists'}

    
        # If not create it (FIX: should probably add some rate-limiting or something around here)
        new_subvoat = self.subvoat_utils.create_subvoat_object(name=args.get('subvoat_name'), creation_date=datetime.datetime.utcnow())

        new_subvoat.owner_id   = u_result.id
        new_subvoat.creator_id = u_result.id
    
        # Just append the subvoat to the user object and commit  

        if not self.subvoat_utils.add_subvoat(new_subvoat):
            return {'result':'subvoat created'}

        return {'error':'could not create subvoat'}
        



class ListSubvoats(Resource):
    def __init__(self, **kwargs):
        self.db            = kwargs['db']
        self.subvoat_utils = kwargs['subvoat_utils']

    def get(self):
        parser        = reqparse.RequestParser()
        subvoats      = []
   
        # probably not gonna keep this
        data = self.subvoat_utils.get_all_subvoats()

        for s in data:
            subvoats.append({'name':s.name, 'owner':s.owner_id})

        return {'result':subvoats}


class SubmitThread(Resource):
    def __init__(self, **kwargs):
        self.db            = kwargs['db'] 
        self.subvoat_utils = kwargs['subvoat_utils']
        self.user_utils    = kwargs['user_utils']
        self.config        = kwargs['cfg']


    def post(self):
        parser        = reqparse.RequestParser()

        parser.add_argument('subvoat_name')
        parser.add_argument('title')
        parser.add_argument('body')
        parser.add_argument('username')
        parser.add_argument('api_token')
       
        args = parser.parse_args()

        
        u_status, u_result = self.user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))

        if not u_status:
            return {'error':u_result}
        
        status, result = self.subvoat_utils.add_thread(subvoat_name=args['subvoat_name'],
                                                       title=args['title'],
                                                       body=args['body'],
                                                       user_obj=u_result)


        if not status:
            return {'error':result}

        return {'result':result}


        

class GetThreads(Resource):
    def __init__(self, **kwargs):
        self.db            = kwargs['db']
        self.subvoat_utils = kwargs['subvoat_utils']
        self.user_utils    = kwargs['user_utils']
        self.config        = kwargs['cfg']
        self.validate      = kwargs['validate']


    def post(self):  
        parser        = reqparse.RequestParser()
        return_data   = []

        parser.add_argument('subvoat_name')
        parser.add_argument('page_start', default=0)
        parser.add_argument('page_end',   default=self.config['max_pages_per_request'])

        args   = parser.parse_args()

        start = args.get('page_start')
        end   = args.get('page_end')

        # FIX: move to SubvoatUtils
        v_status, v_result = self.validate.subvoat_name(args.get('subvoat_name'))

        if not v_status:
            return {'error':v_result}

        p_status, p_result = self.validate.page(start, end)

        if not p_status:
            return {'error':p_result}
        
        
        # check to see if the subvoat even exists
        if not self.subvoat_utils.get_subvoat(args.get('subvoat_name')):
            return {'error':'no such subvoat'}, 404


        t_status, t_result =  self.subvoat_utils.get_threads(args['subvoat_name'], start=start, end=end)

        if not t_status:
            return {'error':t_result}


        # see the thread schema in voat_sql/schemas/subvoat_schema.py
        # FIX: this could cause performance problems (user.id lookup)
        # FIX: just add the count to the subvoat when they voat (voat_count) and keep this so we know who voted where. 
        for t in t_result:
            
            c = 0

            for v in t.votes:
                c += v.direction

            return_data.append({'uuid':t.uuid, 
                                'local_id':t.id,
                                'title':t.title,
                                'body':t.body,
                                'username':t.creator.id,
                                'creation_date':t.creation_date.isoformat(),
                                'votes':c})

        
        return {'result':return_data}
    


class GetComments(Resource):
    def __init__(self, **kwargs):
        self.db            = kwargs['db']
        self.subvoat_utils = kwargs['subvoat_utils']
        self.user_utils    = kwargs['user_utils']
        self.validate      = kwargs['validate']

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('thread_uuid')

        args        = parser.parse_args()
        return_data = []
    
        
        v_status, v_result = self.validate.uuid(args.get('thread_uuid'))

        if not v_status:
            return {'error':v_result}

        comments = self.subvoat_utils.get_comments(args.get('thread_uuid'))

        # append the data to a list and return it. Also change the user_id to username.
        for comment in comments:
            u_status, u_result = self.user_utils.get_user_by_id(comment.user_id)

            c = 0
            
            if not u_status:
                # NEED TO LOG THIS 
                continue 
         
            # FIX: make this native SQL or something
            # thehivemind | should just be like len(select * from votes where up) - len(select * from votes where down)

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
        self.db            = kwargs['db']
        self.config        = kwargs['cfg']
        self.user_utils    = kwargs['user_utils']
        self.subvoat_utils = kwargs['subvoat_utils']
        self.validate      = kwargs['validate']


    def post(self):
        parser        = reqparse.RequestParser()

        parser.add_argument('username')
        parser.add_argument('api_token')
        parser.add_argument('body')
        parser.add_argument('thread_uuid')
        parser.add_argument('reply_to_uuid')

        args = parser.parse_args()

        
        # if they are replying to someone
        if args.get('reply_to_uuid'):
            uuid_status, uuid_result = self.validate.uuid(args.get('reply_to_uuid'))

            if not uuid_status:
                return {'error':uuid_result}


        cb_status, cb_result = self.validate.comment_body(args.get('body'))

        if not cb_status:
            return {'error':cb_result}


        user = self.user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))

        if not user:
            return {'error':'incorrect login'}

      
        # See if we are replying to a comment
        if args.get('reply_to_uuid'):
            status, result = self.subvoat_utils.add_comment(thread_uuid=args.get('thread_uuid'),     
                                                            reply_uuid=args.get('reply_to_uuid'),
                                                            body=args.get('body'), 
                                                            user_obj=user)

        else:
            status, result = self.subvoat_utils.add_comment(thread_uuid=args.get('thread_uuid'), 
                                                            body=args.get('body'), 
                                                            user_obj=user)

        if status == True:
            return {'result':'comment added'}

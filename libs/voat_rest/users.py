import datetime

from flask_restful import Resource, reqparse

from voluptuous import Schema, Required, All, Length, MultipleInvalid

from voat_sql.utils.servers import ServerUtils
from voat_sql.utils.user    import UserUtils
from voat_utils.config      import get_config

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


class SubmitPost(Resource):
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

    
        
        result, message = subvoat_utils.add_post(args['subvoat_name'],
                                                 args['title'],
                                                 args['body'],
                                                 args['username'])


        if not result:
            return {'error':message}

        return {'result':message}


        

class GetUser(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self):  
        config        = get_config()
        subvoat_utils = UserUtils(self.db)
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


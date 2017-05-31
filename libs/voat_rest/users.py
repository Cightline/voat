import datetime

from flask_restful import Resource, reqparse

from voluptuous import Schema, Required, All, Length, MultipleInvalid


class ListSubvoats(Resource):
    def __init__(self, **kwargs):
        self.subvoat_utils = kwars['subvoat_utils']

    def get(self):
        parser        = reqparse.RequestParser()
        subvoats      = []
   
        # probably not gonna keep this
        data = self.subvoat_utils.get_all_subvoats()

        for s in data:
            subvoats.append(s.name)

        return {'result':subvoats}


class SubmitPost(Resource):
    def __init__(self, **kwargs):
        self.subvoat_utils = kwargs['subvoat_utils']

    def post(self):
        parser        = reqparse.RequestParser()

        parser.add_argument('subvoat_name')
        parser.add_argument('title')
        parser.add_argument('body')
        parser.add_argument('username')
        parser.add_argument('api_token')
       
        args = parser.parse_args()

        # FIX: NEED AUTHENTICATION
        
        result, message = subvoat_utils.add_post(args['subvoat_name'],
                                                 args['title'],
                                                 args['body'],
                                                 args['username'])


        if not result:
            return {'error':message}

        return {'result':message}


        

class GetUser(Resource):
    def __init__(self, **kwargs):
        self.config        = kwargs['cfg']
        self.subvoat_utils = kwargs['subvoat_utils']


    def get(self):  
        parser        = reqparse.RequestParser()
        return_data   = []

        parser.add_argument('subvoat_name')

        args = parser.parse_args()

        schema = Schema({ Required('subvoat_name'): All(str, Length(min=self.config['min_length_subvoat_name']))})

        try:
            schema({'subvoat_name':args.get('subvoat_name')})

        except MultipleInvalid as e:
            return {'error':'%s %s' % (e.msg, e.path)}

        posts = self.subvoat_utils.get_posts(args['subvoat_name'])

        
        for p in posts:
            return_data.append(p)

        
        return {'result':return_data}



class GetComments(Resource):
    pass



from flask_restful import Resource, reqparse

from voat_sql.utils.user import UserUtils
from voat_utils.config   import get_config, write_value

class ChangeSetting(Resource):
    def __init__(**kwargs):
        self.db         = kwargs['db']
        self.user_utils = kwargs['user_utils']
        self.config     = kwargs['cfg']

    def post(self):
        parser = reqparse.RequestParser() 
        
        parser.add_argument('setting')
        parser.add_argument('value')
        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()
        user = self.user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))

        if not user:
            # FIX: should probably log this
            # FIX: should probably rate limit this as well
            return {'error':'incorrect login'}
    
        # Gonna put get_config here, instead of up there. That way it doesn't load everytime someone tries to access the admin API. 
        setting = args.get('setting')
        value   = args.get('value')

        if setting not in self.config.keys():
            return {'error':'setting not in config'}
       
        # FIX: need full config object not just get_config()
        #self.config.write_value(setting, value)

        return {'result':'setting updated'}




class GetSettings(Resource):
    def __init__(**kwargs):
        self.db         = kwargs['db']
        self.user_utils = kwargs['user_utils']
        self.config     = kwargs['cfg']

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username')
        parser.add_argument('api_token')

        args = parser.parse_args()

        user = self.user_utils.authenticate_by_token(args.get('username'), args.get('api_token'))

        if not user:
            return {'error':'incorrect login'}

        return {'result': self.config}



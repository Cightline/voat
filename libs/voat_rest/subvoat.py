from flask_restful import Resource, reqparse

from voat_sql.utils.subvoat import SubvoatUtils


class AddSubvoat(Resource):
    def post(self):
        subvoat_utils = SubvoatUtils()
        parser        = reqparse.RequestParser()

        parser.add_argument('subvoat_name')
        parser.add_argument('username')
        parser.add_argument('api_key')

        args = parser.parse_args()

        # authenticate first

        if 'username' not in args:
            return {'error':'no username given'}

        elif 'api_token' not in args:
            return {'error':'no api_token given'}

        elif 'subvoat_name' not in args:
            return {'error':'no subvoat_name given'}

       
    
        # should validate the subvoat here


    
        # See if the subvoat exists
        if subvoat_utils.get_subvoat(args['subvoat_name']):
            return {'error':'subvoat already exists'}

    
        
        
        

        # If not create it (should probably add some rate-limiting or something around here)



class GetSubvoat(Resource):
    def post(self):
        parser = reqparse.RequestParser()
    

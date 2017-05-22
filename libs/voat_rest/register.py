from flask_restful import Resource, Api, reqparse

class Register(Resource):
    def post(self):
        parser = reqparser.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')


        args = parser.parse_args()

        if 'email' not in args:
            return {'error':'no email given'}

        elif 'password' not in args:
            return {'error':'no password given'}

        elif args['password'] == None or args['password'] == '':
            return {'error':'password has no length'}


    
        # check to make sure doesn't exist

        # hash the password

        # validate it

        # commit the changes

import uuid
import datetime

from flask_restful    import Resource, Api, reqparse
from Crypto.PublicKey import RSA
from Crypto           import Random

from passlib.apps import custom_app_context as pwd_context

from voat_sql.utils.user import UserUtils
from voat_sql.utils.db   import get_db


class Register(Resource):
    def post(self):

        user_utils = UserUtils()
        db         = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')


        args = parser.parse_args()

        if 'username' not in args:
            return {'error':'no username given'}

        elif 'password' not in args:
            return {'error':'no password given'}

        elif args['password'] == None or args['password'] == '':
            return {'error':'password has no length'}


    
        # check to make sure doesn't exist
        result, user = user_utils.get_user(args['username'])

        if result == False:
            return {'error': user}

        if result == True and user != None:
            print('USER',user)
            return {'error':'user already exists'}

       
        # Generate the keys (should probably move this to a microservice)
        # http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/#a_3
        
        random_gen = Random.new().read

        key = RSA.generate(1024, random_gen)


        # initilize the user
        u_password    = args['password']
        u_username    = args['username']
        u_hash        = pwd_context.encrypt(u_password)
        u_public_key  = key.publickey().exportKey()
        u_private_key = key.exportKey()
        u_api_token   = str(uuid.uuid4())
               
        
        new_user = user_utils.create_user_object(password_hash=u_hash,
                                                 username=u_username,
                                                 # make this UTC
                                                 creation_time=datetime.datetime.now(),
                                                 public_key=u_public_key,
                                                 private_key=u_private_key,
                                                 api_token=u_api_token)


        db.session.add(new_user)

        # prob need some error handling here
        db.session.commit()

        return {'success':'user created'}


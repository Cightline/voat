
# May use Celery here
#http://www.prschmid.com/2013/04/using-sqlalchemy-with-celery-tasks.html 

from flask  import Flask
#from celery import Celery

from flask_restful import Resource, reqparse, Api

from voat_utils             import config
from voat_sql.utils.servers import ServerUtils

app   = Flask(__name__)
api   = Api(app)
#c_app = Celery('tasks', broker='redis://localhost:6379')

app.config.update(config.get_config())

class UpdatePost(Resource):
    def post(self):

        server_utils = ServerUtils()

        parser = reqparse.RequestParser()

        parser.add_argument('subvoat_name')
        parser.add_argument('user_id')
        parser.add_argument('original_instance')
        parser.add_argument('title')
        parser.add_argument('body')
        parser.add_argument('signature')


        args = parser.parse_args()
    
        # DO IP/DNS LOOKUP HERE

        
        # check against the whitelist
        if args['original_instance'] not in app.config['whitelisted_servers']:
            return {'error':'server not whitelisted'}


        # verify signature 
        server = server_utils.get_public_key(args['original_instance'])
        
        
        if not server:
            return {'error':'no public key for this server'}


        print(server.public_key)


        # add to database







api.add_resource(UpdatePost, '/update_data')


if __name__ == '__main__':
    app.run(debug=config.get_config()['debug'], port=8000)

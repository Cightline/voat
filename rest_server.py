
from flask import Flask
from flask_restful import  Api
from flask_cors import CORS, cross_origin

# API classes
from voat_rest  import register
from voat_rest  import authenticate
from voat_rest  import subvoat
from voat_rest  import utils
from voat_rest  import vote
from voat_utils import config




# Need a logger

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.update(config.get_config())


api.add_resource(authenticate.Authenticate, '/authenticate')
api.add_resource(register.Register,         '/register')
api.add_resource(subvoat.AddSubvoat,        '/create_subvoat')
api.add_resource(subvoat.ListSubvoats,      '/list_subvoats')
api.add_resource(subvoat.GetThreads,        '/get_threads')
api.add_resource(subvoat.SubmitThread,      '/submit_thread')
api.add_resource(vote.VoteThread,           '/vote_thread')
api.add_resource(subvoat.GetComments,       '/get_comments')
api.add_resource(subvoat.SubmitComment,     '/submit_comment')
api.add_resource(utils.GetPublicKey,        '/get_public_key')


# Debugging
if __name__ == '__main__':
    # Make it pull all of these options from the config
    app.run(host="0.0.0.0", port=8080, debug=config.get_config()['debug'])
         
        

        

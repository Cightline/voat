
import json

from flask import Flask
from flask_restful import Resource, Api, reqparse

from passlib.apps import custom_app_context as pwd_context

from voat_sql.db_connect import Connect

# API classes
from voat_rest  import register
from voat_rest  import authenticate
from voat_rest  import subvoat
from voat_utils import config




# Need a logger

app = Flask(__name__)
api = Api(app)

app.config.update(config.get_config())



api.add_resource(authenticate.Authenticate, '/authenticate')
api.add_resource(register.Register,         '/register')
api.add_resource(subvoat.AddSubvoat,        '/create_subvoat')
api.add_resource(subvoat.ListSubvoats,      '/list_subvoats')


# Debugging
if __name__ == '__main__':
    app.run(debug=True)
         
        

        

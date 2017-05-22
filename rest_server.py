
import json

from flask import Flask
from flask_restful import Resource, Api, reqparse

from voat_sql.db_connect import Connect

from voat_rest import register
from voat_rest import authenticate


from passlib.apps import custom_app_context as pwd_context


# Need a logger

app = Flask(__name__)
api = Api(app)


with open('/etc/voat/config/config.json') as cfg:
    config = json.load(cfg)


app.config.update(config)


db = Connect(app.config['SQLALCHEMY_DATABASE_URI'])



api.add_resource(authenticate.Authenticate, '/authenticate')
api.add_resource(register.Register,         '/register')



# Debugging
if __name__ == '__main__':
    app.run(debug=True)
         
        

        

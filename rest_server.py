
import json

from flask import Flask
from flask_restful import Resource, Api, reqparse

# THESE NEED TO BE "INSTALLED" RATHER THAN IMPORTING FROM THE CURRENT DIRECTORY. 
from voat_sql.db_connect import Connect


from passlib.apps import custom_app_context as pwd_context



app = Flask(__name__)
api = Api(app)


# THIS NEEDS TO BE A SEPERATE MODULE/CLASS (AND WRITTEN SLIGHTLY BETTER)
# Should I put the config somewhere else?
with open('config/config.json') as cfg:
    config = json.load(cfg)


app.config.update(config)


db = Connect(app.config['SQLALCHEMY_DATABASE_URI'])

# Need a logger

class Authenticate(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # prob need some sort of max length limit
        parser.add_argument('username')
        parser.add_argument('password')



        
api.add_resource(Authenticate, '/authenticate')




# Debugging
if __name__ == '__main__':
    app.run(debug=True)
         
        

        

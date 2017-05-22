from flask_restful import Resource, Api, reqparse

from voat_sql.utils.user import UserUtils

class Authenticate(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # prob need some sort of max length limit
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()

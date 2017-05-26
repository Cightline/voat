from passlib.apps  import custom_app_context as pwd_context
from voluptuous     import Schema, Required, All, Length, MultipleInvalid

from voat_sql.utils import db
from voat_utils.config import get_config

# PAY ATTENTION WHEN MESSING WITH THIS. 

class UserUtils():
    def __init__(self):
        self.db      = db.get_db()
        self.config  = get_config()
        self.classes = self.db.base.classes
   

    # Returns a user object
    def create_user_object(self, **kwargs):
        return self.classes.users(**kwargs)

   
    # Returns a list [result, data/object/error_message]
    def get_user(self, username):

        schema = Schema({ Required('username'): All(str, Length(min=self.config['min_length_username']))})

        try:
            schema({'username':username})

        except MultipleInvalid as e:
            return [False, '%s %s' % (e.msg, e.path)]

        return [True, self.db.session.query(self.classes.users).filter(self.classes.users.username == username).first()]

    def get_user_by_id(self, user_id):

        # ADD SCHEMA TYPE INTEGER HERE
        
        return [True, self.db.session.query(self.classes.users).filter(self.classes.users.id == user_id).first()]

    def authenticate_by_password(self, username, password):
        result, user = self.get_user(username)

        if result == False:
            # Returns the error message
            return [False, user]

        
        if user:
            if pwd_context.verify(password, user.password_hash):
                return [True, user]

        return [False, False]


    def authenticate_by_token(self, username, api_token):
        result, user = self.get_user(username)

        if result == False:
            return False

        elif not user:
            return False

        elif user.api_token == user.api_token:
            return user

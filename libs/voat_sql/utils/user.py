import uuid
import datetime

from passlib.apps           import custom_app_context as pwd_context
from voluptuous             import Schema, Required, All, Length, MultipleInvalid
from dateutil.relativedelta import relativedelta
import transaction

from voat_sql.utils    import db
from voat_utils.config import get_config

from voat_sql.schemas import * 

# PAY ATTENTION WHEN MESSING WITH THIS. 

class UserUtils():
    def __init__(self, db):
        self.db      = db
        self.config  = get_config()
        self.session = db.session()
   

    # Returns a user object
    def create_user_object(self, **kwargs):
        return User(**kwargs)
        #return self.classes.user(**kwargs)

    
    def add_user(self, password, username):

        schema = Schema({ Required('username'): All(str, Length(min=self.config['min_length_username'])),
                          Required('password'): All(str, Length(min=self.config['min_length_password']))})


        try:
            schema({'username':username, 'password':password})

        except MultipleInvalid as e:
            return [False, '%s %s' % (e.msg, e.path)]

        
        u_status, u_result = self.get_user(username)

        if not u_status:
            return [False, u_result]

        
        elif u_status and u_result:
            return [False, 'user already exists']


        now              = datetime.datetime.utcnow()
        password_hash    = pwd_context.encrypt(password)
        api_token        = str(uuid.uuid4())
        token_expiration = now + relativedelta(months=self.config['months_to_token_expiration'])



        new_user = self.create_user_object(password_hash=password_hash, 
                                           username=username, 
                                           registration_date=now, 
                                           api_token=api_token,
                                           verified=False)

        self.session.add(new_user)

        status = transaction.commit()

        # FIX: log this
        if not status:
            return [True, 'user created']

        return [False, 'unable to create user']


   
    # Returns a list [result, data/object/error_message]
    def get_user(self, username):

        schema = Schema({ Required('username'): All(str, Length(min=self.config['min_length_username']))})

        try:
            schema({'username':username})

        except MultipleInvalid as e:
            return [False, '%s %s' % (e.msg, e.path)]

        return [True, self.session.query(User).filter(User.username == username).first()]
        #return [True, self.db.session.query(self.classes.user).filter(self.classes.user.username == username).first()]


    def get_user_by_id(self, user_id):

        # ADD SCHEMA TYPE INTEGER HERE
        
        return [True, self.session.query(User).filter(User.id == user_id).first()]
        #return [True, self.db.session.query(self.classes.user).filter(self.classes.user.id == user_id).first()]

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

import uuid
import datetime

from passlib.apps           import custom_app_context as pwd_context
from voluptuous             import Schema, Required, All, Length, MultipleInvalid
from dateutil.relativedelta import relativedelta
import transaction

from voat_sql.schemas import * 

# PAY ATTENTION WHEN MESSING WITH THIS. 

class UserUtils():
    def __init__(self, db, config, validation_obj):
        self.db       = db
        self.config   = config 
        self.session  = db.session()
        self.validate = validation_obj
   

    # Returns a user object
    def create_user_object(self, **kwargs):
        return User(**kwargs)

    
    def add_user(self, password, username):

        v_status, v_result = self.validate.user(username=username, password=password)

        if not v_status:
            return [v_status, v_result]
        
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
        
        u_status, u_result = self.validate.username(username)

        if not u_status:
            return [u_status, u_result]

        return [True, self.session.query(User).filter(User.username == username).first()]


    def get_user_by_id(self, user_id):

        # ADD SCHEMA TYPE INTEGER HERE
        
        return [True, self.session.query(User).filter(User.id == user_id).first()]

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

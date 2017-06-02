import uuid
import datetime


import transaction
from passlib.apps           import custom_app_context as pwd_context
from dateutil.relativedelta import relativedelta

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
        
        u_status, u_result  = self.get_user(username)

        if u_status == True and u_result:
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


   
    def get_user_by_id(self, user_id):

        return [True, self.session.query(User).filter(User.id == user_id).first()]


    def get_user(self, username):
        result = self.session.query(User).filter(User.username == username).first()

        return [True, result]


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
        '''Returns [False, error_message] if given an incorrect username and api_token. 
           Otherwise it returns [True, user]'''

        u_status, u_result = self.validate.user(username, api_token=api_token)

        if not u_status:
            return [False, u_result]

        g_status, g_result = self.get_user(username)

        if not g_status:
            return [False, 'incorrect login']


        elif g_result.api_token == api_token:
            return [True, g_result]


        return [False, 'incorrect login']

from passlib.apps  import custom_app_context as pwd_context

from voat_sql.utils import db


class UserUtils():
    def __init__(self):
        self.db      = db.get_db()
        self.classes = self.db.base.classes
   

    # Returns a user object
    def create_user_object(self, **kwargs):
        return self.classes.users(**kwargs)

   
    # Returns a user object 
    def get_user(self, username):
        return self.db.session.query(self.classes.users).filter(self.classes.users.username == username).first()
    

    def authenticate_by_password(self, username, password):
        user = self.get_user(username)

        if not user:
            return False

        if pwd_context.verify(password, user.password_hash):
            return user


    def authenticate_by_token(self, username, api_token):
        user = self.get_user(username)

        if not user:
            return False

        if user.api_token == user.api_token:
            return user


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
    

    
        

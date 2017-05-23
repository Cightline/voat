
from voat_sql.utils import db



class SubvoatUtils():
    def __init__(self):
        self.db      = db.get_db()
        self.classes = self.db.base.classes
   

    # Returns a user object
    def create_subvoat_object(self, **kwargs):
        return self.classes.subvoat(**kwargs)

   
    # Returns a user object 
    def get_subvoat(self, subvoat_name):
        return self.db.session.query(self.classes.subvoat).filter(self.classes.subvoat.name == subvoat_name).first()
    

    
        

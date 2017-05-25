
# These classes mainly deal with database interaction

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
   

    def get_all_subvoats(self):
        return self.db.session.query(self.classes.subvoat).all()

    
    def add_subvoat(self, new_subvoat):
        self.db.session.add(new_subvoat)
        
        result = self.db.session.commit()

        return result



    # Make one that orders by date, with a limit
    def get_posts(self, subvoat_name):
        subvoat =  self.db.session.query(self.classes.subvoat).filter(self.classes.subvoat.name == subvoat_name).first()

        #print(dir(subvoat.posts_collection))

        if subvoat:
            return subvoat.posts_collection 

        return []

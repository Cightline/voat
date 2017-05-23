from voat_sql import *

# I'll have to look more into this, there may be a better way. 

    

class SubVoat(Base):
    __tablename__ = 'subvoat'

    id            = Column(Integer, primary_key=True)
    name          = Column(String(200))
    posts         = relationship('Post')


class Post(Base):
    __tablename__ = 'posts'
    
    id            = Column(Integer, primary_key=True)
    value         = Column(String(200))
    # Change this to the users ID, that way it can follow nick changes.
    user_id       = Column(Integer)
    creation_date = Column(DateTime)
    subvoat_id    = Column(Integer, ForeignKey('subvoat.id'))



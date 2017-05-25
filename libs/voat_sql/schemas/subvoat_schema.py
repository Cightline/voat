from voat_sql import *

# I'll have to look more into this, there may be a better way. 

    

class SubVoat(Base):
    __tablename__ = 'subvoat'

    id            = Column(Integer, primary_key=True)
    name          = Column(String(200), unique=True, nullable=False)
    posts         = relationship('Post', backref=backref('posts', lazy='noload'))
    owner_id      = Column(Integer)
    creator_id    = Column(Integer)
    creation_date = Column(DateTime)


class Post(Base):
    __tablename__ = 'posts'
    
    id            = Column(Integer, primary_key=True)
    value         = Column(String(200))
    title         = Column(String(200))
    body          = Column(String(200))
    user_id       = Column(Integer)
    creation_date = Column(DateTime)
    subvoat_id    = Column(Integer, ForeignKey('subvoat.id'))



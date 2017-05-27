from voat_sql import *

# I'll have to look more into this, there may be a better way. 

    

class SubVoat(Base):
    __tablename__ = 'subvoat'


    id            = Column(Integer, primary_key=True)
    name          = Column(String(200), unique=True, nullable=False)
    threads       = relationship('Thread', backref=backref('thread', lazy='noload'))
    owner_id      = Column(Integer)
    creator_id    = Column(Integer)
    creation_date = Column(DateTime)


class Thread(Base):
    __tablename__ = 'thread'
    
    # NEED A CUSTOM COLUMN TYPE FOR UUIDs
    uuid          = Column(String(200), primary_key=True)
    value         = Column(String(200))
    title         = Column(String(200))
    body          = Column(String(200))
    user_id       = Column(Integer)
    creation_date = Column(DateTime)
    subvoat_id    = Column(Integer, ForeignKey('subvoat.id'))



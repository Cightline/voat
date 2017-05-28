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
    
    uuid          = Column(String(200), primary_key=True)
    title         = Column(String(200))
    body          = Column(String(200))
    user_id       = Column(Integer)
    creation_date = Column(DateTime)
    subvoat_id    = Column(Integer, ForeignKey('subvoat.id'))


class Comment(Base):
    __tablename__ = 'comment'

    uuid          = Column(String(200),  primary_key=True)
    body          = Column(String(5000))
    user_id       = Column(Integer)
    creation_date = Column(DateTime)
    thread_uuid   = Column(String, ForeignKey('thread.uuid'))
    reply_uuid    = Column(String(200))


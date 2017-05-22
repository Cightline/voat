# THIS IS A SAMPLE FROM ANOTHER PROJECT I WAS WORKING ON.

from . import *

from sqlalchemy.schema import Table

association_table = Table('association', Base.metadata,
        Column('users',  Integer, ForeignKey('users.id')),
        Column('groups', Integer, ForeignKey('groups.id')),)

class Group(Base):
    __tablename__ = "groups"
   
    id          = Column(Integer, primary_key=True)
    name        = Column(String(200), unique=True, nullable=False)
    creator_id  = Column(Integer)
    users       = relationship('User', secondary=association_table, back_populates='groups')




class User(Base):
    __tablename__ = 'users'
    
    id          = Column(Integer, primary_key=True)
    c_time      = Column(DateTime)
    email       = Column(String(200), unique=True)
    api_token   = Column(String(200))
    pass_hash   = Column(String(200))
    username    = Column(String(200), unique=True, nullable=False)
    verified    = Column(Boolean)
    admin       = Column(Boolean)
    #groups_     = Column(Integer, ForeignKey('groups.id'))
    groups     = relationship("Group", secondary=association_table, back_populates='users')





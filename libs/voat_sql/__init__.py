from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Time, DateTime, create_engine, ForeignKey, Boolean, Float
from sqlalchemy.orm import Session, backref, relationship

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

Base = declarative_base()


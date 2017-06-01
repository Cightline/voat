from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import *
from zope.sqlalchemy import register

# http://docs.sqlalchemy.org/en/latest/core/pooling.html

class Connect():
    def __init__(self, db_path):
        self.base   = declarative_base()
        self.engine = create_engine(db_path, convert_unicode=True, pool_size=100)

        #self.base.prepare(self.engine, reflect=True)
        self.session = scoped_session(sessionmaker(bind=self.engine, twophase=True, extension=ZopeTransactionExtension()))
        #self.session = scoped_session(sessionmaker(bind=self.engine))

        register(self.session, keep_session=True)

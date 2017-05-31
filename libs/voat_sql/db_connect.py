from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from zope.sqlalchemy import ZopeTransactionExtension

class Connect():
    def __init__(self, db_path):
        self.base   = automap_base()
        self.engine = create_engine(db_path, convert_unicode=True)

        self.base.prepare(self.engine, reflect=True)
        session_factory = sessionmaker(bind=self.engine, extension=ZopeTransactionExtension())
        #self.session = scoped_session(Session(self.engine))

        self.session = scoped_session(session_factory)

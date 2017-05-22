from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

class Connect():
    def __init__(self, db_path):
        self.base   = automap_base()
        self.engine = create_engine(db_path, convert_unicode=True)

        self.base.prepare(self.engine, reflect=True)
        self.session = Session(self.engine)

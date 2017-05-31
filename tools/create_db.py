import json
import os

from sqlalchemy.ext.automap     import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import create_engine, MetaData
from sqlalchemy_utils.functions import database_exists, drop_database

from voat_sql.schemas    import *
from voat_sql.db_connect import Connect
from voat_sql            import initialize_sql


class CreateDB():
    def __init__(self, db_path):
        #self.base    = automap_base()
        self.db_path = db_path
        self.engine  = create_engine(db_path, echo=True)
        self.engine.connect()
        self.metadata = MetaData()


    def create(self):
        #self.engine.execute('create database voat')
        #self.base.metadata.bind = self.engine
        #self.base.metadata.create_all(self.engine)

        self.metadata.reflect(self.engine)

        self.base = automap_base(metadata=self.metadata)



if __name__ == '__main__':
    # Reads the config file, creates the database, checks to make sure it was actually created
    
    with open('/etc/voat/config/config.json') as c:
        cfg     = json.load(c)
        db_path = cfg['SQLALCHEMY_DATABASE_URI']

        #try:
        #    if database_exists(db_path):
        #        confirm = input('database already exists, delete anyways? [y/n]: ').lower().strip()

        #        if confirm != 'y' and confirm.lower() != 'yes':
        #            exit()

        #        drop_database(db_path)

        #except FileNotFoundError as e:
        #    pass

        cdb     = CreateDB(db_path)
        result  = cdb.create()

        if result == None:
            print('database created')

        else:
            print('unable to create the database')
            exit()




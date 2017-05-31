
from voat_sql.db_connect import Connect
from voat_utils          import config

def get_db():
    return Connect(config.get_config()['SQLALCHEMY_DATABASE_URI'])




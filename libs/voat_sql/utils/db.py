
from voat_sql.db_connect import Connect
from voat_utils          import config

# Probably not the best way of doing this, I bet it reads the config for every request. 
def get_db():
    return Connect(config.get_config()['SQLALCHEMY_DATABASE_URI'])

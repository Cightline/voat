
from sqlalchemy.schema import Table

from voat_sql import *

class User(Base):
    __tablename__ = 'users'

    id            = Column(Integer, primary_key=True)
    creation_time = Column(DateTime)
    username      = Column(String(200), unique=True, nullable=False)
    email         = Column(String(200), unique=True)
    api_token     = Column(String(200))
    password_hash = Column(String(200))
    banned        = Column(Boolean)



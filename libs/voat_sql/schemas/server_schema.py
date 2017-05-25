from voat_sql import *

class Servers(Base):
    __tablename__ = 'servers'

    id            = Column(Integer, primary_key=True)
    address       = Column(String(200), unique=True)
    public_key    = Column(String(200))



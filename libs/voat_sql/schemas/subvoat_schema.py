
from sqlalchemy.schema import Table

# I'll have to look more into this, there may be a better way. 

    

class SubVoat(Base):
    __tablename__ = 'subvoat'

    id            = Column(Integer, primary_key=True)
    name          = Column(String(200))
    posts         = relationship('Post')


class Post(Base):
    __tablename__ = 'posts'

    value         = Column(String(200))
    username      = Column(String(200))
    creation_date = Column(DateTime)
    subvoat_id    = Column(Integer, ForeignKey('subvoat.id'))



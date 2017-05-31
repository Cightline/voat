from voat_sql import *

# I'll have to look more into this, there may be a better way. 

class SubVoat(Base):
    __tablename__ = 'subvoat'
    
    id            = Column(Integer, primary_key=True)
    name          = Column(String(200), unique=True, nullable=False)
    creation_date = Column(DateTime)
    # FIX: make owner_id/creator_id a one-to-one relationship
    creator_id    = Column(Integer)
    threads       = relationship('Thread',    backref=backref('thread',    lazy='noload'))
    moderators    = relationship('Moderator', backref=backref('moderator', lazy='noload'))
    admins        = relationship('SubAdmin',     backref=backref('sub_admin',     lazy='noload'))
    owner_id      = Column(Integer, ForeignKey('user.id'))


class Thread(Base):
    __tablename__ = 'thread'
    
    uuid          = Column(String(200), primary_key=True)
    title         = Column(String(200))
    body          = Column(String(200))
    user_id       = Column(Integer)
    creation_date = Column(DateTime)
    subvoat_id    = Column(Integer, ForeignKey('subvoat.id'))
    votes         = relationship('ThreadVote',    backref=backref('thread_vote',    lazy='noload'))
    comments      = relationship('Comment',       backref=backref('comment', lazy='noload'))


class Comment(Base):
    __tablename__ = 'comment'

    uuid          = Column(String(200),  primary_key=True)
    body          = Column(String(5000))
    user_id       = Column(Integer)
    creation_date = Column(DateTime)
    thread_uuid   = Column(String, ForeignKey('thread.uuid'))
    reply_uuid    = Column(String(200))
    is_edit       = Column(Boolean, default=False)
    # for editing  
    original_uuid = Column(String(200))
    votes         = relationship('CommentVote', backref=backref('comment_vote', lazy='noload'))



class User(Base):
    __tablename__ = 'user'

    id                = Column(Integer, primary_key=True)
    registration_date = Column(DateTime)
    username          = Column(String(200), unique=True, nullable=False)
    email             = Column(String(200), unique=True)
    password_hash     = Column(String(200))
    api_token         = Column(String(200))
    token_expiration  = Column(DateTime)
    banned            = Column(Boolean)
    verified          = Column(Boolean, default=False)
    site_admin        = Column(Boolean, default=False)
    
    
    subvoat_admin     = relationship('SubAdmin',  backref=backref('user_sub_admin', lazy='noload'))
    subvoat_moderator = relationship('Moderator', backref=backref('user_moderator', lazy='noload'))
    owned_subvoats    = relationship('SubVoat',   backref=backref('subvoat',   lazy='noload'))
    subscribed_subs   = relationship('Sub',       backref=backref('sub',       lazy='noload'))


class SubAdmin(Base):
    __tablename__ = 'sub_admin'

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('user.id'))
    subvoat_id = Column(Integer, ForeignKey('subvoat.id'))


class Moderator(Base):
    __tablename__ = 'moderator'
    id           = Column(Integer, primary_key=True)
    user_id      = Column(Integer, ForeignKey('user.id'))
    subvoat_id   = Column(Integer, ForeignKey('subvoat.id'))


class Sub(Base):
    __tablename__ = 'sub'
    
    user_id    = Column(Integer, ForeignKey('user.id'), primary_key=True)
    subvoat_id = Column(Integer, ForeignKey('subvoat.id'))


class Server(Base):
    __tablename__ = 'server'

    id         = Column(Integer, primary_key=True)
    address    = Column(String(200), unique=True)
    public_key = Column(String(200), unique=True)


class CommentVote(Base):
    __tablename__ = 'comment_vote'

    id           = Column(Integer, primary_key=True)
    # make one-to-one relationship
    user_id      = Column(Integer)
    direction    = Column(Integer, default=0)
    comment_uuid = Column(String, ForeignKey('comment.uuid'))


class ThreadVote(Base):
    __tablename__ = 'thread_vote'

    id           = Column(Integer, primary_key=True)
    # make one-to-one relationship
    user_id      = Column(Integer)
    direction    = Column(Integer, default=0)
    thread_uuid  = Column(String, ForeignKey('thread.uuid'))

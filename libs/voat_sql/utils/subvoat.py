
# These classes mainly deal with database interaction

import datetime
import json
import uuid

import requests
import transaction

from voat_utils.updater  import send_thread

# testing something
from voat_sql.schemas import *


class SubvoatUtils():
    def __init__(self, db, config, user_utils, validation_obj):
        self.db         = db
        self.config     = config
        self.session    = db.session()
        self.user_utils = user_utils
        self.validate   = validation_obj
   

    # Returns a user object (see the schemas)
    def create_subvoat_object(self, **kwargs):
        return SubVoat(**kwargs)


    def create_thread_object(self, **kwargs):
        return Thread(**kwargs)


    def create_comment_object(self, **kwargs):
        return Comment(**kwargs)


    # Returns a user object 
    def get_subvoat(self, subvoat_name):
        return self.session.query(SubVoat).filter(SubVoat.name == subvoat_name).first()


    def get_comments(self, thread_uuid):
        
        return self.session.query(Thread).filter(Thread.uuid == thread_uuid).first().comments


    def get_all_subvoats(self):
        return self.session.query(SubVoat).all()


   

    def add_subvoat(self, subvoat_obj):
        ''' Bascially just commits, trying to keep db.session out of the main functions'''

        self.session.add(subvoat_obj)
        
        result = transaction.commit()

        return result


    def add_comment(self, thread_uuid, body, user_obj, reply_uuid=None):
        
        thread = self.get_thread_by_uuid(thread_uuid)

        if not thread:
            return [False, 'no such thread']

        if reply_uuid:
            new_comment = self.create_comment_object(body=body, 
                                                 user_id=user_obj.id, 
                                                 uuid=str(uuid.uuid4()), 
                                                 creation_date=datetime.datetime.utcnow(),
                                                 reply_uuid=reply_uuid)

        else:
            new_comment = self.create_comment_object(body=body, 
                                                 user_id=user_obj.id, 
                                                 uuid=str(uuid.uuid4()), 
                                                 creation_date=datetime.datetime.utcnow())

        thread.comments.append(new_comment)

        if not transaction.commit():
            return [True, 'added']

        return [False, 'unable to add comment']


    # Returns [result, message]
    def add_thread(self, subvoat_name, title, body, user_obj):

        t_status, t_result = self.validate.thread(subvoat_name=subvoat_name,
                                                  title=title,
                                                  body=body)

        if not t_status:
            return [False, t_result]

        subvoat = self.get_subvoat(subvoat_name)

        if not subvoat:
            return [False, 'subvoat does not exist']

       
        now = datetime.datetime.utcnow()
        new_thread = self.create_thread_object(uuid=str(uuid.uuid4()),
                                               title=title,
                                               body=body,
                                               creator_id=user_obj.id,
                                               creation_date=now)


        # Append the thread to the subvoat
        subvoat.threads.append(new_thread)

        transaction.commit()

        # FIX: 
        #send_thread.delay()

        return [True, 'thread added']

        
    # Make one that orders by date, with a limit
    def get_threads(self, subvoat_name, start, end):
        # Find out how many pages there are, start with that page (descending) and limit by pages. 
        pages = end - start
        print(pages)
        
        if pages > self.config['max_threads_per_request']:
            return [False, 'too many pages, %s is the max' % (self.config['max_threads_per_request'])]

        #threads = self.session.query(Thread).order_by(Thread.id.desc()).filter(SubVoat.name == subvoat_name).limit(pages)

        # SORT BY LATEST
        #latest_thread = self.session.query(Thread).filter(SubVoat.name == subvoat_name).order_by(Thread.id.desc()).first()
        threads = self.session.query(Thread).filter(SubVoat.name == subvoat_name).filter(Thread.id.between(start, end)).order_by(Thread.id.desc())
       


        return [True, threads]


    def get_latest_thread_id(self, subvoat_name):

        latest_thread = self.session.query(Thread).filter(Subvoat.name == subvoat_name).order_by(Thread.id.desc()).first().id


    def get_thread_by_uuid(self, uuid):
        thread = self.session.query(Thread).filter(Thread.uuid == uuid).first()


        return thread

    def get_comment_by_uuid(self, uuid):
        comment = self.session.query(Comment).filter(Comment.uuid == uuid).first()

        return comment

    
    def vote_thread(self, thread_uuid, direction, user_id):

        v_status, v_result = self.validate.vote(direction)

        if not v_status:
            return [v_status, v_result]

        u_status, u_result = self.validate.uuid(thread_uuid)

        if not u_status:
            return [u_status, u_result]
        
        thread = self.get_thread_by_uuid(thread_uuid)

        if not thread:
            return [False, 'no such thread']

        # see if the user already voted, if so change the vote direction if its different 

        sq = self.session.query(Thread).filter(Thread.uuid == thread_uuid).subquery()
       
        q = self.session.query(ThreadVote, sq).filter(ThreadVote.user_id == user_id).first() 

    
        # if the vote doesn't exist, create it and commit it
        if not q:
            new_vote = ThreadVote(user_id=user_id, direction=direction)

            thread.votes.append(new_vote)

            self.session.add(thread)

            if not transaction.commit():
                return [True, 'vote added']

            return [False, 'unable to commit vote']


        # If the vote is the same
        if q.ThreadVote.direction == int(direction):
            return [True, 'vote unchanged']

        # Otherwise update the vote direction 
        else:
            q.ThreadVote.direction = int(direction)
            self.session.add(q.vote)

            if not transaction.commit():
                return [True, 'vote changed']
       
            return [False, 'unable to commit vote change'] 


    def vote_comment(self, comment_uuid, direction, user_id):
        
        
        v_status, v_result = self.validate.vote(direction)

        if not v_status:
            return [v_status, v_result]

        u_status, u_result = self.validate.uuid(comment_uuid)

        if not u_status:
            return [u_status, u_result]
        
    
        # FIX: calling comment 2x (sq = )
        comment = self.get_comment_by_uuid(comment_uuid)

        if not comment:
            return [False, 'no such comment']


        # get the comments
        
        sq = self.session.query(Comment).filter(Comment.uuid == comment_uuid).subquery()

        q = self.session.query(CommentVote, sq).filter(CommentVote.user_id == user_id).first()

        if not q:
            new_vote = CommentVote(user_id=user_id, direction=direction)

            comment.votes.append(new_vote)

            self.db.session.add(comment)

            if not transaction.commit():
                return [True, 'vote added']

            return [False, 'unable to commit vote']

        if q.CommentVote.direction == int(direction):
            return [True, 'vote unchanged']

        else:
            q.CommentVote.direction = int(direction)
            self.db.session.add(q.vote)

            if not transaction.commit():
                return [True, 'vote changed']

            return [False, 'unable to commit vote change']
            

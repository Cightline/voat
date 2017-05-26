
# These classes mainly deal with database interaction

import datetime
import json

from voluptuous import Schema, Required, All, Length, MultipleInvalid

import pika

from voat_sql.utils      import db
from voat_utils.config   import get_config
from voat_sql.utils.user import UserUtils



class SubvoatUtils():
    def __init__(self):
        self.db         = db.get_db()
        self.classes    = self.db.base.classes
        self.config     = get_config()
        self.user_utils = UserUtils()
   

    # Returns a user object (see the schemas)
    def create_subvoat_object(self, **kwargs):
        return self.classes.subvoat(**kwargs)

    def create_post_object(self, **kwargs):
        return self.classes.posts(**kwargs)
   
    # Returns a user object 
    def get_subvoat(self, subvoat_name):
        return self.db.session.query(self.classes.subvoat).filter(self.classes.subvoat.name == subvoat_name).first()
   

    def get_all_subvoats(self):
        return self.db.session.query(self.classes.subvoat).all()

    
    def add_subvoat(self, new_subvoat):
        self.db.session.add(new_subvoat)
        
        result = self.db.session.commit()

        return result


    # Returns [result, message]
    def add_post(self, subvoat_name, title, body, username):

        schema = Schema({ 
            Required('subvoat_name'): All(str, Length(min=self.config['min_length_subvoat_name'])),
            Required('title'):        All(str, Length(min=self.config['min_length_post_title'])),
            Required('body'):         All(str, Length(min=self.config['min_length_post_body'])),
            })


        try:
            schema({'subvoat_name':subvoat_name,
                    'title':title,
                    'body':body})

        except MultipleInvalid as e:
            return [False, '%s %s' % (e.msg, e.path)]

    

        subvoat = self.get_subvoat(subvoat_name)

        if not subvoat:
            return [False, 'subvoat does not exist']

        # We need to use the user.id  
    
        status, result = self.user_utils.get_user(username)

        if not status:
            return [False, result]

       
        # Should this even be here?
        elif not result:
            return [False, 'user does not exist']

        now = datetime.datetime.utcnow()
        new_post = self.create_post_object(title=title,
                                           body=body,
                                           user_id=result.id,
                                           creation_date=now)

        subvoat.posts_collection.append(new_post)

        self.db.session.commit()


        # JUST TESTING, FIX THIS
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        channel = connection.channel()

        channel.queue_declare(queue='post')
        channel.basic_publish(exchange='', routing_key='post', body=json.dumps({'title':title, 'body':body, 'user_id':result.id}))

        connection.close()

        return [True, 'post added']

        
    # Make one that orders by date, with a limit
    def get_posts(self, subvoat_name):
        posts = []
        subvoat =  self.db.session.query(self.classes.subvoat).filter(self.classes.subvoat.name == subvoat_name).first()

        #print(dir(subvoat.posts_collection))

        # probably want to limit this
        if subvoat:
            for post in subvoat.posts_collection:
                # Need to convert the user_id to username
                u_result, u_obj = self.user_utils.get_user_by_id(post.user_id)

                if u_result == False:
                    # LOG ERROR HERE
                    # error message should be in u_obj
                    continue 

                posts.append({'title':post.title,
                              'body':post.body,
                              # FIX THIS
                              'username':u_obj.username,
                              'creation_date':post.creation_date.isoformat()})

        return posts

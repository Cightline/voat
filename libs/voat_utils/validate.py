
from voluptuous import Schema, Required, All, Length, Range, MultipleInvalid

# If you want to add something here, just look at "validate_subvoat_name" and work off of that. 

class Valid():
    def __init__(self, config):
        self.config = config

    
    def try_schema(self, key, value, schema_obj):
        try:
            schema_obj({key:value})

        except MultipleInvalid as e:
            return [False, '%s %s' % (e.msg, e.path)]

        return [True, None]

    
    def subvoat_name(self, subvoat_name):
        schema = Schema({ Required('subvoat_name'): All(str, Length(min=self.config['min_length_subvoat_name']))})

        return self.try_schema('subvoat_name', subvoat_name, schema)

  
    def uuid(self, uuid):
        schema = Schema({ Required('uuid'): All(str, Length(min=36, max=36))})

        return self.try_schema('uuid', uuid, schema)


    def comment_body(self, comment_body):
        schema = Schema({ Required('comment_body'): All(str, Length(min=self.config['min_length_comment_body'], 
                                                                    max=self.config['max_length_comment_body']))})

        return self.try_schema('comment_body', comment_body, schema)


    def thread(self, subvoat_name, title, body):
        title_schema = Schema({ Required('title'): All(str, Length(min=self.config['min_length_thread_title'],
                                                             max=self.config['max_length_thread_title']))})

        body_schema = Schema({  Required('body'):  All(str, Length(min=self.config['min_length_thread_body'],
                                                             max=self.config['max_length_thread_body']))})



    
        # validate the subvoat_name first
        sn_status, sn_result = self.subvoat_name(subvoat_name)

        if not sn_status:
            return [sn_status, sn_result]

        # Then validate the thread title
        t_status, t_result = self.try_schema('title', title, title_schema)

        if not t_status:
            return [t_status, t_result]
    
        # and thread body
        b_status, b_result = self.try_schema('body', body, body_schema)

        if not b_status:
            return [b_status, b_result]

        # return True if everything is ok
        return [True, None]



    def vote(self, direction):
        schema = Schema({ Required('vote'): All(int, Range(min=-1, max=1))})

        return self.try_schema('vote', direction, schema)

    def username(self, username):
        schema = Schema({ Required('username'): All(str, Length(min=self.config['min_length_username'], max=self.config['max_length_username']))})

        return self.try_schema('username', username, schema)


    def password(self, password):
        schema = Schema({ Required('password'): All(str, Length(min=self.config['min_length_password'], max=self.config['max_length_password']))})

        return self.try_schema('password', password, schema)


    def user(self, username, password):


        u_status, u_result = self.username(username)

        if not u_status:
            return [u_status, u_result]

        
        p_status, p_result = self.password(password)

        if not p_status:
            return [p_status, p_result]

        return [True, None]
        

    def page(self, start, end):
        s_schema = Schema({ Required('start'): All(int, Range(min=0))})
        e_schema = Schema({ Required('end'):   All(int, Range(min=0))})

        s_status, s_result = self.try_schema('start', start, s_schema)

        if not s_status:
            return [s_status, s_result]

       
        e_status, e_result = self.try_schema('end', end, e_schema)

        if not e_status:
            return [e_status, e_result]

        if end < start:
            return [False, 'ending page cannot be lower than starting page']

    
        total_pages = end - start

        if total_pages > 50:
            return [False, 'you cannot request more than 50 pages']

        return [True, None]
        
    

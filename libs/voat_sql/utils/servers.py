
# THIS SHOULD BE MOVED 

# WE SHOULD ALSO MAKE A SEPERATE KEY MODULE

import requests

from voat_sql.utils.db import get_db
from voat_utils.config import get_config

class ServerUtils():
    def __init__(self):
        self.db      = get_db()
        self.config  = get_config()
        self.classes = self.db.base.classes




    def create_server_object(self, **kwargs):
        return self.classes.server(**kwargs)


    def is_whitelisted(self, address):

        if address in config['whitelisted_servers']:
            return True

        return False
            

    def get_public_key(self, address):
    
        public_key = self.db.session.query(self.classes.servers).filter(self.classes.servers.address == address).first().public_key

        return public_key


    def get_server(self, address):
        return self.db.session.query(self.classes.servers).filter(self.classes.servers.address == address).first()


    def update_server(self, address):
        # MORE ERROR CHECKING NEEDED

        try:
            r = requests.get('%s/get_public_key' % (address))

        except requests.exceptions.ConnectionError as e:
            return [False, 'unable to establish a connection to %s' % (address)]
      
        
        if 'result' not in r.json():
            return [False, 'server responded with no result']

        # IS THIS SAFE?
        elif 'error' in r.json():
            return [False, 'server responded with an error %s' % (r.json()['error'])]


        # See if it already exists
        q = self.get_server(address)

        if not q:
             
            new_server = self.classes.servers(address=address,
                                             public_key=r.json()['result'])
                                             
         

            self.db.session.add(new_server)
            self.db.session.commit()
      
            return [True, 'added']

           
        if q:
            if q.public_key == r.json()['result']:
                return [True, 'no change']

            
            q.public_key = r.json()['result']

            self.db.session.commit()

            return [True, 'updated']


        return [False, None]

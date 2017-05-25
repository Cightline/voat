
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
            

    def get_server(self, address):
        # FIX THIS UP (validation)

        return [True, self.db.session.query(self.classes.servers).filter(self.classes.servers.address == address).first()]


    def update_server(self, address):
        
        d = requests.get('%s/get_public_key' % (address))

        print(d)



        

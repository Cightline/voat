# When executed, this should check all the servers against the whitelist. It should add or remove depending on the whitelist. 

import requests

from voat_sql.utils.servers import ServerUtils
from voat_sql.utils.db      import get_db
from voat_utils.config      import get_config


s       = ServerUtils()
config  = get_config()
db      = get_db()
classes = db.base.classes

def update_public_key(address):

    # see if it already exists
    
    print(s.get_server(address))


def update():
    for server in config['whitelisted_servers']:
        result, message = s.update_server(server)

        if not result:
            print('Error: %s' % (message))

        else:
            print('[%s] %s' % (server, message))
        

if __name__ == '__main__':
    update()

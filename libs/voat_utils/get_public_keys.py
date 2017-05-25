
from voat_utils.config import get_config

config = get_config()

def update():

    for server in config['whitelisted_servers']:
        print(server)


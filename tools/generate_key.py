import os
#from voat_sql.utils.db  import get_db
from voat_utils.config  import get_config
from voat_utils.config  import write_value
from voat_utils.keys    import generate_key


#db = get_db()
#classes = db.base.classes

config = get_config()

def update_server_key():
    key = generate_key(config['server_key_bits'])

    if os.path.exists('/etc/voat/config/public_key') or os.path.exists('/etc/voat/config/private_key'):
        confirm = input('Keys are already in /etc/voat/config/ , generate new ones anyway? [y/n]: ').lower().strip()

        if confirm != 'y' and confirm != 'yes':
            exit()


    with open('/etc/voat/config/public_key', 'wb') as public_key:
        public_key.write(key.publickey().exportKey())


    with open('/etc/voat/config/private_key', 'wb') as private_key:
        private_key.write(key.exportKey())


    print('New (%s) bit keys generated' % (config['server_key_bits']))


if __name__ == '__main__':
    update_server_key()

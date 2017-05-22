


# DEPENDENCIES:

You can install these with pip (python-pip on Arch Linux)

* flask-restful
* flask
* sqlalchemy
* passlib



# RUNNING:
on the first run only
`mkdir /etc/voat`

`mkdir /etc/voat/db`

`mkdir /etc/voat/config`

`useradd voat`

`chown -R voat:voat /etc/voat`

`chmod -R 775 /etc/voat`

link the config to `/etc/voat/config/config.json`

`ln -s [config_path] /etc/voat/config/config.json`


on the first run (or after changes)  

`cd /where/ever/voat/libs`

`sudo python setup.py install`

`sudo su voat -c "python tools/create_db.py"`

to start the server

`sudo su voat -c "python rest_server.py"`


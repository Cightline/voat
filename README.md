


# DEPENDENCIES:

You can install these with pip (python-pip on Arch Linux)

* flask-restful
* flask
* sqlalchemy
* passlib



# RUNNING:
on the first run (or after changes)  

`cd /where/ever/voat/libs`

`sudo python setup.py install`

`sudo su voat -c "python tools/create_db.py"`

to start the server

`sudo su voat -c "python rest_server.py"`


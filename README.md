


# DEPENDENCIES:
    - flask-restful
    - flask
    - sqlalchemy



# RUNNING:
on the first run (or after changes) cd to voat/libs and run

`sudo python setup.py install`


on the first run (or after changes) run

`sudo su voat -c "python tools/create_db.py"`



to start the server

`sudo su voat -c "python rest_server.py"`


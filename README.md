


# DEPENDENCIES:

You can install these with pip (python-pip on Arch Linux)

* flask-restful
* flask
* sqlalchemy
* passlib
* voluptuous
* pycrypto



# RUNNING:
on the first run only

```
mkdir /etc/voat
mkdir /etc/voat/db
mkdir /etc/voat/config
useradd voat
chown -R voat:voat /etc/voat
chmod -R 775 /etc/voat
```

link the config

```sudo su voat -c "ln -s [absolute_config_path] /etc/voat/config/config.json"```


on the first run (or after changes to voat/libs )  

```cd /where/ever/voat/libs
sudo python setup.py install

```

if you make changes to the database schemas, run this to recreate it. 
```
sudo su voat -c "python tools/create_db.py"
```


to start the server

```sudo su voat -c "python rest_server.py"```

if you would like to run 2 instances on the same machine

``` 
sudo su voat -c "export FLASK_APP=/path/to/voat/rest_server.py; flask run --host 0.0.0.0 --port [whatever_port]"
```


# TODO:

- [ ] authentication


# NOTES:

This will probably use PyPy or uWSGI. (https://pypy.org/) (https://uwsgi-docs.readthedocs.io/en/latest/)

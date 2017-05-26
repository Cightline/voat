


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

## link the config

```sudo su voat -c "ln -s [absolute_config_path] /etc/voat/config/config.json"```


## on the first run (or after changes to voat/libs )  

```cd /where/ever/voat/libs
sudo python setup.py install

```

## if you make changes to the database schemas, run this to recreate it. 
```
sudo su voat -c "python tools/create_db.py"
```


## to start the server

```sudo su voat -c "python rest_server.py"```

## if you would like to run 2 instances on the same machine

``` 
sudo su voat -c "export FLASK_APP=/path/to/voat/rest_server.py; flask run --host 0.0.0.0 --port [whatever_port]"
```


# TODO:

- [ ] authentication


# NOTES:

Users will have a "home" server or "primary provider". This server can be run locally, or by someone else. It's just the server that the user registered to. Users can register the same name on different providers, however the public keys will be different. The "primary provider" will whitelist servers it wants to communicate with. Each server will have a public/private keypair. The primary provider will listen for posts coming from other servers. It will display these messages to the user. If the user needs to search something, the primary provider can look locally or from other servers. All messages are signed by the user (automaticlally by the primary provider). Users will have to midly trust the primary provider, or host their own instance. 

This will probably use PyPy or uWSGI. (https://pypy.org/) (https://uwsgi-docs.readthedocs.io/en/latest/)


# DEVELOPER INFO

As of now, Voat runs from whatever directory you cloned it to. Eventually it will be moved to the proper directory. The config and database are stored (the config.json is technically symlinked) in `/etc/voat`.


main functions (main logic really)

```voat/libs/voat_rest``` 

schemas and database utilities (basically lower level stuff for the main functions) (I may reorganize this)

```voat/libs/voat_sql``` 

utilities that aren't run from the main functions (I may reorganize this)

```voat/libs/voat_utils```





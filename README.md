


# DEPENDENCIES:

You can install these with pip (python-pip on Arch Linux)

* flask-restful
* flask
* sqlalchemy
* sqlalchemy_utils
* passlib
* voluptuous
* pycrypto
* requests
* celery[redis]

The following need to be installed
* redis (pacman -S redis)



# RUNNING:
on the first run only (or after a `git pull`)

```
sudo bash install.sh
```


## to start the server

As of now you have to run the following:

```
# ensure redis is running (systemctl start redis)
bash start_rest_server
bash start_celery_workers
bash start_listener 
```



# TODO:

- [ ] logging
- [ ] admin stuff
- [x] authentication
- [x] registration 
- [x] posting 
- [x] creating subvoats 
- [x] private/public key generation for server
- [x] private/public key generation for user
- [x] serving public key
- [x] simple tool to update whitelisted servers 
- [ ] verification of whitelisted server 
- [ ] sharing posts/comments 
- [ ] searching posts/comments locally
- [ ] searching posts/comments remotely

I need people to go through and check/reorganize things. 



# NOTES:

Users will have a "home" server or "primary provider". This server can be run locally, or by someone else. It's just the server that the user registered to. Users can register the same name on different providers, however the public keys will be different. The "primary provider" will whitelist servers it wants to communicate with. Each server will have a public/private keypair. The primary provider will listen for posts coming from other servers. It will display these messages to the user. If the user needs to search something, the primary provider can look locally or from other servers. All messages are signed by the user (automaticlally by the primary provider). Users will have to midly trust the primary provider, or host their own instance. 

This will probably use PyPy or uWSGI. (https://pypy.org/) (https://uwsgi-docs.readthedocs.io/en/latest/)


# DEVELOPER INFO:

READ THROUGH THIS: https://guides.github.com/introduction/flow/

As of now, Voat runs from whatever directory you cloned it to. Eventually it will be moved to the proper directory. The config and database are stored in `/etc/voat`. For the moment I'm using Sqlite, and the config should be symlinked. 


main functions (main logic really)

```voat/libs/voat_rest``` 


schemas and database utilities (basically lower level stuff for the main functions) (I may reorganize this)

```voat/libs/voat_sql``` 


utilities that aren't run from the main functions (I may reorganize this)

```voat/libs/voat_utils```





The listener listens for new incoming posts and stores them in the database (not complete).

The celery workers make certain functions asynchronous



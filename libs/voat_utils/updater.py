
import requests

from celery import Celery

from flask import current_app

from voat_utils.config import get_config

app    = Celery('send', broker=get_config()['broker'])


@app.task
def send_thread():
    # yep, getting the config 2x. Otherwise it wont update the whitelist when a new task is started
    # FIX CONFIG?
    config = get_config()
    for address in config['whitelisted_servers']:
        print(address)
        requests.post('%s/update_data' % (address), {'test':'test'})

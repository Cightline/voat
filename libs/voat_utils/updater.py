
import requests

from celery import Celery

from flask import current_app

from voat_utils.config import get_config

app    = Celery('send', broker='redis://localhost:6379')
config = get_config()


@app.task
def send_post():
    for address in config['whitelisted_servers']:
        print(address)
        requests.post('%s/update_data' % (address), {'test':'test'})

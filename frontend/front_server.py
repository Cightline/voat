
from flask import Flask, render_template, request
import requests


app = Flask(__name__)

api_url = 'http://localhost:5000'

def get_threads(url, subvoat_name, thread_start, thread_end):
    page = requests.get('%s/get_threads/%s' % (url, subvoat_name), {'thread_start':thread_start, 'thread_end':thread_end})

    threads = page.json()

    return threads 

def get_latest_thread(url, subvoat_name):

    page = requests.get('%s/latest_thread/%s' % (url, subvoat_name))

    latest_thread = page.json()

    return latest_thread

def api_login(username, password):
    page = requests.post('%s/authenticate' % (api_url), {'username':username, 'password':password})

    return page.json()

def api_register(username, password):
    page = requests.post('%s/register' % (api_url), {'username':username, 'password':password})

    return page.json()


def show_error(msg):
    return render_template('error.html', msg=msg)


@app.route('/')
def index():
    page = 1

    if request.args.get('page'):
        try:
            page = int(request.args.get('page')) 
        except: 
            return show_error('invalid page')

   
    # basically this converts the page to thread counts 
    thread_end   = page * 25
    thread_start = thread_end - 25

    # make sure users can't add special characters to thread/subvoat names (security)
    # threads = get_threads(api_url, 'default')
    threads = get_threads(api_url, 'test_exists', thread_start, thread_end)

    if 'error' in threads:
        return show_error(threads['error'])

    elif 'result' in threads:
        return render_template('index.html', threads=threads['result'], next_page=page + 1)


    return show_error('no data returned from API')

@app.route('/login', methods=['POST'])
def login():


    username = request.args.get('username')
    password = request.args.get('password')

    status = api_login(username, password)

    if 'error' in status:
        return show_error(status['error'])

    elif 'result' in status:

        if 'api_token' in status['result']:
            session['logged_in'] = True
            session['username']  = username
            session['api_token'] = status['result']['api_token']


    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():

    username = request.args.get('username')
    password = request.args.get('password')

    status = api_register(username, password)

    if 'error' in status:
        return show_error(status['error'])

    elif 'result' in status:

        if 'api_token' in status['result']:
            session['logged_in'] = True
            session['username']  = username
            session['api_token'] = status['result']['api_token']


    return render_template('index.html')

@app.route('/status')
def status():
    return render_template('status.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

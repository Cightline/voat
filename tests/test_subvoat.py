import requests
import random
import string

# this shit is half-assed

base_address = 'http://localhost:5000'

def get_api_token():
    result = requests.post('%s/authenticate' % (base_address), {'username':'test_username', 'password':'test_password'}).json()['result']

    #rint(result)
    
    return result['api_token']

def test_registration():
    result = requests.post('%s/register' % (base_address), {'username':'test_username', 'password':'test_password'}).json()

    print(result)


# test subvoat creation
def test_new_subvoat_creation():
    api_token = get_api_token()

    
    result = requests.post('%s/create_subvoat' % (base_address), {'username':'test_username', 
                                                                  'api_token':api_token,
                                                                  'subvoat_name':'test_%s' % (''.join(random.choices(string.ascii_letters, k=10)))})

    print(result.json())


# Try to create the same subvoat that already exists
def test_same_subvoat_creation():

    api_token = get_api_token()

    requests.post('%s/create_subvoat' % (base_address), {'username':'test_username', 'api_token':api_token, 'subvoat_name':'test_exists'})

    result = requests.post('%s/create_subvoat' % (base_address), {'username':'test_username', 'api_token':api_token, 'subvoat_name':'test_exists'})

    print(result.json())


def test_listing_subvoats():
    print(requests.get('%s/list_subvoats' % (base_address)).json())


def test_posting():
    api_token = get_api_token()

    body  = ''.join(random.choices(string.ascii_letters, k=100))
    title = ''.join(random.choices(string.ascii_letters, k=10))

    print(requests.post('%s/submit_thread' % (base_address), {'username':'test_username', 
                                                            'api_token':api_token, 
                                                            'subvoat_name':'test_exists',
                                                            'title':title,
                                                            'body':body}).json())

def test_listing_threads():

    data = requests.post('%s/get_threads' % (base_address), {'subvoat_name':'test_exists'}).json()

    print(data)

    thread_uuid = data['result'][0]['uuid']
   
    print(requests.post('%s/get_comments' % (base_address), {'thread_uuid':thread_uuid}).json())


def test_posting_comment():
    api_token = get_api_token()
    body  = ''.join(random.choices(string.ascii_letters, k=100))

    data = requests.post('%s/get_threads' % (base_address), {'subvoat_name':'test_exists'}).json()

    thread_uuid = data['result'][0]['uuid']

    print(requests.post('%s/submit_comment' % (base_address), {'thread_uuid':thread_uuid, 
                                                              'username':'test_username', 
                                                              'api_token':api_token,
                                                              'body':body}).text)
    
def test_vote_thread():
    # this needs to try directions that exceed -1 or 1 (ie 5 or something)
    # this should also test incorrect API tokens
    # and it should test incorrect thread uuids (88322c7f-929e-43b0-844b-13b9b309f253)
    api_token = get_api_token()

    thread_data = requests.post('%s/get_threads' % (base_address), {'subvoat_name':'test_exists'}).json()

    thread_uuid = thread_data['result'][0]['uuid']

    data = requests.post('%s/vote_thread' % (base_address), {'thread_uuid':thread_uuid,
                                                             'username':'test_username',
                                                             'api_token':api_token,
                                                             'direction':-1})


    print(data.json())

def test_vote_comment():
    api_token = get_api_token()

    thread_data = requests.post('%s/get_threads' % (base_address), {'subvoat_name':'test_exists'}).json()

    thread_uuid = thread_data['result'][0]['uuid']

    comments = requests.post('%s/get_comments' % (base_address), {'thread_uuid':thread_uuid}).json()

    comment_uuid = comments['result'][0]['uuid']

    print('COMMENT UUID: %s' % (comment_uuid))


    data = requests.post('%s/vote_comment' % (base_address), {'comment_uuid':comment_uuid,
                                                              'username':'test_username',
                                                              'api_token':api_token,
                                                              'direction':-1})


    print(data.json())



if __name__ == '__main__':
    print('TESTING REGISTRATION')
    test_registration()
    print('\n')

    print('TESTING NEW SUBVOAT CREATION')
    test_new_subvoat_creation()
    print('\n')

    print('TESTING SAME SUBVOAT CREATION')
    test_same_subvoat_creation()
    print('\n')

    print('LISTING SUBVOATS')
    test_listing_subvoats()
    print('\n')


    print('POSTING TO SUBVOAT')
    test_posting()
    print('\n')

    print('LISTING THREADS AND COMMENTS')
    test_listing_threads()
    print('\n')

    print('POSTING COMMENT')
    test_posting_comment()
    print('\n')

    print('TEST VOTE THREAD')
    test_vote_thread()
    print('\n')

    print('TEST VOTE COMMENT')
    test_vote_comment()
    print('\n')

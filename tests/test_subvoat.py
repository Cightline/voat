import requests
import random
import string

base_address = 'http://localhost:5000'


def get_api_token():
    result = requests.post('%s/authenticate' % (base_address), {'username':'test_username', 'password':'test_password'}).json()['result']
    
    return result['api_token']

def test_registration():
    result = requests.post('%s/register' % (base_address), {'username':'test_username', 'password':'test_password'})


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

    print(requests.post('%s/get_threads' % (base_address), {'subvoat_name':'test_exists'}).json())
   

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

    print('LISTING THREADS')
    test_listing_threads()
    print('\n')

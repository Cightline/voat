import argparse
import requests
import random
import string

import datetime

# make sure you dont run data.json(), we just want the return time, not how long it takes python 
# to transform it into JSON

class Performance():
    def __init__(self):
        self.base_address = 'http://localhost:5000'

    def get_now(self):
        return datetime.datetime.now()

    def check(self, result):
        if result.status_code != 200:
            print('Something happened')
            print(result.text)
            exit()

        try:
            j_result = result.json()

        except Exception as e:
            print('Exception caught: %s' % (e))
            exit()

        if 'result' not in result.json():
            print('Error returned')
            print(j_result)
            print(result.url)
            exit()


    def create_test_user(self):
        result = requests.post('%s/register' % (self.base_address), {'username':'test_username', 'password':'test_password'})

        self.check(result)

        return result.json()['result']

    
    def create_test_subvoat(self, count=0):
        api_token = self.get_api_token()

        for x in range(count):

            body  = ''.join(random.choices(string.ascii_letters, k=100))
            title = ''.join(random.choices(string.ascii_letters, k=10))

            result = requests.post('%s/create_subvoat' % (self.base_address), {'subvoat_name':'test_%s' % (title[0:5]),
                                                                              'username':'test_username', 
                                                                              'api_token':api_token,
                                                                              'body':body,
                                                                              'title':title})

            self.check(result)

        #return result.json()['result']


    # test subvoat. 
    # try to create thread without subvoat. 
    # try to create subvoat that already exists
    # try to create subvoat with name length out of parameters (see config.json)
    # try to create subvoat with incorrect api_token
    # try to create subvoat with fake user


    def get_api_token(self):
        
        result = requests.post('%s/authenticate' % (self.base_address), {'username':'test_username', 'password':'test_password'})

        self.check(result)

        return result.json()['result']['api_token']

        

    def list_subvoats(self):
        start_time = self.get_now()

        result  = requests.get('%s/list_subvoats' % (self.base_address))
   
        result_time = self.get_now() - start_time
    
        self.check(result)

        print(result.json())
        print('%s subvoats, execution time: %s' % (len(result.json()['result']), result_time))
    

    def list_comments(self):
        threads     = requests.post('%s/get_threads' % (self.base_address), {'subvoat_name':'test_exists'}).json()
        thread_uuid = threads['result'][0]['uuid']

        start_time = self.get_now()
        result = requests.post('%s/get_comments' % (self.base_address), {'thread_uuid':thread_uuid})

        result_time = self.get_now() - start_time

        self.check(result)

        print('%s comments, execution time: %s' % (len(result.json()['result']), result_time))
   

    def list_threads(self):
        start_time = self.get_now()
        
        result = requests.post('%s/get_threads' % (self.base_address), {'subvoat_name':'test_exists'})

        result_time = self.get_now() - start_time

        self.check(result)

        #print(result.json()['result'][0])

        print('%s threads, execution time: %s' % (len(result.json()['result']), result_time))

    
    def generate_threads(self):
        api_token = self.get_api_token()

        for x in range(100):
           
            title = ''.join(random.choices(string.ascii_letters, k=10))
            body  = ''.join(random.choices(string.ascii_letters, k=100))
        
            
            result = requests.post('%s/submit_thread' % (self.base_address), {'username':'test_username',
                                                                              'api_token':api_token,
                                                                              'subvoat_name':'test_exists',
                                                                              'title':title,
                                                                              'body':body}).json()



if __name__ == '__main__':

    p = Performance()

    parser = argparse.ArgumentParser(description='Performance testing tool')

    parser.add_argument('--list-subvoats',       dest='list_subvoats',       action='store_true')
    parser.add_argument('--list-comments',       dest='list_comments',       action='store_true')
    parser.add_argument('--list-threads',        dest='list_threads',        action='store_true')
    parser.add_argument('--gen-threads',         dest='gen_threads',         action='store_true')
    parser.add_argument('--test-create-user',    dest='test_create_user',    action='store_true')
    parser.add_argument('--test-create-subvoat', dest='test_create_subvoat', action='store', type=int, default=0)

    args = parser.parse_args()
    
    
    if args.list_subvoats:
        p.list_subvoats()

    elif args.list_comments:
        p.list_comments()

    elif args.list_threads:
        p.list_threads()

    elif args.gen_threads:
        p.generate_threads()

    elif args.test_create_user:
        p.create_test_user()

    elif args.test_create_subvoat:
        p.create_test_subvoat(args.test_create_subvoat)

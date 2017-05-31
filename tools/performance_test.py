import argparse
import requests

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

    def list_subvoats(self):
        start_time = self.get_now()

        result  = requests.get('%s/list_subvoats' % (self.base_address))
   
        result_time = self.get_now() - start_time
    
        self.check(result)

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


if __name__ == '__main__':

    p = Performance()

    parser = argparse.ArgumentParser(description='Performance testing tool')

    parser.add_argument('--list-subvoats', dest='list_subvoats', action='store_true')
    parser.add_argument('--list-comments', dest='list_comments', action='store_true')
    parser.add_argument('--list-threads',  dest='list_threads',  action='store_true')

    args = parser.parse_args()

    if args.list_subvoats:
        p.list_subvoats()

    elif args.list_comments:
        p.list_comments()

    elif args.list_threads:
        p.list_threads()


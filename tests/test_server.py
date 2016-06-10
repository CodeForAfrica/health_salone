"""
health_salone/src/core.py tests
"""
import random
import unittest
import requests
from health_salone.src.core import CITIES

class ServerTestCase(unittest.TestCase):
    
    def setUp(self,):
        self.url = "http://localhost:9099/sms/incoming"

    def test_endpoint(self,):
        '''
        '''
        random_city = CITIES[random.randint(0, len(CITIES)-1)]
        args = dict(phone_number='', Body=random_city)
        resp = requests.post(self.url, params=args)
        print "%s: %s - %s" % (random_city, resp.status_code, resp.text)
        self.assertTrue(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()

"""
health_salone/src/core.py tests
"""
import random
import unittest
import requests
from health_salone.src.core import CITIES, Database, construct_message, MESSAGES
from health_salone.src import config

class ServerTestCase(unittest.TestCase):
    
    def setUp(self,):
        self.url = "http://localhost:9099/sms/incoming"
        self.db = Database()

    def xtest_endpoint(self,):
        '''
        '''
        random_city = CITIES[random.randint(0, len(CITIES)-1)]
        args = dict(phone_number='', Body=random_city)
        resp = requests.post(self.url, params=args)
        print "%s: %s - %s" % (random_city, resp.status_code, resp.text)
        self.assertTrue(resp.status_code, 200)

    def test_get_by_city(self,):
        random_city = CITIES[random.randint(0, len(CITIES)-1)]
        sample_data = self.db.get_by_city(random_city)
        self.assertIsInstance(sample_data, list)

    def test_construct_message(self,):
        random_city = CITIES[random.randint(0, len(CITIES)-1)]
        sample_data_true = self.db.get_by_city(random_city)
        sample_data_false = []
        msg_true = construct_message(sample_data_true)
        msg_false = construct_message(sample_data_false)

        self.assertEqual(msg_false, MESSAGES['miss'])

        



    def test_env_variables(self,):
        pass



if __name__ == '__main__':
    unittest.main()

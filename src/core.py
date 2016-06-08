import dataset
from celery import Celery
from health_salone.src import config

app = Celery('sms-listener', broker=config.MESSAGE_BROKER)

@app.task(name='health_salone.src.core.process_request')
def process_request(params):
    '''
    {'Body': 'Great',
    'MessageSid': 'SM2d806f6da54385bb5ec435aad6c7589e',
    'FromZip': '',
    'From': '+',
    'SmsMessageSid': 'SM2d806f6daad6c7589e',
    'SmsStatus': 'received',
    'MessagingServiceSid': 'MG0999f2e7f79860b59',
    'FromCity': '',
    'ApiVersion': '2010-04-01',
    'To': '+13234194762',
    'NumMedia': '0',
    'ToZip': '91337',
    'ToCountry': 'US',
    'AccountSid': 'ACfd313e36f5b20f',
    'NumSegments': '1',
    'ToState': 'CA',
    'SmsSid': 'SM2d80c435aad6c758',
    'ToCity': 'LOS ANGELES', 'FromState': '', 'FromCountry': 'KE'}
    '''
    try:
        print params
        message_body = params['Body']

        # assume message body == city
        db = Database()
        city_list = db.get_by_city(message_body)
        print "Result: %s" % city_list

    except Exception, err:
        print "ERROR: %s -- %s" % (err, params)
        raise err

class Database():

    def __init__(self):
        self.db = dataset.connect(config.DATABASE)
        self.table = self.db['healthdata']

    def get_by_city(self, city):
        # REMOVE THIS !!!!
        return self.db.query(
                """select description, hours from healthdata where "City"='{}' """.format(city)
                )

import dataset
import requests
from celery import Celery
from health_salone.src import config
#from twilio.rest import TwilioRestClient

app = Celery('sms-listener', broker=config.MESSAGE_BROKER)

RESULT_COUNT = 3
CITIES = ['Western Area Rural', 'Bombali', 'Southern Province',
          'Western Area Urban', 'Bo', 'Tonkolili', 'Kenema', 'Kono',
          'Kambia', 'Freetown']

MESSAGES = dict(
        hit='',
        miss="""Sorry, we were unable to find facilities that match your query.
        Please try again with your city from this list: %s""" % CITIES
        )


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
        message_body = params['Body'].strip()
        if message_body.capitalize() not in CITIES:
            message = "Please try again with one of the cities below:\n%s" % CITIES
            send_message(message, params['From'])
            return

        # assume message body == city
        db = Database()
        city_list = db.get_by_city(message_body.capitalize())
        message = construct_message(city_list)
        print "====  %s =====" % message
        return send_message(message, params['From'])

    except Exception, err:
        print "ERROR: %s -- %s" % (err, params)
        raise err


def construct_message(facility_list):
    '''
    returns a message to be sent to the user
    '''
    if not facility_list:
        return MESSAGES['miss']
    else:
        count = 0
        message = ""
        for facility in facility_list:
            count += 1
            message += "%s) %s/n" % (count, facility)
            if count >= RESULT_COUNT:
                break
        return message


def send_message(message, phone_number):
    '''
    sends SMS
    '''
    try:
        # some validations
        if not phone_number.startswith('+'):
            phone_number = '+%s' % str(phone_number)
        if len(message) > config.MAX_MESSAGE_LENGTH:
            message = message[:config.MAX_MESSAGE_LENGTH]

        sms_client = TwilioRestClient(config.TWILIO['SID'], config.TWILIO['TOKEN'])
        sent = sms_client.messages.create(to=phone_number, from_=config.TWILIO['SENDER'], body=message)
        print "msg - %s - %s - %s" % (phone_number, sent.status, sent.body)

    except Exception, err:
        print "ERROR: send_message() fail:  %s -- %s" % (phone_number, str(err))
        sent = False

    finally:
        return dict(sent=sent,
                phone_number=phone_number)



class Database():

    def __init__(self):
        self.db = dataset.connect(config.DATABASE)
        self.table = self.db['healthdata']

    def get_by_city(self, city):
        resultset = self.table.find(City=city)
        result_list = []
        for result in resultset:
            result_list.append(result['description'])
        return result_list

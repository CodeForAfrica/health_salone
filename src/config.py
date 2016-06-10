import os
HOME = os.getenv('APPS_HOME')

WEB_PORT = 9099
WEB_THREADS = 20

LOGS = dict(
        WEB='twistd-web-service.log',
        CONSUMER='/logs/consumer.log',
        LOCATION='%s/health_salone/logs' % (HOME)
        )

MESSAGE_BROKER = os.getenv('SL_RABBITMQ_URL')
DATABASE = os.getenv('SL_DATABASE_URL')

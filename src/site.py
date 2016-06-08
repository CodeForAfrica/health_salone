#!/usr/bin/python2.7
from twisted.application import internet, service
from twisted.web import server, resource
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor

from health_salone.src.server import RequestFactory
from health_salone.src import config

ProfilerService = internet.TCPServer(config.WEB_PORT, RequestFactory())
ProfilerService.setName('sms-listener')
application = service.Application('sms-listener')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile(config.LOGS['WEB'], config.HOME)
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(config.WEB_THREADS)

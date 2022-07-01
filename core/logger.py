'''基于logging的日志器。'''
import os
import re
import sys

from loguru import logger


logpath = os.path.abspath('./logs')
if not os.path.exists(logpath):
    os.mkdir(logpath)

bot_name = re.split(r'[/\\]', sys.path[0])[-1].title()
basic_logger_format = "<cyan>[" + bot_name + "]</cyan><green>[{time:YYYY-MM-DD HH:mm:ss}]</green><blue>[{name}:{function}:{line}]</blue><level>[{level}]:{message}</level>"


class Logginglogger:
    def __init__(self):
        self.log = logger
        self.log.remove()
        self.log.add(sys.stderr, format=basic_logger_format, level="INFO", backtrace=False, diagnose=False)
        self.log.add(logpath + '/' + bot_name + "_{time:YYYY-MM-DD}.log", format=basic_logger_format, retention="10 days")
        self.info = self.log.info
        self.error = self.log.error
        self.debug = self.log.debug
        self.warn = self.log.warning
        self.exception = self.log.exception


Logger = Logginglogger()

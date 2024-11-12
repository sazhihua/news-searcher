import os
from os import path
import logging.config


# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

# create logger
def createLogger(loggerName):
    logging.config.fileConfig(os.path.abspath(os.path.dirname(__file__)) + r'\logging.conf')
    log = logging.getLogger(loggerName)
    return log

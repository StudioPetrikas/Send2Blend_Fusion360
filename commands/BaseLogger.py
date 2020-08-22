import os
import logging
from logging.handlers import RotatingFileHandler

# create format of the log message
logFormatter = logging.Formatter('%(levelname)-7s; %(funcName)-37s; %(lineno)3d; %(message)s')

# Get the path of the running script (api command)
appPath = os.path.dirname(os.path.abspath(__file__))

# add subdirectory "log" to the path
logPath = os.path.join(appPath, 'logs')

if not os.path.isdir(logPath):
    os.makedirs(logPath)

# create full logfilename
logFullPathName = os.path.join(logPath, 'Send2Blend.log')

# create log handler
logHandler = RotatingFileHandler(logFullPathName, mode='a', maxBytes=200000, backupCount=2, encoding=None, delay=0)
logHandler.setFormatter(logFormatter)
logHandler.setLevel(logging.DEBUG)

# create logger
logger = logging.getLogger('Send2Blend')
logger.setLevel(logging.DEBUG)

# add logger no logger is available
if not len(logger.handlers):
    logger.addHandler(logHandler)

logger.debug("Logging started")

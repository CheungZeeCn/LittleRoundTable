#!/usr/bin/env python
# -*- coding: utf-8 -*-  

"""
log module

Usage:
    import log
    import logging
    
    log.logInit('programName', logDir='./')

    two log file will generated:
    - logDir/programName.log: all log
    - logDir/programName.wf.log: log >= warning

    # DEBUG < INFO < WARNING < ERROR < CRITICAL    
    logging.debug('msg')
    logging.info('msg')
    logging.warning('msg')
    logging.error('msg')
    logging.critical('msg')

"""
import logging 
import logging.handlers
import sys
import os

LOG_BASE_DIR = os.path.join(os.getcwd(), 'logs')   # base dir of log

# we would like to init it at first.
def initLogBasicPath(thePath):
    global LOG_BASE_DIR
    LOG_BASE_DIR = thePath

def _logPathGen(progName):
    path = progName.replace('.', '/')
    path = os.path.join(LOG_BASE_DIR, path)
    return path

def _fileNameGen(progName, logDir, isErrorLog=False):
    "Generate filename from program name"
    logDir = logDir.rstrip('/')

    if isErrorLog:
        # warning, error, critical
        fileName = os.path.join(logDir, progName + ".wf.log")
    else:
        # all log
        fileName = os.path.join(logDir, progName + ".log")

    return fileName

def _logDirCheckAndCreate(dirPath):
    "check, and create dir if nonexist"
    retVal = 'OK'
    
    if not os.path.exists(dirPath):
        try:
            # create directory (recursively)
            os.makedirs(dirPath)
        except OSError:
            retVal = 'ERROR'
    return retVal

def getSubLogger(loggerName, logLevel=logging.DEBUG, logDir=None, formatStr=None, \
            when='D', backupCount=7, stdout=True):
    """
     logInit - initialize log module
    
     ARGs:
       loggerName    - name of the program, e.g., 'gtc.bfe_reader'
                     log file: loggerName.log loggerName.wf.log
       logLevel    - msg above the logLevel will be displayed
                     DEBUG < INFO < WARNING < ERROR < CRITICAL
                     the default value is logging.DEBUG
       logDir      - directory to store log files
                     the default dir is 
                     /home/work/PythonCode/log + loggerName                     
                     e.g., /home/work/PythonCode/log/gtc/bfe_reader
       formatStr   - format of the log
                     default format:
                     date time [level][file:lineno]: msg
                     e.g., 2013-01-28 10:10:33,105 [ERROR][test.py:1]: test
       when        - how to split the log file by time interval
                     'S' : Seconds
                     'M' : Minutes
                     'H' : Hours
                     'D' : Days
                     'W' : Week day
                     default value: 'D'
       backupCount - how many backup file to keep
                     default value: 7
       stdout      - whether output to stdout
                     default value: True                     

     RETURNs: 
        logger or None
    """
    # Generate directory path of log
    if logDir == None:
        logDir = _logPathGen(loggerName)
        
    # check, and create dir if nonexist
    if _logDirCheckAndCreate(logDir) != 'OK':
        logging.error("logInit(), in _logDirCheckAndCreate(%s)" % logDir)
        return None      

    # set log file name
    _logFileName = _fileNameGen(loggerName, logDir)
    # warning and fatal
    _logWfFileName = _fileNameGen(loggerName, logDir, True)
    
    # set format
    if formatStr == None:
        formatStr = ('%(asctime)s [%(levelname)s][%(filename)s:%(lineno)s]:'
                     ' %(message)s')
    formatter = logging.Formatter(formatStr)

    logger = logging.getLogger(loggerName)
    # root logger is created with level WARNING, modify it
    logger.setLevel(logLevel)
    
    # prepare handler for file rotate, all log
    logHandler = logging.handlers.TimedRotatingFileHandler( \
                    _logFileName, when=when, backupCount=backupCount)
    logHandler.setLevel(logLevel)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    # prepare handler for file rotate, > WARNING
    logHandler = logging.handlers.TimedRotatingFileHandler( \
                    _logWfFileName, when=when, backupCount=backupCount)
    logHandler.setLevel(logging.WARNING)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    # prepare handler for stdout
    if stdout:
        logHandler = logging.StreamHandler()
        logHandler.setLevel(logLevel)
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
    # do not propagate
    logger.propagate = False
    return logger


def initRootLogger(progName=os.path.basename(sys.argv[0]).replace(".", "_"), logLevel=logging.DEBUG, logDir=None, formatStr=None, \
            when='MIDNIGHT', backupCount=7, stdout=True):
    """
     logInit - initialize log module
    
     ARGs:
       progName    - name of the program, e.g., 'gtc.bfe_reader'
                     log file: progName.log progName.wf.log
       logLevel    - msg above the logLevel will be displayed
                     DEBUG < INFO < WARNING < ERROR < CRITICAL
                     the default value is logging.DEBUG
       logDir      - directory to store log files
                     the default dir is 
                     /home/work/PythonCode/log + progName                     
                     e.g., /home/work/PythonCode/log/gtc/bfe_reader
       formatStr   - format of the log
                     default format:
                     date time [level][file:lineno]: msg
                     e.g., 2013-01-28 10:10:33,105 [ERROR][test.py:1]: test
       when        - how to split the log file by time interval
                     'S' : Seconds
                     'M' : Minutes
                     'H' : Hours
                     'D' : Days
                     'W' : Week day
                     default value: 'D'
       backupCount - how many backup file to keep
                     default value: 7
       stdout      - whether output to stdout
                     default value: True                     

     RETURNs: 
        root logger or None
    """
    # Generate directory path of log
    if logDir == None:
        logDir = _logPathGen(progName)
        
    # check, and create dir if nonexist
    if _logDirCheckAndCreate(logDir) != 'OK':
        logging.error("logInit(), in _logDirCheckAndCreate(%s)" % logDir)
        return None

    # set log file name
    _logFileName = _fileNameGen(progName, logDir)
    # warning and fatal
    _logWfFileName = _fileNameGen(progName, logDir, True)
    
    # set format
    if formatStr == None:
        formatStr = ('%(asctime)s [%(levelname)s][%(filename)s:%(lineno)s]:'
                     ' %(message)s')
    formatter = logging.Formatter(formatStr)

    logger = logging.getLogger()
    # root logger is created with level WARNING, modify it
    logger.setLevel(logLevel)
    
    # prepare handler for file rotate, all log
    logHandler = logging.handlers.TimedRotatingFileHandler( \
                    _logFileName, when=when, backupCount=backupCount)
    logHandler.setLevel(logLevel)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    # prepare handler for file rotate, > WARNING
    logHandler = logging.handlers.TimedRotatingFileHandler( \
                    _logWfFileName, when=when, backupCount=backupCount)
    logHandler.setLevel(logging.WARNING)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    # prepare handler for stdout
    if stdout:
        logHandler = logging.StreamHandler()
        logHandler.setLevel(logLevel)
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)

    return logger


if __name__ == '__main__':
    logging.info('hello world')


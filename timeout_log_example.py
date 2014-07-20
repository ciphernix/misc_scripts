#!/usr/bin/env python

'''Example on how to use logging and create a timout exemption.
A timeout exception is needed when some process may block, eg.: 
you try to download a file but this may take a long time to timeout. Instead of
waiting for the default timeout, you can define your own'''

import logging
import logging.handlers
import signal
import sys
import time


#GLOBAL VARS
LOGFILE = "/tmp/log"
TIMEOUT = 5

def timeout(signum, frame):
    '''Timeout handler to be use with signal.SIGALRM.'''

    raise Exception("Timeout Error")


def notify(message,level="INFO:"):
    '''Writes to log. Will also write to stdout if running on a tty.'''

    is_tty = sys.stdout.isatty()
    if is_tty:
        print "%s %s" %(level,message)
    if "ERR" in level:
        log.error(message)
    else:
        log.info(message)


if __name__ == "__main__":
    #init log
    log = logging.getLogger("Log")
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=1048576, backupCount=3)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    ########Log###########

    signal.signal(signal.SIGALRM, timeout)
    try:
        signal.alarm(TIMEOUT)
        #Do something here,
        #if task takes longer than TIMEOUT, an exception is generated
        #e.g: try a simple time.sleep(timeout+1)
        time.sleep(TIMEOUT + 1)
    except Exception, why:
        notify("Failed! :%s" %why,"ERROR")
        sys.exit(-1)
    else:
        signal.alarm(0) #reset signal.alarm to 0

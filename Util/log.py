#encoding=utf-8
import logging.config
import logging
from ProjVar.var import ProjDirPath
print(ProjDirPath+"\\Conf\\"+"Logger.conf")
logging.config.fileConfig(ProjDirPath+"\\Conf\\"+"Logger.conf")
logger = logging.getLogger("example01")


def debug(message):
   print ("debug")
   logger.debug(message)

def error(message):
    print("error")
    logger.error(message)


def warning(message):
    logger.warning(message)


def info(message):
    logger.info(message)

if __name__=="__main__":
    debug("hi")
    info("gloryroad")
    warning("hello")
    error("something error!")
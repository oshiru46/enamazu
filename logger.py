import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("enamazu")


def getLogger(module_name):
    return logger.getChild(module_name)

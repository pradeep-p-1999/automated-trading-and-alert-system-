import logging
import datetime
LOG_FORMAT="%(levelname)s-%(asctime)s-%(message)s"
logging.basicConfig(filename=datetime.datetime.now().strftime('log\\logfile_%d_%m_%Y.log'),level=logging.DEBUG,format=LOG_FORMAT)
logger=logging.getLogger(__name__)
    

from Exception import *
import threading
from logging_config import *

class AtomicCounter:
    def __init__(self, initial=0):
        self.value = initial
        self.addition=0
        self._lock = threading.Lock()

    def increment(self, num=1):
        with self._lock:
            self.value += num
            return self.value

    def decrement(self, num=1):
        with self._lock:
            self.value -= num
            return self.value

    def Add(self,val1,val2):
        try:
            with self._lock:
                self.addition=val1+val2
                return self.addition
        except:
            logger.exception(PrintException())

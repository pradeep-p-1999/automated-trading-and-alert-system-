import queue
import threading
import array
from Exception import *
from time import *
from AutoIncrement import *
from logging_config import *

class CQueue():
    counter=0
    SendData=array.array('B')

    atocounter=AtomicCounter()
    def __init__(self):
        self.SendData=array.array('B')
        self._DataQ=queue.Queue()
        self.lock=threading.Condition()
        self.__iPackets=0

    def PacketsCanSend(self):
        @property
        def iPackets(self):
            return self.__iPackets
        @iPackets.setter
        def iPackets(self,val):
            self.__iPackets=val

    def IncrementCounter():
        try:
            self.iPackets=CQueue.atocounter.increment()
            if iPackets>0:
                with self.lock:
                    self.lock.set()
        except:
            logger.exception(PrintException())

    def DecrementCounter():
        if iPackets>0:
            iPackets=CQueue.atocounter.decrement()
        else:
            return

    def AddCounter(self,value):
        try:
            self.__iPackets=CQueue.atocounter.Add(self.__iPackets,value)
            if self.__iPackets>0:
                with self.lock:
                    self.lock.notifyAll()
        except:logger.exception(PrintException())



    def Enqueue(self,data):
        with self.lock:
            self._DataQ.put(data)
            try:
                self.lock.notify_all()
            except:
                logger.exception(PrintException())


    def DeQueue(self,val=None):
        try:
            if val ==True:
                with self.lock:
                    if self.IsDataPresent(True):
                        try:
                            data=self._DataQ.get()
                            return data
                        except:
                            logger.exception(PrintException())
                            return None
                    else:
                        return None
            else:
                with self.lock:
                    if self.IsDataPresent():
                        try:
                            data=self._DataQ.get()
                            return data
                        except:
                            logger.exception(PrintException())
                            return None
        except:
            logger.exception(PrintException())

    def IsDataPresent(self,value=None):
        if value is not None:
            while 1:
                if self._DataQ.empty() is True:
                    try:
                        self.lock.wait()
                    except:
                        logger.exception(PrintException())
                    finally:
                        self.lock.notify_all()
                else:
                    return True
        else:
            while 1:
                if self._DataQ.empty() is True:
                    try:
                        self.lock.wait()
                    except:
                        logger.exception(PrintException())
                    finally:
                        self.lock.notify_all()
                else:
                    return True

    def clear(self):
        with self.lock:
            self._DataQ.clear()

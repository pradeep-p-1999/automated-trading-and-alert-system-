from tkinter import ttk
import tkinter as tk
import sys
import threading
import queue
import time
from MainWindowGUI import *
from TapClient import *
import CQueue
from Exception import *

class MainWindow():
    count=0
    lstFeedScrips=[]
    StartRead=False
    i=0
    isSuccess=False
    Queue=CQueue.CQueue()


    ScriptNameList=[]
    dicReqIDTrack={}
    OrderSendflag=False
    def __init__(self):
        try:
            MainWindowGUI.MainWindowGUI.InitializeComponent()
        except:
            logger.exception(PrintException())

class ThreadStart(threading.Thread):
    def __init__(self,tName):
      threading.Thread.__init__(self,daemon=True)
      self._tName = tName

    def run(self):
        if self._tName=='ParseResponseQ':
            self.ParseResponseQ()
        elif self._tName=='ParseSendRequestQ':
            self.ParseSendRequestQ()


    def ParseResponseQ(self):
        '''Thread To log response and request'''
        try:
            while 1:
                outputtext=logOutputQueue.DeQueue(True)
                init.init.rqRecvText.insert('end',outputtext.strip()+'\n')
                init.init.rqRecvText.see('end')
                if MainWindow.isSuccess==True:
                    MainWindow.isSuccess==False
        except:
            logger.exception(PrintException())

    def ParseSendRequestQ(self):
        try:
            while 1:
                requestQueue=requestSentQueue.DeQueue(True)
                init.init.rqSendText.insert('end',requestQueue)
                init.init.rqSendText.see('end')
        except:
            logger.exception(PrintException())

class orders():
    def __init__(self):
        self._StockIndexInfo,self._ScriptName,self._Signal,self._open,self._datetime,self._FormulaName,self._SettingType,self._Exchange,self._ExchangeCode=None,None,None,None,None,None,None,None,None
        self._InstrumentName,self._Strikeprice,self._Expiry,self._APIReqID,self._SharuID,self._ExchangeOrdID,self._ConfrmType,self._ExcQty,self._ExcPrice,self._OrdDateTime,self._ExcDateTime,self._ExchangeSignal=None,None,None,None,None,None,None,None,None,None,None,None
        self._NetPosition,self._AvgPrice,self._Quantity,self._price=0,0,0,0

    @property
    def StockIndexInfo(self):return self._StockIndexInfo
    @StockIndexInfo.setter
    def StockIndexInfo(self,value):self._StockIndexInfo=value

    @property
    def ScriptName(self):return self._ScriptName
    @ScriptName.setter
    def ScriptName(self,value):self._ScriptName=value

    @property
    def Signal(self):return self._Signal
    @Signal.setter
    def Signal(self,value):self._Signal=value

    @property
    def NetPosition(self):return self._NetPosition
    @NetPosition.setter
    def NetPosition(self,value):self._NetPosition=value

    @property
    def open(self):return self._open
    @open.setter
    def open(self,value):self._open=value

    @property
    def datetime(self):return self._datetime
    @datetime.setter
    def datetime(self,value):self._datetime=value

    @property
    def FormulaName(self):return self._FormulaName
    @FormulaName.setter
    def FormulaName(self,value):self._FormulaName=value

    @property
    def SettingType(self):return self._SettingType
    @SettingType.setter
    def SettingType(self,value):self._SettingType=value

    @property
    def AvgPrice(self):return self._AvgPrice
    @AvgPrice.setter
    def AvgPrice(self,value):self._AvgPrice=value

    @property
    def Exchange(self):return self._Exchange
    @Exchange.setter
    def Exchange(self,value):self._Exchange=value

    @property
    def ExchangeCode(self):return self._ExchangeCode
    @ExchangeCode.setter
    def ExchangeCode(self,value):self._ExchangeCode=value

    @property
    def InstrumentName(self):return self._InstrumentName
    @InstrumentName.setter
    def InstrumentName(self,value):self._InstrumentName=value

    @property
    def Strikeprice(self):return self._Strikeprice
    @Strikeprice.setter
    def Strikeprice(self,value):self._Strikeprice=value

    @property
    def Expiry(self):return self._Expiry
    @Expiry.setter
    def Expiry(self,value):self._Expiry=value

    @property
    def Quantity(self):return self._Quantity
    @Quantity.setter
    def Quantity(self,value):self._Quantity=value

    @property
    def price(self):return self._price
    @price.setter
    def price(self,value):self._price=value

    @property
    def APIReqID(self):return self._APIReqID
    @APIReqID.setter
    def APIReqID(self,value):self._APIReqID=value

    @property
    def SharuID(self):return self._SharuID
    @SharuID.setter
    def SharuID(self,value):self._SharuID=value

    @property
    def ExchangeOrdID(self):return self._ExchangeOrdID
    @ExchangeOrdID.setter
    def ExchangeOrdID(self,value):self._ExchangeOrdID=value

    @property
    def ConfrmType(self):return self.ConfrmType
    @ConfrmType.setter
    def ConfrmType(self,value):self._ConfrmType=value

    @property
    def ExcQty(self):return self._ExcQty
    @ExcQty.setter
    def ExcQty(self,value):self._ExcQty=value

    @property
    def ExcPrice(self):return self._ExcPrice
    @ExcPrice.setter
    def ExcPrice(self,value):self._ExcPrice=value

    @property
    def OrdDateTime(self):return self._OrdDateTime
    @OrdDateTime.setter
    def OrdDateTime(self,value):self._OrdDateTime=value

    @property
    def ExcDateTime(self):return self._ExcDateTime
    @ExcDateTime.setter
    def ExcDateTime(self,value):self._ExcDateTime=value

    @property
    def ExchangeSignal(self):return self._ExchangeSignal
    @ExchangeSignal.setter
    def ExchangeSignal(self,value):self._ExchangeSignal=value

    @property
    def NetPosition(self):return self._NetPosition
    @NetPosition.setter
    def NetPosition(self,value):self._NetPosition=value

    @property
    def AvgPrice(self):return self._AvgPrice
    @AvgPrice.setter
    def AvgPrice(self,value):self._AvgPrice=value

    @property
    def Quantity(self):return self._Quantity
    @Quantity.setter
    def Quantity(self,value):self._Quantity=value

    @property
    def price(self):return self._price
    @price.setter
    def price(self,value):self._price=value

    def ToString():
        return "APIReqID : " + APIReqID + " SharekhanID : " + SharuID + "  ExchangeID : " + ExchangeOrdID + "Signal : "+Signal +" ExchangeSignal : "+ExchangeSignal +" NetPosition :"+NetPosition +"  Quantity : " + Quantity + " Price : " + price + " ConfirmationType : " + ConfrmType + " ExecuteQty : " + ExcQty + " ExecutePrice : " + ExcPrice



def main():
    MainWindow()

if __name__ == '__main__': main()

from tkinter import messagebox
import socket,asyncore
from CStructures import *
from init import *
from Constants import *
import threading,time
from CQueue import *
from threading import *
from CStructures import *
import MainWindow
from tkinter import ttk
import asyncio
import MainWindowGUI
from array import *
from profile import *
from logging_config import *
from Exception import *
import pandas as pd



tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectDone=threading.Event()

processFalg=False
flag=False

Queue=CQueue()
SendData=CQueue()
InData=CQueue()
LoginSendData=CQueue()
QueueTrade=CQueue()
lastAckTimeData=CQueue()
logOutputQueue=CQueue()
requestSentQueue=CQueue()
queueAmbi=CQueue()
queueProcessAmbi=CQueue()
tempSendData=CQueue()
b=MessageHeader(0)

class TapClient():
    receiveData=False
    ProcessData=False
    isConnection = False
    bytesToRemove=0
    TAPSequenceNumber=0
    DataReceived=0
    NewOrderRejected=0
    ModifyOrderRejected = 0
    CancelOrderRejected = 0
    OrderAckReceived = 0
    SpreadAckReceived = 0
    TradeReceived = 0
    bolLogin = True
    bolConnected = False
    data={}
    dicseg=set()
    Symlist=set()

    def __init__(self):
        pass

    def connect(self):
        try:
            TapClient.connection(constants.TapIp, constants.TapPort)
            return True
        except:
            logger.exception(PrintException())
            return False

    def connection(host_ip,server_port):
        try:
            try:
                threading.Thread(target=TapClient.ConnectCallback, args=(host_ip,server_port,),daemon=True).start()
                connectDone.wait()
            except:
                logger.exception(PrintException())
                messagebox.showwarning('error','''Can't Connect''')
            return True
        except:
            logger.exception(PrintException())
            return False

    def ConnectCallback(host_ip, server_port):
        try:
            while 1:
                if TapClient.isconnected()==False:
                    tcp_client.connect((host_ip, server_port))
                    logOutputQueue.Enqueue("TT Connected...")
                    logger.info("Connection started On  IP : " + str(host_ip) + "  Port: " + str(server_port))
                    connectDone.set()
                    TapClient.receiveData = True
                    tapClient.OnConnected(None,None)
                    if(TapClient.isconnected()==True):
                        TapClient.Receive()

        except socket.timeout as  exc:
            logger.exception(exc)
        except:
            logger.exception(PrintException())

    def OnConnected(self,status,discription):
        try:
            TapClient.TAPSequenceNumber = 1
            InData.PacketsCanSend = 1
            SendData.PacketsCanSend = 0
            LoginSendData.PacketsCanSend = 0
            TapClient.DataReceived = 0
            TapClient.NewOrderRejected = 0
            TapClient.ModifyOrderRejected = 0
            TapClient.CancelOrderRejected = 0
            TapClient.OrderAckReceived = 0
            TapClient.SpreadAckReceived = 0
            TapClient.TradeReceived = 0
            TapClient.ProcessData=True
            TapClient.bolLogin = True
            TapClient.bolConnected = False

            tapClient.StartThreads()
        except:
            logger.exception(PrintException())

    def isconnected():
        try:
            data=array('B')
            tcp_client.send(data)
            return True
        except:
            return False
            logger.exception(PrintException())

    def Receive():
        try:
            state=StateObject()
            state.worksocket=tcp_client
            if(TapClient.isconnected()==True):
                TapClient.ReceiveCallback()


        except:
            logger.exception(PrintException())

    def ReceiveCallback():
        try:
            stateObj=StateObject()
            while 1:
                bytesRead=tcp_client.recv(9999)
                InData.Enqueue(bytesRead)
                InData.AddCounter(1)
                TapClient.DataReceived+=1
        except:
            logger.exception(PrintException())


    def SendLoginRequest(self):
        try:
            Header=MessageHeader(constants.TranCode.LoginRequest)
            Header.Prop01MessageLength=constants.LoginRequestSize
            Header.Prop02TransactionCode=constants.TranCode.LoginRequest.value
            cLoginRequest=SignOn()
            cLoginRequest.Prop01Header=[Header.cMessageLength,Header.cTransactionCode]
            cLoginRequest.Prop02LoginId = constants.LoginId
            cLoginRequest.Prop03MemberPassword = constants.MemberPassword
            cLoginRequest.Prop04TradingPassword = constants.TradingPassword
            cLoginRequest.Prop05IP = constants.TapIp
            cLoginRequest.Prop06Reserved =""

            TapClient.SendRequest(cLoginRequest.StructToByte())
            requestSentQueue.Enqueue(cLoginRequest.ToString())
        except:
            logger.exception(PrintException())
            print("no acoount or internet")
            return False

    def SendRequest(loginCred):
        try:
            SendData.Enqueue(loginCred)
        except:
            logger.exception(PrintException())

    def SendScripMasterDownload(self):
        header=MessageHeader(1)
        header.Prop01MessageLength=constants.ScripMasterRequest
        header.Prop02TransactionCode=constants.TranCode.ScripMasterRequest
        NFScripMaster=ScripMasterRequest(1)
        NFScripMaster.Prop01Header=[header.cMessageLength,header.cTransactionCode]
        NFScripMaster.Prop02ExchangeCode=constants.NFExCode
        NFScripMaster.Prop03Reserved=''
        TapClient.SendRequest(NFScripMaster.StructToByte())
        requestSentQueue.Enqueue(NFScripMaster.ToString())

        NCScripMaster=ScripMasterRequest(1)
        NCScripMaster.Prop01Header=[header.cMessageLength,header.cTransactionCode]
        NCScripMaster.Prop02ExchangeCode=constants.NCExcode
        NCScripMaster.Prop03Reserved=''
        TapClient.SendRequest(NCScripMaster.StructToByte())
        requestSentQueue.Enqueue(NCScripMaster.ToString())
        BCScripMaster=ScripMasterRequest(1)
        BCScripMaster.Prop01Header=[header.cMessageLength,header.cTransactionCode]
        BCScripMaster.Prop02ExchangeCode=constants.BCExcode
        BCScripMaster.Prop03Reserved=''
        TapClient.SendRequest(BCScripMaster.StructToByte())
        requestSentQueue.Enqueue(BCScripMaster.ToString())

        RNScripMaster=ScripMasterRequest(1)
        RNScripMaster.Prop01Header=[header.cMessageLength,header.cTransactionCode]
        RNScripMaster.Prop02ExchangeCode=constants.RNExCode
        RNScripMaster.Prop03Reserved=''
        TapClient.SendRequest(RNScripMaster.StructToByte())
        requestSentQueue.Enqueue(RNScripMaster.ToString())
        RMScripMaster=ScripMasterRequest(1)
        RMScripMaster.Prop01Header=[header.cMessageLength,header.cTransactionCode]
        RMScripMaster.Prop02ExchangeCode=constants.RMExcode
        RMScripMaster.Prop03Reserved=''
        TapClient.SendRequest(RMScripMaster.StructToByte())
        requestSentQueue.Enqueue(RMScripMaster.ToString())

        MXScripMaster=ScripMasterRequest(1)
        MXScripMaster.Prop01Header=[header.cMessageLength,header.cTransactionCode]
        MXScripMaster.Prop02ExchangeCode=constants.MXExcode
        MXScripMaster.Prop03Reserved=''
        TapClient.SendRequest(MXScripMaster.StructToByte())
        requestSentQueue.Enqueue(MXScripMaster.ToString())

        NXScripMaster=ScripMasterRequest(1)
        NXScripMaster.Prop01Header=[header.cMessageLength,header.cTransactionCode]
        NXScripMaster.Prop02ExchangeCode=constants.NXExcode
        NXScripMaster.Prop03Reserved=''
        TapClient.SendRequest(NXScripMaster.StructToByte())
        requestSentQueue.Enqueue(NXScripMaster.ToString())


        return True

    def StartThreads(self):
        try:
             tapClient.StartThread( ['SendData','ListenSocket','InData'])
        except:
            logger.exception(PrintException())
    def StartThread(self,threadName):
        try:
            for threads in threadName:
                if threads=="ProcessXml":
                    thread=Thread(target=tapClient.ThreadProcessXml,args=(),daemon=True)
                    if thread.isAlive():
                        thread.stop()
                    thread.start()

                if threads=="ListenSocket":
                    thread=Thread(target=tapClient.ListenSocket,args=(),daemon=True)
                    if thread.isAlive():
                        thread.stop()
                    thread.start()

                if threads=="InData":
                    thread=Thread(target=tapClient.ThreadParseData,args=(),daemon=True)
                    if thread.isAlive():
                        thread.stop()
                    thread.start()

                if threads=="SendData":
                    thread=Thread(target=tapClient.ThreadSendData,args=(),daemon=True)
                    if thread.isAlive():
                        thread.stop()
                    thread.start()

                if threads=="SendLoginData":
                    thread=Thread(target=tapClient.ThreadSendLoginData,daemon=True)
                    if thread.isAlive():
                        thread.stop()
                    thread.start()
        except:
            logger.exception(PrintException())
    def ThreadProcessXml(self):
        while 1:
            try:
                TradeConfirm=QueueTrade.DeQueue()
                MainWindow.logOutPutQueue.Enqueue("Queue XML:"+TradeConfirm)
                if Tradeconfirm in MainWindow.dicReqIDTrack:
                    with lock:
                        pass1
            except:
                logger.exception(PrintException())

    def ListenSocket(self):
        try:
            while 1:
                if tcp_client.fileno() != -1:
                    isConnection = True
                else:
                    isConnection=False
        except:
            logger.warning(PrintException())


    def ThreadParseData(self):
        data=array('B')
        PartialBuffer=array('B')
        TotalBuffer=array('B')
        try:
            while TapClient.ProcessData:
                if TapClient.bytesToRemove>0 or len(PartialBuffer)>0:
                    TotalBuffer=array('B')
                    TotalBuffer.extend(PartialBuffer)
                    bytesToRemove=0
                    PartialBuffer=array('B')

                if tapClient.CheckCompletePacket(TotalBuffer) == False:
                    data=InData.DeQueue()
                    TotalBuffer.extend(data)
                else:
                    messageHeader=array('B')
                    messageHeader.extend(TotalBuffer[0:constants.MsgHeaderSize])
                    header=MessageHeader(0)
                    header.ByteToStruct(messageHeader)
                    transactioncode=header.cTransactionCode[0]
                    if transactioncode==1:
                        loginResponse=LoginResponse(1)
                        loginResponse.ByteToStruct(TotalBuffer)
                        if(loginResponse.cStatusCode==0):
                            isSuccess=True
                        else:
                            isSuccess=False

                        logOutputQueue.Enqueue('\n'+loginResponse.ToString())
                    elif transactioncode==2:
                        MainWindow.MainWindow.logOutputQueue.EnQueue("\n" + "LogOff done Successfully");
                    elif transactioncode==21:
                        scripMasterResponse=ScripMasterResponse(1)
                        scripMasterResponse.ByteToStruct(TotalBuffer)
                        numberOfScrips=0
                        sourceIndex = 0

                        if scripMasterResponse.cExchangeCode[0:]=='NF':
                            nfData=array('B')
                            nfData.extend(TotalBuffer[8:header.cMessageLength[0]])
                            numberOfScrips=len(nfData)/constants.DerivativeMasterItemSize
                            dicNfScripMaster={}
                            dicTokenvsNF={}
                            for i in range(int(numberOfScrips)):
                                nfScripMaster=NFScripMaster(True)
                                nfScripData=array('B')
                                nfScripData.extend(nfData[sourceIndex:sourceIndex+constants.DerivativeMasterItemSize])
                                nfScripMaster.ByteToStruct(nfScripData)

                                if nfScripMaster.cScripShortName.strip(' \x00') not in dicNfScripMaster:
                                    dicNfScripMaster.update({nfScripMaster.cScripShortName.strip(' \x00'):[nfScripMaster.cDataLength[0:],nfScripMaster.cDerivativeType[0:].strip(' \x00'),nfScripMaster.cScripCode[0:].strip(' \x00'),nfScripMaster.cScripShortName[0:].strip(' \x00'),nfScripMaster.cExpiryDate[0:].strip(' \x00'),nfScripMaster.cFutOption[0:].strip(' \x00'),nfScripMaster.cStrikePrice[0:],nfScripMaster.cLotSize[0:]]})

                                sourceIndex+=constants.DerivativeMasterItemSize

                            MainWindowGUI.FeedRequest.LoadScripmaster(dicNfScripMaster,scripMasterResponse.Prop02ExchangeCode)
                            logOutputQueue.Enqueue('\n'+scripMasterResponse.ToString()+'||'+str(next(iter(dicNfScripMaster.values()))))

                        elif scripMasterResponse.cExchangeCode[0:]=='NC':
                            ncData=array('B')
                            ncData.extend(TotalBuffer[8:header.cMessageLength[0]])
                            numberOfScrips=len(ncData)/constants.CashcripMasterSize
                            sourceIndex = 0
                            dicNcScripMaster={}
                            dicBcScripMaster={}

                            for i in range(int(numberOfScrips)):
                                ncScripMaster=NCScripMaster(True)
                                ncScripData=array('B')
                                ncScripData.extend(ncData[sourceIndex:sourceIndex+constants.CashcripMasterSize])

                                ncScripMaster.ByteToStruct(ncScripData)
                                if ncScripMaster.cScripShortName.strip(' \x00') not in dicNcScripMaster:
                                    dicNcScripMaster.update({ncScripMaster.cScripShortName.strip(' \x00'):[ncScripMaster.cDataLength[0:],ncScripMaster.CSegment[0:].strip(' \x00'),ncScripMaster.cScripCode[0:].strip(' \x00'),ncScripMaster.cScripShortName[0:].strip(' \x00')]})

                                sourceIndex+=constants.CashcripMasterSize
                            MainWindowGUI.FeedRequest.LoadScripmaster(dicNcScripMaster,scripMasterResponse.Prop02ExchangeCode)
                            logOutputQueue.Enqueue('\n'+scripMasterResponse.ToString()+'||'+str(next(iter(dicNcScripMaster.values()))))
                        elif scripMasterResponse.cExchangeCode[0:]=='BC':
                            ncData=array('B')
                            ncData.extend(TotalBuffer[8:header.cMessageLength[0]])
                            numberOfScrips=len(ncData)/constants.CashcripMasterSize
                            sourceIndex = 0
                            dicNcScripMaster={}
                            dicBcScripMaster={}

                            for i in range(int(numberOfScrips)):
                                ncScripMaster=NCScripMaster(True)
                                ncScripData=array('B')
                                ncScripData.extend(ncData[sourceIndex:sourceIndex+constants.CashcripMasterSize])

                                ncScripMaster.ByteToStruct(ncScripData)

                                if ncScripMaster.cScripShortName.strip(' \x00') not in dicBcScripMaster:
                                    dicBcScripMaster.update({ncScripMaster.cScripShortName.strip(' \x00'):[ncScripMaster.cDataLength[0:],ncScripMaster.CSegment[0:].strip(' \x00'),ncScripMaster.cScripCode[0:].strip(' \x00'),ncScripMaster.cScripShortName[0:].strip(' \x00')]})
                                sourceIndex+=constants.CashcripMasterSize

                            MainWindowGUI.FeedRequest.LoadScripmaster(dicBcScripMaster,scripMasterResponse.Prop02ExchangeCode)
                            logOutputQueue.Enqueue('\n'+scripMasterResponse.ToString()+'||'+str(next(iter(dicBcScripMaster.values()))))

                        elif scripMasterResponse.cExchangeCode[0:]=='RN':

                            rnData=array('B')
                            rnData.extend(TotalBuffer[8:header.cMessageLength[0]])
                            numberOfScrips=len(rnData)/constants.CurrencycripMasterSize
                            sourceIndex = 0
                            dicRNScripMaster={}
                            dicRMScripMaster={}

                            for i in range(int(numberOfScrips)):
                                currencycripMaster=RNScripMaster(True)
                                scripData=array('B')
                                scripData.extend(rnData[sourceIndex:sourceIndex+constants.CurrencycripMasterSize])

                                currencycripMaster.ByteToStruct(scripData)

                                if currencycripMaster.cScripShortName.strip(' \x00') not in dicRNScripMaster:
                                    dicRNScripMaster.update({currencycripMaster.cScripShortName.strip(' \x00'):[currencycripMaster.cDataLength[0:],currencycripMaster.cCurrencyType[0:].strip(' \x00'),currencycripMaster.cScripCode[0:].strip(' \x00'),currencycripMaster.cScripShortName[0:].strip(' \x00'),currencycripMaster.cExpiryDate[0:].strip(' \x00'),currencycripMaster.cFutOption[0:].strip(' \x00'),currencycripMaster.cStrikePrice[0:],
                                    currencycripMaster.cLotSize[0:],currencycripMaster.cDisplayLotSize[0:],currencycripMaster.cLotType[0:].strip(' \x00'),currencycripMaster.cDisplayLotType[0:].strip(' \x00'),currencycripMaster.cOFType[0:].strip(' \x00'),currencycripMaster.cMinimumTradeQty[0:],currencycripMaster.cPriceTick[0:].strip(' \x00'),currencycripMaster.cMultipler[0:]]})

                                sourceIndex+=constants.CurrencycripMasterSize

                            MainWindowGUI.FeedRequest.LoadScripmaster(dicRNScripMaster,scripMasterResponse.Prop02ExchangeCode)
                            logOutputQueue.Enqueue('\n'+scripMasterResponse.ToString()+'||'+str(next(iter(dicRNScripMaster.values()))))

                        elif scripMasterResponse.cExchangeCode[0:]=='RM':
                            rnData=array('B')
                            rnData.extend(TotalBuffer[8:header.cMessageLength[0]])
                            numberOfScrips=len(rnData)/constants.CurrencycripMasterSize
                            sourceIndex = 0
                            dicRNScripMaster={}
                            dicRMScripMaster={}

                            for i in range(int(numberOfScrips)):
                                currencycripMaster=RNScripMaster(True)
                                scripData=array('B')
                                scripData.extend(rnData[sourceIndex:sourceIndex+constants.CurrencycripMasterSize])

                                currencycripMaster.ByteToStruct(scripData)

                                if ncScripMaster.cScripShortName.strip(' \x00') not in dicRMScripMaster:
                                    dicRMScripMaster.update({currencycripMaster.cScripShortName.strip(' \x00'):[currencycripMaster.cDataLength[0:],currencycripMaster.cCurrencyType[0:].strip(' \x00'),currencycripMaster.cScripCode[0:].strip(' \x00'),currencycripMaster.cScripShortName[0:].strip(' \x00'),currencycripMaster.cExpiryDate[0:].strip(' \x00'),currencycripMaster.cFutOption[0:].strip(' \x00'),currencycripMaster.cStrikePrice[0:],
                                    currencycripMaster.cLotSize[0:],currencycripMaster.cDisplayLotSize[0:],currencycripMaster.cLotType[0:].strip(' \x00'),currencycripMaster.cDisplayLotType[0:].strip(' \x00'),currencycripMaster.cOFType[0:].strip(' \x00'),currencycripMaster.cMinimumTradeQty[0:],currencycripMaster.cPriceTick[0:].strip(' \x00'),currencycripMaster.cMultipler[0:]]})

                                sourceIndex+=constants.CurrencycripMasterSize

                            MainWindowGUI.FeedRequest.LoadScripmaster(dicRMScripMaster,scripMasterResponse.Prop02ExchangeCode)
                            logOutputQueue.Enqueue('\n'+scripMasterResponse.ToString()+'||'+str(next(iter(dicRMScripMaster.values()))))

                    elif transactioncode==22:
                        feedResponse=FeedResponse(1)
                        feedResponse.ByteToStruct(TotalBuffer)
                        token=feedResponse.cScripToken


                        if token not in MainWindowGUI.FeedRequest.DicFeedsRespone:
                            MainWindowGUI.FeedRequest.DicFeedsRespone.update({token:[feedResponse.cHeader[0:],feedResponse.cScripToken[0:],feedResponse.cLTPrice,feedResponse.cLTQuantity,feedResponse.cLTDate[0:],feedResponse.cBidPrice,feedResponse.cBidQuantity,feedResponse.cOfferPrice,feedResponse.cOfferQuantity,feedResponse.cTotalTradedQty,feedResponse.cTotalTradedQty,feedResponse.cTradedQuantity,feedResponse.cAverageTradePrice]})

                            attribut=[str(attr)+':'+str(val)  for (attr,val) in feedResponse.__dict__.items()]
                            MainWindowGUI.FeedRequest.DicFeedsRespone.update({token:attribut})

                            feedResponsestr=feedResponse.ToString()
                            logOutputQueue.Enqueue('Feed Response :'+feedResponsestr)


                        strsss=TapClient.getKeysByValues(token)

                        TapClient.data.update({strsss:[feedResponse.cLTDate.strip('\x00 '),feedResponse.cLTPrice/100,feedResponse.cBidPrice/100,feedResponse.cBidQuantity,feedResponse.cOfferPrice/100,feedResponse.cOfferQuantity]})

                        init.init.treeview.delete(*init.init.treeview.get_children())

                        for k,v in TapClient.data.items():

                            if k not in TapClient.Symlist:
                                init.init.treeview.insert('','end',text=(k),values=(v[0:]))
                            if k in TapClient.Symlist:
                                init.init.treeview.insert('','end',text=(k),values=(v[0:]))

                        children =init.init.treeview.get_children()
                        for child in children:
                            TapClient.Symlist.add(init.init.treeview.item(child)['text'])


                    elif transactioncode==26:
                        depthResponse=MarketDepthResponse(1)
                        depthResponse.ByteToStruct(TotalBuffer)
                        token=depthResponse.cScripCode
                        if token not in MainWindowGUI.FeedRequest.DicMarketDepthResponse:
                            attribut=[str(attr)+':'+str(val)  for (attr,val) in depthResponse.__dict__.items()]
                            MainWindowGUI.FeedRequest.DicMarketDepthResponse.update({token:attribut})
                            logOutputQueue.Enqueue('Depth Response : '+depthResponse.ToString())

                    elif transactioncode==11:    #soc
                        soc=SharekhanOrderConfirmation(1)

                        soc.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue("SharekhanOrderConfirmation : "+soc.ToString())
                        if soc.cRequestID not in MainWindowGUI.FeedRequest.DicSharekhanOrderResponse:
                            MainWindowGUI.FeedRequest.DicSharekhanOrderResponse.update({soc.cRequestID[0:]:[MessageHeader.ToString(soc.cHeader),soc.cRequestID[0:],soc.cExchangeCode[0:],soc.cCount,soc.cOrderConfirmationItems[0:]]})

                        logger.info("SharekhanOrderConfirmation :"+soc.ToString())
                        self.diclock=threading.Condition()


                    elif transactioncode==13:
                        orderConfirmation=ExchangeTradeConfirmation(1)
                        orderConfirmation.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue('Exchange Order Confirmation :'+orderConfirmation.ToString())

                        if orderConfirmation.cSharekhanOrderID.replace('\0','').strip(' ') in MainWindowGUI.FeedRequest.dicSharekhanIDvsAPIReqID:
                            APIReqID=MainWindowGUI.FeedRequest.dicSharekhanIDvsAPIReqID[orderConfirmation.cSharekhanOrderID.replace('\0','').strip(' ')]

                            self.diclock=threading.Condition()
                            with self.diclock:
                                order=MainWindow.orders()
                                order=MainWindowGUI.FeedRequest.dicReqIDTrack[APIReqID]
                                order.ExchangeOrdID=orderConfirmation.cExchangeOrderId.replace('\0','').strip(' ')
                                order.ExchangeSignal=orderConfirmation.cBuySell
                                order.ConfrmType="ExchangeConfirmation"
                                logger.info("Exchange Order Confirmation :"+order.ToString())

                    elif transactioncode==14:
                        tradeConfirmation=ExchangeTradeConfirmation(1)
                        tradeConfirmation.ByteToStruct(TotalBuffer)
                        self.diclock=threading.Condition()
                        with self.diclock:
                            if tradeConfirmation.cSharekhanOrderID.replace('\0','').strip(' ') not in MainWindowGUI.FeedRequest.dicTradeConfirm:
                                attribut=[str(attr)+':'+str(val)  for (attr,val) in tradeConfirmation.__dict__.items()]
                                MainWindowGUI.FeedRequest.dicTradeConfirm.update({tradeConfirmation.cExchangeCode.replace('\0','').strip(' '):attribut})
                            else:
                                MainWindowGUI.FeedRequest.dicTradeConfirm[tradeConfirmation.cSharekhanOrderID.replace('\0','').strip(' ')]=attribut
                        QueueTrade.Enqueue(tradeConfirmation.cSharekhanOrderID.replace('\0','').strip(' '))

                    elif transactioncode==31:
                        objTransCode31=ReportResponse(1)
                        objTransCode31.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode31.ToString())

                        for i in range(objTransCode31.cRecordCount[0]):

                            logOutputQueue.Enqueue("Record Number : " + str(i))
                            objReportResponse=EquityOrderReportItem(1)
                            objReportResponse.ByteToStruct(TotalBuffer)
                            logOutputQueue.Enqueue(objReportResponse.ToString())

                    elif transactioncode==32:
                        objTransCode32=ReportResponse(1)
                        objTransCode32.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode32.ToString())

                        for i in range(objTransCode32.cRecordCount[0]):

                            logOutputQueue.Enqueue("Record Number : " + str(i))
                            DPSRReport=DPSRReportItem(1)
                            DPSRReport.ByteToStruct(TotalBuffer)
                            logOutputQueue.Enqueue(DPSRReport.ToString())

                    elif transactioncode==33:
                        objTransCode33=ReportResponse(1)
                        objTransCode33.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode33.ToString())

                        cashOrderStart=0
                        cashOrderEnd=0
                        if objTransCode33.cRecordCount[0]>0:
                            for i in range(objTransCode33.cRecordCount[0]):
                                FixSize=461
                                if i==0:
                                    cashOrderStart=10
                                    cashOrderEnd=10+FixSize
                                else:
                                    cashOrderStart=cashOrderEnd
                                    cashOrderEnd=cashOrderStart+FixSize
                                Report=array('B')
                                Report.extend(TotalBuffer[0:FixSize])
                                logOutputQueue.Enqueue('Record Number :'+str(i))
                                CashOrderDetailsReportItemResponse=CashOrderDetailsReportItem(1)
                                CashOrderDetailsReportItemResponse.ByteToStruct(Report)
                                logOutputQueue.Enqueue(CashOrderDetailsReportItemResponse.ToString())

                    elif transactioncode==34:
                        objTransCode34=ReportResponse(1)
                        objTransCode34.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode34.ToString())

                        cashOrderStart=0
                        cashOrderEnd=0
                        if objTransCode34.cRecordCount[0]>0:
                            for i in range(objTransCode34.cRecordCount):
                                FixSize=294
                                if i==0:
                                    cashOrderStart=10
                                    cashOrderEnd=10+FixSize
                                else:
                                    cashOrderStart=cashOrderEnd+100
                                    cashOrderEnd=cashOrderStart+FixSize+100
                                Report=array('B')
                                Report.extend(TotalBuffer[0:FixSize])
                                logOutputQueue.Enqueue('Record Number :'+str(i))
                                CashTradeDetailsReport=CashTradeDetailsReportItem(1)
                                CashTradeDetailsReport.ByteToStruct(Report)
                                logOutputQueue.Enqueue(CashTradeDetailsReport.ToString())

                    elif transactioncode==35:
                        objTransCode35=ReportResponse(1)
                        objTransCode35.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode35.ToString())

                        for i in range(objTransCode35.cRecordCount[0]):

                            logOutputQueue.Enqueue("Record Number : " + str(i))
                            cashLimitReportItem=CashLimitReportItem(1)
                            cashLimitReportItem.ByteToStruct(TotalBuffer)
                            logOutputQueue.Enqueue(cashLimitReportItem.ToString())

                    elif transactioncode==36:
                        objTransCode36=ReportResponse(1)
                        objTransCode36.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode36.ToString())

                        for i in range(objTransCode36.cRecordCount[0]):

                            logOutputQueue.Enqueue("Record Number : " + str(i))
                            cashNetPositionReportItem=CashNetPositionReportItem(1)
                            cashNetPositionReportItem.ByteToStruct(TotalBuffer)
                            logOutputQueue.Enqueue(cashNetPositionReportItem.ToString())

                    elif transactioncode==41:
                        objTransCode41=ReportResponse(1)
                        objTransCode41.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode41.ToString())

                        for i in range(objTransCode41.cRecordCount[0]):

                            logOutputQueue.Enqueue("Record Number : " + str(i))
                            derivativeOrderReportItem=DerivativeOrderReportItem(1)
                            derivativeOrderReportItem.ByteToStruct(TotalBuffer)
                            logOutputQueue.Enqueue(derivativeOrderReportItem.ToString())

                    elif transactioncode==42:
                        objTransCode42=ReportResponse(1)
                        objTransCode42.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode42.ToString())

                        for i in range(objTransCode42.cRecordCount[0]):

                            logOutputQueue.Enqueue("Record Number : " + str(i))
                            turnOverReportItem=TurnOverReportItem(1)
                            turnOverReportItem.ByteToStruct(TotalBuffer)
                            logOutputQueue.Enqueue(turnOverReportItem.ToString())

                    elif transactioncode==43:
                        objTransCode43=ReportResponse(1)
                        objTransCode43.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode43.ToString())

                        Reportstartind=0
                        Reortendind=0
                        if objTransCode43.cRecordCount[0]>0:
                            for i in range(objTransCode43.cRecordCount[0]):
                                FixSize=764
                                if i==0:
                                    Reportstartind=10
                                    Reortendind=10+FixSize
                                else:
                                    Reportstartind=Reortendind
                                    Reortendind=Reportstartind+FixSize
                                Report=array('B')
                                Report.extend(TotalBuffer[0:FixSize])
                                logOutputQueue.Enqueue('Record Number :'+str(i))
                                objDerOrdDetailReport=DerivativeOrderDetailReportItem(1)
                                objDerOrdDetailReport.ByteToStruct(Report)
                                logOutputQueue.Enqueue(objDerOrdDetailReport.ToString())


                    elif transactioncode==44:
                        objTransCode44=ReportResponse(1)
                        objTransCode44.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode44.ToString())

                        fnotradeStart=0
                        fnotradeEnd=0
                        if objTransCode44.cRecordCount[0]>0:
                            for i in range(objTransCode44.cRecordCount):
                                FixSize=364
                                if i==0:
                                    fnotradeStart=10
                                    fnotradeEnd=10+FixSize
                                else:
                                    fnotradeStart=fnotradeEnd+100
                                    fnotradeEnd=fnotradeStart+FixSize+100
                                Report=array('B')
                                Report.extend(TotalBuffer[0:FixSize])
                                logOutputQueue.Enqueue('Record Number :'+str(i))
                                objDerTradeDetail=DerivativeTradeDetailsReportItem(1)
                                objDerTradeDetail.ByteToStruct(Report)
                                logOutputQueue.Enqueue(objDerTradeDetail.ToString())

                    elif transactioncode==54:
                        objTransCode54=ReportResponse(1)
                        objTransCode54.ByteToStruct(TotalBuffer)
                        logOutputQueue.Enqueue(objTransCode54.ToString())

                        for i in range(objTransCode54.cRecordCount[0]):

                            logOutputQueue.Enqueue("Record Number : " + str(i))
                            objcmdLimit=CommodityLimitReportItem(1)
                            objcmdLimit.ByteToStruct(TotalBuffer)
                            logOutputQueue.Enqueue(objcmdLimit.ToString())

                    if header.cMessageLength[0] <len(TotalBuffer):
                        bytesToRemove=header.cMessageLength[0]
                        PartialBuffer=TotalBuffer[bytesToRemove:]

                    TotalBuffer=array('B')

        except:
            logger.exception(PrintException())

    def getKeysByValues(token):
        try:
            l = ""
            seg=init.init.selectedSegment
            if seg+':'+token not in TapClient.dicseg:
                TapClient.dicseg.add(seg+':'+token)
            dicsegval=TapClient.dicseg
            for segment in dicsegval:
                ss=segment.split(':')
                if ss[0]=='NC':
                    for k, v in MainWindowGUI.FeedRequest.ncScripMaster.items():
                        if token.strip('\x00 ') == v[2]:
                            l=k
                            return l
                elif ss[0]=='NF':
                    for k, v in MainWindowGUI.FeedRequest.nfScripMaster.items():
                        if token.strip('\x00 ') == v[2]:
                            l=k
                            return l
                elif ss[0]=='RN':
                    for k, v in MainWindowGUI.FeedRequest.rnScripMaster.items():
                        if token.strip('\x00 ') == v[2]:
                            l=k
                            return l
                elif ss[0]=='RM':
                    for k, v in MainWindowGUI.FeedRequest.rmScripMaster.items():
                        if token.strip('\x00 ') == v[2]:
                            l=k
                            return l
                elif ss[0]=='BC':
                    for k, v in MainWindowGUI.FeedRequest.bcScripMaster.items():
                        if token.strip('\x00 ') == v[2]:
                            l=k
                            return l
                elif ss[0]=='NX':
                    for k, v in MainWindowGUI.FeedRequest.nxScripMaster.items():
                        if token.strip('\x00 ') == v[2]:
                            l=k
                            return l
                elif ss[0]=='MX':
                    for k, v in MainWindowGUI.FeedRequest.mxScripMaster.items():
                        l=k
                        if token.strip('\x00 ') == v[2]:
                            return l
        except:
            logger.exception(PrintException())

    def CheckCompletePacket(self,TotalBuffer):
        try:
            if len(TotalBuffer)>0:
                messageHeader=array('B')
                messageHeader=TotalBuffer[0:constants.MsgHeaderSize]
                header=MessageHeader(0)
                header.ByteToStruct(messageHeader)
                if header.cTransactionCode==0:
                    return True
                else:
                    if header.cMessageLength[0] <= len(TotalBuffer):
                        return True
                    else:
                        return False
            else:
                return False

        except:
            logger.exception(PrintException())
            return False

    def ThreadSendData(self):
        while TapClient.ProcessData:
            try:
                if processFalg==False:
                    data=SendData.DeQueue(True)
                    TapClient.Send(tcp_client,data)
            except:
                logger.exception(PrintException())

    def Send(socket,data):
        try:
            processFalg = True
            tcp_client.send(data)
            processFalg = False
        except:
            logger.exception(PrintException())

    def ThreadSendLoginData(self):
        while ProcessData:
            try:
                data=LoginSendData.DeQueue(true)
                send(tcp_client,data)
            except:
                logger.exception(PrintException())

    def SubscribeforFeeds(self,request):
        TapClient.SendRequest(request)

    def SendOrderReportRequest(self,p):
        TapClient.SendRequest(p)

class StateObject():
    def __init__(self):
        self.worksocket=None
        buffer=array('B')
        data=array('B')


tapClient=TapClient()

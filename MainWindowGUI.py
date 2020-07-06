from tkinter import ttk
import init
from Constants import *
import pandas as pd

import threading
import alerter
import MainWindow
from TapClient import *
import tkinter as tk
from CStructures import *
from time import *
from Exception import *



class MainWindowGUI():
    def InitializeComponent():
        try:
            win = tk.Tk()
            win.title("MainWindow")

            tabControl = ttk.Notebook(win)
            Login = LoginGUI(tabControl)
            Feed_Request = FeedRequest(tabControl)
            Order_Report = OrderReport(tabControl)
            objstatus = Status(tabControl)
            objAlert= Alert(tabControl)


            tabControl.add(Login, text='Login')
            tabControl.add(Feed_Request, text='Feed Request')
            tabControl.add(Order_Report, text='Order Report')
            tabControl.pack(expand=1, fill="both")
            tabControl.add(objstatus, text='Status')
            tabControl.add(objAlert, text='Alert')

            scr=ScrollViewer(win)
            scr.pack(expand=1,fill='both')


            threadList = ["ParseResponseQ","ParseSendRequestQ","sendorder","ProcessAmbiOrdes"]
            for threads in threadList:
                thread=MainWindow.ThreadStart(threads)
                thread.start()

            win.mainloop()
        except:
            logger.exception(PrintException())


class LoginGUI(ttk.Frame):
    def __init__(self,parent):
        try:
            ttk.Frame.__init__(self,parent)
            init.init.addLables(self)
            init.init.addEntry(self)
            init.init.addButton(self)
        except:
            logger.exception(PrintException())


    def login_btn_evnt(self):
        try:
            if (len(self.LoginIdEntry.get())!=0 and len(self.MemberPswdEntry.get())!=0 and len(self.TradingpswdEntry.get())!=0  and len(self.IPAddEntry.get())!=0):
                constants.LoginId=self.LoginIdEntry.get()
                constants.MemberPassword=self.MemberPswdEntry.get()
                constants.TradingPassword=self.TradingpswdEntry.get()
                constants.TapIp=self.IPAddEntry.get()
                constants.TapPort=8000
                TapClient.connect(self)
                init.init.rqSendText.insert(INSERT,'connection done')
                TapClient.SendLoginRequest(self)
            else:
                messagebox.showwarning("Something Missing","Please Fill all fields")
        except:
            logger.exception(PrintException())

class FeedRequest(ttk.Frame):
    DicMarketDepthResponse={}
    DicFeedsRespone={}
    DicSharekhanOrderResponse={}
    dicReqIDTrack={}
    dicSharekhanIDvsAPIReqID={}
    dicTradeConfirm={}
    AutoInc=0
    ncScripMaster={}
    nfScripMaster={}
    rnScripMaster={}
    rmScripMaster={}
    bcScripMaster={}
    nxScripMaster={}
    mxScripMaster={}

    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        init.init.fr_addButtons(self)
        init.init.fr_addLables(self)
        init.init.fr_adddropdown(self)
        init.init.fr_addEntry(self)

    def btnScripMasterDownload_click(self):
        TapClient.SendScripMasterDownload(self)
        MainWindow.MainWindow.StartRead=True

    def LoadScripmaster(scripmaster,exchangeCode):
        try:


            if scripmaster is not None and exchangeCode==constants.NCExcode:
                FeedRequest.ncScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.NFExCode:
                FeedRequest.nfScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.RNExCode:
                FeedRequest.rnScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.RMExcode:
                FeedRequest.rmScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.BCExcode:
                FeedRequest.bcScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.NXExcode:
                FeedRequest.nxScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.MXExcode:
                FeedRequest.mxScripMaster.update(scripmaster)

        except:
            logger.exception(PrintException())

    def btnPlaceOrder_Click(self):
        '''click to place order after providing price and quantity'''
        try:
            #self.se_option.current()!=-1 and
            if( self.sec_option.current()!=-1 and len(self.PriceeEntery.get())!=0 and len(self.QtyEntry.get())!=0):
                header=MessageHeader(1)
                header.Prop01MessageLength=constants.OrderRequestSize
                header.Prop02TransactionCode=constants.TranCode.OrderRequest.value

                orderItem=OrderItem(True)
                orderItem.Prop01DataLength=constants.OrderItemSize
                orderItem.Prop02OrderID=''
                scripName=None

                selectedval=self.sec_var.get()
                selectedScrip=self.scrip_var.get()
                if selectedval=='NC':
                    for v in FeedRequest.ncScripMaster.values():
                        if v[3].split(' ')[0]==selectedScrip:
                            orderItem.Prop05ScripToken=v[2]

                if selectedval=='BC':
                    for v in FeedRequest.bcScripMaster.values():
                        if v[3].split(' ')[0]==selectedScrip:
                            orderItem.Prop05ScripToken=v[2]
                if selectedval=='NF':
                    scripvariable=self.scrip_var.get()
                    expiryvaribale=self.expiry_var.get()
                    instvar=self.instrument_var.get()
                    strikevar=self.strike_var.get()
                    if strikevar.endswith('.0'):
                        strikevar=strikevar.replace('.0','')

                    scripName=scripvariable+expiryvaribale+instvar+strikevar
                    if instvar=='FUT':
                        scripName=scripvariable+expiryvaribale
                    for x in FeedRequest.nfScripMaster.values():
                        if x[3].replace(' ','')==scripName:
                            orderItem.Prop05ScripToken=x[2]
                if selectedval=='RN':
                    scripvariable=self.scrip_var.get()
                    expiryvaribale=self.expiry_var.get()
                    instvar=self.instrument_var.get()
                    strikevar=self.strike_var.get()
                    if strikevar.endswith('.0'):
                        strikevar=strikevar.replace('.0','')
                    scripName=scripvariable+expiryvaribale+instvar+strikevar
                    for x in FeedRequest.rnScripMaster.values():
                        if x[3].replace(' ','')==scripName:
                            orderItem.Prop05ScripToken=x[2]
                if selectedval=='MX':
                    for v in FeedRequest.mxScripMaster.values():
                        if v[3].split(' ')[0]==selectedScrip:
                            orderItem.Prop05ScripToken=v[2]
                if selectedval=='RM':
                    for v in FeedRequest.rmScripMaster.values():
                        if v[3].split(' ')[0]==selectedScrip:
                            orderItem.Prop05ScripToken=v[2]
                if selectedval=='NX':
                    for v in FeedRequest.nxScripMaster.values():
                        if v[3].split(' ')[0]==selectedScrip:
                            orderItem.Prop05ScripToken=v[2]

                orderItem.Prop03CustomerID='139504'
                orderItem.Prop04S2KID=''
                orderItem.Prop06BuySell = "B"
                orderItem.Prop07OrderQty = int(self.QtyEntry.get())
                orderItem.Prop08OrderPrice = int(self.PriceeEntery.get())
                orderItem.Prop09TriggerPrice = 0
                orderItem.Prop10DisclosedQty = 0
                orderItem.Prop11ExecutedQty = 0
                orderItem.Prop12RMSCode = ""
                orderItem.Prop13ExecutedPrice = 0
                orderItem.Prop14AfterHour = "N"
                orderItem.Prop15GTDFlag = "IOC" #"GFD";
                orderItem.Prop16GTD = ""
                orderItem.Prop17Reserved = ""
                orderData=orderItem.StructToByte()
                FeedRequest.AutoInc=FeedRequest.AutoInc+1
                orderRequest=OrderRequest(1)
                orderRequest.Prop01Header=[header.cMessageLength,header.cTransactionCode]
                orderRequest.Prop03OrderCount=int(FeedRequest.AutoInc)
                orderRequest.Prop04ExchangeCode=str(selectedval)
                orderRequest.Prop05OrderType1='NEW'
                orderRequest.Prop02RequestID=str(FeedRequest.AutoInc)
                orderRequest.Prop07Reserved=''

                itemList=array('B')

                placeOrder=orderRequest.StructToByte(orderData)

                tapClient.SubscribeforFeeds(placeOrder)
                requestSentQueue.Enqueue(orderRequest.ToString())
                init.init.lb_orders.insert(END,selectedScrip)
            else:
                messagebox.showwarning('Please provide complete details...')
        except:
            logger.exception(PrintException())

    def SelectionChanged(self):
        '''select feed or depth to request'''
        if self.feedororder_option.current()!=-1:
            if self.feedororder_var.get()=='get feeds':
                optiontype=self.sec_var.get()
                if self.feedordepth_option.current()!=-1 and len(optiontype)!=0 and len(self.scrip_var.get())!=0 and len(self.se_var.get())!=0:
                    try:
                        scripName=None
                        if self.feedordepth_var.get()=='feed':
                            header=MessageHeader(1)
                            header.Prop01MessageLength=constants.FeedRequestSize
                            header.Prop02TransactionCode=constants.TranCode.FeedRequest
                            feedreq=FeedRequestF(1)
                            feedreq.Prop01Header=[header.cMessageLength,header.cTransactionCode]
                            feedreq.Prop02Count=1
                            selectedScrip=self.scrip_var.get()
                            if optiontype=='NC':
                                for v in FeedRequest.ncScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc

                            elif optiontype=='BC':
                                for v in FeedRequest.bcScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc

                            elif optiontype=='MX':
                                for v in FeedRequest.mxScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc
                            elif optiontype=='RM':
                                for v in FeedRequest.rmScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc

                            elif optiontype=='NX':
                                for v in FeedRequest.nxScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc

                            elif optiontype=='NF':
                                if self.instrument_var.get()!='FUT':
                                    scripvariable=self.scrip_var.get()
                                    expiryvaribale=self.expiry_var.get()
                                    instvar=self.instrument_var.get()
                                    strikevar=self.strike_var.get()
                                    if strikevar.endswith('.0'):
                                        strikevar=strikevar.replace('.0','')

                                    scripName=scripvariable+expiryvaribale+instvar+strikevar
                                else:
                                    scripName=scripvariable+expiryvaribale
                                for x in FeedRequest.nfScripMaster.values():
                                    if x[3].replace(' ','')==scripName:
                                        feedreq.Prop03ScripList=optiontype+x[2]

                            elif optiontype=='RN':
                                scripvariable=self.scrip_var.get()
                                expiryvaribale=self.expiry_var.get()
                                instvar=self.instrument_var.get()
                                strikevar=self.strike_var.get()
                                if strikevar.endswith('.0'):
                                    strikevar=strikevar.replace('.0','')
                                scripName=scripvariable+expiryvaribale+instvar+strikevar
                                for x in FeedRequest.rnScripMaster.values():
                                    if x[3].replace(' ','')==scripName:
                                        feedreq.Prop03ScripList=optiontype+x[2]

                            feedreq.Prop04Reserved=''
                            requestSentQueue.Enqueue(feedreq.ToString())
                            tapClient.SubscribeforFeeds(feedreq.StructToByte())
                            init.init.lb_feeds.insert(END,selectedScrip)



                        elif self.feedordepth_var.get()=='depth':
                            header=MessageHeader(1)
                            header.Prop01MessageLength=constants.MarketDepthRequestSize
                            header.Prop02TransactionCode=constants.TranCode.DepthRequest

                            depthRequest=MarketDepthRequest(1)
                            depthRequest.Prop01Header=[header.cMessageLength,header.cTransactionCode]
                            selectedScrip=self.scrip_var.get()
                            if optiontype=='NC':
                                for v in FeedRequest.ncScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc

                            elif optiontype=='BC':
                                for v in FeedRequest.bcScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc

                            elif optiontype=='NF':
                                if self.instrument_var.get()!='FUT':
                                    scripvariable=self.scrip_var.get()
                                    expiryvaribale=self.expiry_var.get()
                                    instvar=self.instrument_var.get()
                                    strikevar=self.strike_var.get()
                                    if strikevar.endswith('.0'):
                                        strikevar=strikevar.replace('.0','')

                                    scripName=scripvariable+expiryvaribale+instvar+strikevar
                                else:
                                    scripName=scripvariable+expiryvaribale
                                for x in FeedRequest.nfScripMaster.values():
                                    if x[3].replace(' ','')==scripName:
                                        depthRequest.Prop03ScripCode=x[2]

                            elif optiontype=='RN':
                                scripvariable=self.scrip_var.get()
                                expiryvaribale=self.expiry_var.get()
                                instvar=self.instrument_var.get()
                                strikevar=self.strike_var.get()
                                if strikevar.endswith('.0'):
                                    strikevar=strikevar.replace('.0','')
                                scripName=scripvariable+expiryvaribale+instvar+strikevar
                                for x in FeedRequest.rnScripMaster.values():
                                    if x[3].replace(' ','')==scripName:
                                        depthRequest.Prop03ScripCode=x[2]

                            elif optiontype=='NX':
                                for v in FeedRequest.nxScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc

                            elif optiontype=='MX':
                                for v in FeedRequest.mxScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc

                            elif optiontype=='RM':
                                for v in FeedRequest.rmScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc
                            depthRequest.Prop04Reserved=''
                            depthRequest.Prop02ExchangeCode=optiontype
                            requestSentQueue.Enqueue(depthRequest.ToString())
                            tapClient.SubscribeforFeeds(depthRequest.StructToByte())
                            init.init.lb_depth.insert(END,selectedScrip)


                    except:
                        logger.exception(PrintException())


class OrderReport(ttk.Frame):

    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        init.init.or_addButtons(self)
        init.init.or_addLables(self)
        init.init.or_adddropdown(self)

    def getreport(self):
        if self.cmbordereport_option.current()!=-1:
            header=MessageHeader(1)
            header.Prop01MessageLength=181
            selected_report=self.cmbordereport_var.get()
            transcode=0
            if selected_report=='Equity Order Report':transcode=31
            elif selected_report=='DPRS Report':transcode=32
            elif selected_report=='Cash Order Report':transcode=33
            elif selected_report=='Cash Trade Details Report':transcode=34
            elif selected_report=='Cash Limit Report':transcode=35
            elif selected_report=='Cash Net Position Report':transcode=36
            elif selected_report=='Derivative Order Report':transcode=41
            elif selected_report=='Turn Over report':transcode=42
            elif selected_report=='Derivative order Details Report':transcode=43
            elif selected_report=='Derivative Trade Details Report':transcode=44
            elif selected_report=='Commodity Limit Report':transcode=49
            elif selected_report=='Currency Limit Report':transcode=54

            header.Prop02TransactionCode=transcode
            orderReportReq=ReportRequest(1)
            orderReportReq.Prop01Header=[header.cMessageLength,header.cTransactionCode]
            orderReportReq.Prop02LoginID='karuppa'
            orderReportReq.Prop03CustomerID='139504'
            orderReportReq.Prop04DateTime=''
            orderReportReq.Prop05ScripCode=''
            orderReportReq.Prop06OrderId="243638563"    #   For Report put your sharekhanorder ID here  to see Order Report
            #like example cash order : 243638552      FNOOrder:  58459357
            orderReportReq.Prop07Reserved=''
            tapClient.SendOrderReportRequest(orderReportReq.StructToByte())
            requestSentQueue.Enqueue(orderReportReq.ToString())

class Status(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        init.init.fr_addlistbox(self)
        init.init.st_addLables(self)


class Alert(ttk.Frame):
    DicMarketDepthResponse={}
    DicFeedsRespone={}
    DicSharekhanOrderResponse={}
    dicReqIDTrack={}
    dicSharekhanIDvsAPIReqID={}
    dicTradeConfirm={}
    AutoInc=0
    ncScripMaster={}
    nfScripMaster={}
    rnScripMaster={}
    rmScripMaster={}
    bcScripMaster={}
    nxScripMaster={}
    mxScripMaster={}

    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        init.init.al_addButtons(self)
        init.init.al_addLables(self)
        init.init.al_adddropdown(self)
        init.init.al_addEntry(self)

    def btnScripMasterDownload_click(self):
        TapClient.SendScripMasterDownload(self)
        MainWindow.MainWindow.StartRead=True

    def LoadScripmaster(scripmaster,exchangeCode):
        try:
            if scripmaster is not None and exchangeCode==constants.NCExcode:
                FeedRequest.ncScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.NFExCode:
                FeedRequest.nfScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.RNExCode:
                FeedRequest.rnScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.RMExcode:
                FeedRequest.rmScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.BCExcode:
                FeedRequest.bcScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.NXExcode:
                FeedRequest.nxScripMaster.update(scripmaster)
            elif scripmaster is not None and exchangeCode==constants.MXExcode:
                FeedRequest.mxScripMaster.update(scripmaster)

        except:
            logger.exception(PrintException())

    def btnAlertOrder_Click(self):
        '''click to place order after providing price and quantity'''
        try:
            #self.se_option.current()!=-1 and
            if( self.sec_option.current()!=-1 and len(self.MinEntery.get())!=0 and len(self.HrEntry.get())!=0):
                header=MessageHeader(1)
                header.Prop01MessageLength=constants.OrderRequestSize
                header.Prop02TransactionCode=constants.TranCode.OrderRequest.value


                orderItem=OrderItem(True)
                orderItem.Prop01DataLength=constants.OrderItemSize
                orderItem.Prop02OrderID=''
                scripName=None

                selectedval=self.sec_var.get()
                selectedScrip=self.scrip_var.get()
                if selectedval=='NC':
                    print(FeedRequest.ncScripMaster.values()[3])

                if selectedval=='BC':
                    for v in FeedRequest.bcScripMaster.values():
                        if v[3].split(' ')[0]==selectedScrip:
                            alerter.alertit()
                if selectedval=='NF':
                    scripvariable=self.scrip_var.get()
                    expiryvaribale=self.expiry_var.get()
                    instvar=self.instrument_var.get()
                    strikevar=self.strike_var.get()
                    if strikevar.endswith('.0'):
                        strikevar=strikevar.replace('.0','')

                    scripName=scripvariable+expiryvaribale+instvar+strikevar
                    if instvar=='FUT':
                        scripName=scripvariable+expiryvaribale
                    for x in FeedRequest.nfScripMaster.values():
                        if x[3].replace(' ','')==scripName:
                            alerter.alertit()

                if selectedval=='RN':
                    scripvariable=self.scrip_var.get()
                    expiryvaribale=self.expiry_var.get()
                    instvar=self.instrument_var.get()
                    strikevar=self.strike_var.get()
                    if strikevar.endswith('.0'):
                        strikevar=strikevar.replace('.0','')
                    scripName=scripvariable+expiryvaribale+instvar+strikevar
                    for x in FeedRequest.rnScripMaster.values():
                        if x[3].replace(' ','')==scripName:
                            alerter.alertit()

                if selectedval=='MX':
                    for v in FeedRequest.mxScripMaster.values():
                        if v[3].split(' ')[0]==selectedScrip:
                            alerter.alertit()

                if selectedval=='RM':
                    for v in FeedRequest.rmScripMaster.values():
                        if v[3].split(' ')[0]==selectedScrip:
                            alerter.alertit()

                if selectedval=='NX':
                    for v in FeedRequest.nxScripMaster.values():
                        if v[3].split(' ')[0]==selectedScrip:
                            alerter.alertit()


            else:
                messagebox.showwarning('Please provide complete details...')
        except:
            logger.exception(PrintException())

    def SelectionChanged(self):
        '''select feed or depth to request'''
        if self.feedororder_option.current()!=-1:
            if self.feedororder_var.get()=='get feeds':
                optiontype=self.sec_var.get()
                if self.feedordepth_option.current()!=-1 and len(optiontype)!=0 and len(self.scrip_var.get())!=0 and len(self.se_var.get())!=0:
                    try:
                        scripName=None
                        if self.feedordepth_var.get()=='feed':
                            header=MessageHeader(1)
                            header.Prop01MessageLength=constants.FeedRequestSize
                            header.Prop02TransactionCode=constants.TranCode.FeedRequest
                            feedreq=FeedRequestF(1)
                            feedreq.Prop01Header=[header.cMessageLength,header.cTransactionCode]
                            feedreq.Prop02Count=1
                            selectedScrip=self.scrip_var.get()
                            if optiontype=='NC':
                                for v in FeedRequest.ncScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc

                            elif optiontype=='BC':
                                for v in FeedRequest.bcScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc

                            elif optiontype=='MX':
                                for v in FeedRequest.mxScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc
                            elif optiontype=='RM':
                                for v in FeedRequest.rmScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc

                            elif optiontype=='NX':
                                for v in FeedRequest.nxScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                feedreq.Prop03ScripList=optiontype+tempnc

                            elif optiontype=='NF':
                                if self.instrument_var.get()!='FUT':
                                    scripvariable=self.scrip_var.get()
                                    expiryvaribale=self.expiry_var.get()
                                    instvar=self.instrument_var.get()
                                    strikevar=self.strike_var.get()
                                    if strikevar.endswith('.0'):
                                        strikevar=strikevar.replace('.0','')

                                    scripName=scripvariable+expiryvaribale+instvar+strikevar
                                else:
                                    scripName=scripvariable+expiryvaribale
                                for x in FeedRequest.nfScripMaster.values():
                                    if x[3].replace(' ','')==scripName:
                                        feedreq.Prop03ScripList=optiontype+x[2]

                            elif optiontype=='RN':
                                scripvariable=self.scrip_var.get()
                                expiryvaribale=self.expiry_var.get()
                                instvar=self.instrument_var.get()
                                strikevar=self.strike_var.get()
                                if strikevar.endswith('.0'):
                                    strikevar=strikevar.replace('.0','')
                                scripName=scripvariable+expiryvaribale+instvar+strikevar
                                for x in FeedRequest.rnScripMaster.values():
                                    if x[3].replace(' ','')==scripName:
                                        feedreq.Prop03ScripList=optiontype+x[2]

                            feedreq.Prop04Reserved=''
                            requestSentQueue.Enqueue(feedreq.ToString())
                            tapClient.SubscribeforFeeds(feedreq.StructToByte())
                            init.init.lb_feeds.insert(END,selectedScrip)



                        elif self.feedordepth_var.get()=='depth':
                            header=MessageHeader(1)
                            header.Prop01MessageLength=constants.MarketDepthRequestSize
                            header.Prop02TransactionCode=constants.TranCode.DepthRequest

                            depthRequest=MarketDepthRequest(1)
                            depthRequest.Prop01Header=[header.cMessageLength,header.cTransactionCode]
                            selectedScrip=self.scrip_var.get()
                            if optiontype=='NC':
                                for v in FeedRequest.ncScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc

                            elif optiontype=='BC':
                                for v in FeedRequest.bcScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc

                            elif optiontype=='NF':
                                if self.instrument_var.get()!='FUT':
                                    scripvariable=self.scrip_var.get()
                                    expiryvaribale=self.expiry_var.get()
                                    instvar=self.instrument_var.get()
                                    strikevar=self.strike_var.get()
                                    if strikevar.endswith('.0'):
                                        strikevar=strikevar.replace('.0','')

                                    scripName=scripvariable+expiryvaribale+instvar+strikevar
                                else:
                                    scripName=scripvariable+expiryvaribale
                                for x in FeedRequest.nfScripMaster.values():
                                    if x[3].replace(' ','')==scripName:
                                        depthRequest.Prop03ScripCode=x[2]

                            elif optiontype=='RN':
                                scripvariable=self.scrip_var.get()
                                expiryvaribale=self.expiry_var.get()
                                instvar=self.instrument_var.get()
                                strikevar=self.strike_var.get()
                                if strikevar.endswith('.0'):
                                    strikevar=strikevar.replace('.0','')
                                scripName=scripvariable+expiryvaribale+instvar+strikevar
                                for x in FeedRequest.rnScripMaster.values():
                                    if x[3].replace(' ','')==scripName:
                                        depthRequest.Prop03ScripCode=x[2]

                            elif optiontype=='NX':
                                for v in FeedRequest.nxScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc

                            elif optiontype=='MX':
                                for v in FeedRequest.mxScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc

                            elif optiontype=='RM':
                                for v in FeedRequest.rmScripMaster.values():
                                    if v[3].split(' ')[0]==selectedScrip:tempnc=v[2]
                                depthRequest.Prop03ScripCode=tempnc
                            depthRequest.Prop04Reserved=''
                            depthRequest.Prop02ExchangeCode=optiontype
                            requestSentQueue.Enqueue(depthRequest.ToString())
                            tapClient.SubscribeforFeeds(depthRequest.StructToByte())
                            init.init.lb_depth.insert(END,selectedScrip)


                    except:
                        logger.exception(PrintException())


class ScrollViewer(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        init.init.txtaddLables(self)
        init.init.txtscrldText(self)

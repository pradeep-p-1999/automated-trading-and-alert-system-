from Exception import *
from tkinter import *
import tkinter as tk
import MainWindowGUI
from Constants import *
import MainWindow
import threading
from tkinter import ttk
from performance import *
from tkinter.scrolledtext import ScrolledText
from AutoCmb import *
from datetime import datetime

lblFont=('times',10,'bold')

class init():
    def addLables(self):
        try:
            lblLoginID = tk.Label(self,text='Login ID :',height=3,font=lblFont)

            labelMemberPswd = tk.Label(self,text="MemberShip Password :",height=3,font=lblFont)

            labelTradingPswd = tk.Label(self,text="Trading Password :",height=3,font=lblFont)

            labelIP = tk.Label(self,text="IP Address :",height=3,font=lblFont)

            lblLoginID.grid(row=0,sticky=E)
            labelMemberPswd.grid(row=1,sticky=E)
            labelTradingPswd.grid(row=2,sticky=E)
            labelIP.grid(row=3,sticky=E)
        except:
            logger.exception(PrintException())

    def addEntry(self):
        try:
            self.LoginIdEntry=ttk.Entry(self, textvariable=StringVar(),font=lblFont)
            self.LoginIdEntry.insert(END,'enter_login_id')

            self.MemberPswdEntry=ttk.Entry(self, textvariable=StringVar(),show='*',font=lblFont)
            self.MemberPswdEntry.insert(END,'MemberPassword')

            self.TradingpswdEntry=ttk.Entry(self, textvariable=StringVar(),show='*',font=lblFont)
            self.TradingpswdEntry.configure(font=lblFont,show='*')
            self.TradingpswdEntry.insert(END,'TradingPassword')

            self.IPAddEntry=ttk.Entry(self, textvariable=StringVar(),font=lblFont)
            self.IPAddEntry.insert(END,'192.168.85.114')



            self.LoginIdEntry.grid(column=1,row=0)
            self.MemberPswdEntry.grid(column=1,row=1)
            self.TradingpswdEntry.grid(column=1,row=2)
            self.IPAddEntry.grid(column=1,row=3)
        except:
            logger.exception(PrintException())

    def addButton(self):
        try:
            Loginbtn=ttk.Button(self,text="Login",command=self.login_btn_evnt)

            Cancelbtn=ttk.Button(self,text="Cancel")
            Loginbtn.grid(row=4)
            Cancelbtn.grid(row=4,column=1)
        except:
            logger.exception(PrintException())

    def login_btn_evnt(self,event):
        try:
            if (len(self.LoginIdEntry.get())!=0 and len(self.MemberPswdEntry.get())!=0 and len(self.TradingpswdEntry.get())!=0  and len(self.IPAddEntry.get())!=0):
                constants.LoginId=self.LoginIdEntry.get()
                constants.MemberPassword=self.MemberPswdEntry.get()
                constants.TradingPassword=self.TradingpswdEntry.get()
                constants.TapIp=self.IPAddEntry.get()
                constants.TapPort=8000
                TapClient.connect(self)
                TapClient.SendLoginRequest(self)

        except:
            logger.exception(PrintException())

    def fr_addLables(self):
        select_exchange = tk.Label(self,text='Select Exchange')
        select_exchange.configure(height=2,width=20,font=lblFont)

        select_exchange_code = tk.Label(self,text="Select Exchange Code")
        select_exchange_code.configure(height=2,width=20,font=lblFont)

        select_scrip = tk.Label(self,text="Select Scrip")
        select_scrip.configure(height=2,width=20,font=lblFont)

        self.select_exp=tk.Label(self,text="Select Expiry")
        self.select_exp.configure(height=2,width=20,font=lblFont)

        self.select_inst=tk.Label(self,text="Select instrument")
        self.select_inst.configure(height=2,width=20,font=lblFont)

        self.select_srike=tk.Label(self,text="Select StrikePrice")
        self.select_srike.configure(height=2,width=20,font=lblFont)

        select_feed_depth = tk.Label(self,text="Select Feed or Depth")
        select_feed_depth.configure(height=2,width=20,font=lblFont)

        select_feed_order = tk.Label(self,text="Select Feed or Order")
        select_feed_order.configure(height=2,width=20,font=lblFont)

        tv = ttk.Treeview(self)
        tv['columns'] = ('LTT', 'LTP', 'BidPrice','Bid_Qnt','OfferPrice','Offer_Qnt')
        tv.heading("#0", text='Symbol', anchor='center')
        tv.column("#0", anchor="center")
        tv.heading('LTT', text='LTT')
        tv.column('LTT', anchor='center', width=100)
        tv.heading('LTP', text='LTP')
        tv.column('LTP', anchor='center', width=100)
        tv.heading('BidPrice', text='BidPrice')
        tv.column('BidPrice', anchor='center', width=100)
        tv.heading('Bid_Qnt', text='Bid Qnt')
        tv.column('Bid_Qnt', anchor='center', width=100)
        tv.heading('OfferPrice', text='OfferPrice')
        tv.column('OfferPrice', anchor='center', width=100)
        tv.heading('Offer_Qnt', text='Offer Qnt')
        tv.column('Offer_Qnt', anchor='center', width=100)
        tv.grid(row=0,column=4,rowspan=15,sticky='nsew')
        init.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.Qty=tk.Label(self,text='Qty')
        self.Qty.configure(height=2,font=lblFont)
        self.Price=tk.Label(self,text='Price')
        self.Price.configure(height=2,font=lblFont)

        select_exchange.grid(row=0)
        select_exchange_code.grid(row=1,column=0)
        select_scrip.grid(row=2,column=0)
        select_feed_depth.grid(row=6,column=0)
        select_feed_order.grid(row=7,column=0)
        self.Qty.grid(row=8,column=0)
        self.Price.grid(row=8,column=2)

    def fr_addEntry(self):
        self.QtyEntry=ttk.Entry(self, textvariable=StringVar(),font=lblFont)
        self.PriceeEntery=ttk.Entry(self,textvariable=StringVar(),font=lblFont)


        self.QtyEntry.grid(column=1,row=8)
        self.PriceeEntery.grid(column=3,row=8)



    def fr_adddropdown(self):
        try:

            exchanges = ["NSE","BSE","MCX","NCDX"]
            self.se_var = tk.StringVar()
            for val, exchange in enumerate(exchanges):
                self.rdbtn=tk.Radiobutton(self,text=exchange,indicatoron = 0,width=10,padx =5,variable=self.se_var,
                command = lambda : change_dropdown(self.se_var.get()),value=val)
                self.rdbtn.grid(row=0,column=val)

            def change_dropdown(widget):
                self.sec_var = StringVar(self)
                sec_code={
                '0':['NC','NF','RN'],
                '1':['BC'],
                '2':['MX','RM'],
                '3':['NX']}

                self.sec_var.set('SelectExchange')

                self.sec_option=ttk.Combobox(self,textvariable=self.sec_var,height=5,width=30)
                self.sec_option['values']=(sec_code[widget])
                self.sec_option.grid(row=1,column=1)



                self.sec_var.trace('w',lambda *args:change_cmbScripType())

                self.expiry_var=StringVar()
                self.expiry_var.set('select expiry')
                self.cmbExpiry=ttk.Combobox(self,textvariable=self.expiry_var,height=10,width=30)

                self.instrument_var=StringVar()
                self.instrument_var.set('select instrument')
                self.cmbInstrument=ttk.Combobox(self,textvariable=self.instrument_var,height=10,width=30)

                self.strike_var=StringVar()
                self.strike_var.set('select strikePrice')
                self.cmbStrike=ttk.Combobox(self,textvariable=self.strike_var,height=10,width=30)

                self.scrip_var=StringVar()
                def change_cmbScripType(*args):
                    def getoption():
                        if len(self.scrip_var.get())!=0 and self.scrip_var.get().isupper()==True:
                            str=set()
                            findScrip=self.scrip_var.get()
                            for (k,v) in MainWindowGUI.FeedRequest.nfScripMaster.items():
                                if k.split(' ')[0]==findScrip:
                                    str.add(int(v[6][0])/100)

                            self.cmbStrike['values']=sorted(str)
                            expiry=set(x[4] for x in MainWindowGUI.FeedRequest.nfScripMaster.values())
                            tempExp=list(expiry)
                            tempExp.sort(key=lambda date: datetime.strptime(date, "%d-%b-%Y"))
                            self.cmbExpiry['values']=tempExp

                            instrument=set(x[5] for x in MainWindowGUI.FeedRequest.nfScripMaster.values())
                            self.cmbInstrument['values']=sorted(instrument)

                    init.selectedSegment=self.sec_var.get()
                    def matches(fieldValue, acListEntry):
                        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
                        return re.match(pattern, acListEntry)

                    if init.selectedSegment=='NF':
                        nfScripMaster=list(x.partition(' ') for x in MainWindowGUI.FeedRequest.nfScripMaster.keys())
                        nfscrip=set(x[0] for x in nfScripMaster)
                        self.scrip_var=StringVar()
                        combobox_autocomplete = Combobox_Autocomplete(self, sorted(nfscrip), highlightthickness=1, textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        combobox_autocomplete.focus()

                        self.select_exp.grid(row=3,column=0)
                        self.select_inst.grid(row=4,column=0)
                        self.select_srike.grid(row=5,column=0)
                        self.cmbExpiry.grid(row=3,column=1)
                        self.cmbInstrument.grid(row=4,column=1)
                        self.cmbStrike.grid(row=5,column=1)

                    elif init.selectedSegment=='NC':
                        nfScripMaster=list(x.partition(' ') for x in MainWindowGUI.FeedRequest.ncScripMaster.keys())
                        nfscrip=set(x[0] for x in nfScripMaster)
                        self.scrip_var=StringVar()
                        combobox_autocomplete = Combobox_Autocomplete(self, sorted(nfscrip), highlightthickness=1,textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        combobox_autocomplete.focus()

                        self.cmbInstrument.grid_remove()
                        self.select_exp.grid_remove()
                        self.select_inst.grid_remove()
                        self.select_srike.grid_remove()
                        self.cmbExpiry.grid_remove()
                        self.cmbStrike.grid_remove()

                    elif init.selectedSegment=='BC':
                        nfScripMaster=list(x.partition(' ') for x in MainWindowGUI.FeedRequest.bcScripMaster.keys())
                        nfscrip=set(x[0] for x in nfScripMaster)
                        combobox_autocomplete = Combobox_Autocomplete(self, nfscrip, highlightthickness=1,textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        combobox_autocomplete.focus()


                        self.select_exp.grid_remove()
                        self.select_inst.grid_remove()
                        self.select_srike.grid_remove()
                        self.cmbExpiry.grid_remove()
                        self.cmbInstrument.grid_remove()
                        self.cmbStrike.grid_remove()

                    elif init.selectedSegment=='RN':
                        self.scrip_var.set('SelectExchange')
                        nfScripMaster=list(x.partition(' ') for x in MainWindowGUI.FeedRequest.rnScripMaster.keys())
                        nfscrip=set(x[0] for x in nfScripMaster)
                        combobox_autocomplete = Combobox_Autocomplete(self, nfscrip, highlightthickness=1,textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        self.select_exp.grid(row=3,column=0)
                        self.select_inst.grid(row=4,column=0)
                        self.select_srike.grid(row=5,column=0)
                        self.cmbExpiry.grid(row=3,column=1)
                        self.cmbInstrument.grid(row=4,column=1)
                        self.cmbStrike.grid(row=5,column=1)

                    elif init.selectedSegment=='RM':
                        self.scrip_var.set('SelectExchange')
                        nfScripMaster=set(x for x in MainWindowGUI.FeedRequest.rmScripMaster.keys())
                        nfscrip=set(x for x in nfScripMaster)
                        combobox_autocomplete = Combobox_Autocomplete(self, nfscrip, highlightthickness=1,textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        combobox_autocomplete.focus()

                    if init.selectedSegment=='NC' or init.selectedSegment=='RN':
                        self.select_exp.grid_remove()
                        self.select_inst.grid_remove()
                        self.select_srike.grid_remove()
                        self.cmbExpiry.grid_remove()
                        self.cmbInstrument.grid_remove()
                        self.cmbStrike.grid_remove()

                    self.scrip_var.trace('w',lambda *args:getoption())


            self.feedordepth_var = StringVar(self)
            self.fd=('feed','depth')
            self.feedordepth_var.set('Select feed or depth')
            self.feedordepth_option=ttk.Combobox(self,textvariable=self.feedordepth_var,height=5,width=30)
            self.feedordepth_option['values']=self.fd
            self.feedordepth_option.grid(row=6,column=1)

            self.feedororder_var = StringVar(self)
            self.fo=('get feeds','place order')
            self.feedororder_var.set('Select feed or order')
            self.feedororder_option=ttk.Combobox(self,textvariable=self.feedororder_var,height=5,width=30)
            self.feedororder_option['values']=self.fo
            self.feedororder_option.grid(row=7,column=1)

        except:
            logger.exception(PrintException())

    def fr_addButtons(self):
        try:
            ScripMaster=ttk.Button(self,text="ScripMaster",command=self.btnScripMasterDownload_click)

            LogOff=ttk.Button(self,text="LogOff")
            Place=ttk.Button(self,text='Place',command=self.btnPlaceOrder_Click)

            Feeds=ttk.Button(self,text='GetFeed',command=self.SelectionChanged)
            ScripMaster.grid(row=1,column=3)
            LogOff.grid(row=2,column=3)
            Place.grid(row=9,column=1)
            Feeds.grid(row=7,column=3)
        except:
            logger.exception(PrintException())

    def fr_addlistbox(self):
        init.lb_feeds=Listbox(self,width=50)
        init.lb_feeds.grid(row=1,padx=10,sticky=N+S+E+W)

        init.lb_depth=Listbox(self,width=50)
        init.lb_depth.grid(row=1,column=1,padx=10,sticky=N+S+E+W)

        init.lb_orders=Listbox(self,width=50)
        init.lb_orders.grid(row=1,column=2,padx=10,sticky=N+S+E+W)


    def al_addButtons(self):
        try:
            ScripMaster=ttk.Button(self,text="ScripMaster",command=self.btnScripMasterDownload_click)

            LogOff=ttk.Button(self,text="LogOff")
            Place=ttk.Button(self,text='Set Alert',command=self.btnAlertOrder_Click)


            ScripMaster.grid(row=1,column=3)
            LogOff.grid(row=2,column=3)
            Place.grid(row=9,column=1)

        except:
            logger.exception(PrintException())

    def al_addLables(self):
        select_exchange = tk.Label(self,text='Select Exchange')
        select_exchange.configure(height=2,width=20,font=lblFont)

        select_exchange_code = tk.Label(self,text="Select Exchange Code")
        select_exchange_code.configure(height=2,width=20,font=lblFont)

        select_scrip = tk.Label(self,text="Select Scrip")
        select_scrip.configure(height=2,width=20,font=lblFont)

        self.select_exp=tk.Label(self,text="Select Expiry")
        self.select_exp.configure(height=2,width=20,font=lblFont)

        self.select_inst=tk.Label(self,text="Select instrument")
        self.select_inst.configure(height=2,width=20,font=lblFont)

        self.select_srike=tk.Label(self,text="Select StrikePrice")
        self.select_srike.configure(height=2,width=20,font=lblFont)



        tv = ttk.Treeview(self)

        tv.grid(row=0,column=4,rowspan=15,sticky='nsew')
        init.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.Qty=tk.Label(self,text='hour')
        self.Qty.configure(height=2,font=lblFont)
        self.Price=tk.Label(self,text='minute')
        self.Price.configure(height=2,font=lblFont)

        select_exchange.grid(row=0)
        select_exchange_code.grid(row=1,column=0)
        select_scrip.grid(row=2,column=0)

        self.Qty.grid(row=8,column=0)
        self.Price.grid(row=8,column=2)

    def al_addEntry(self):
        self.HrEntry = ttk.Entry(self, textvariable=StringVar(), font=lblFont)
        self.MinEntery = ttk.Entry(self, textvariable=StringVar(), font=lblFont)


        self.HrEntry.grid(column=1, row=8)
        self.MinEntery.grid(column=3, row=8)

    def al_adddropdown(self):
        try:

            exchanges = ["NSE","BSE","MCX","NCDX"]
            self.se_var = tk.StringVar()
            for val, exchange in enumerate(exchanges):
                self.rdbtn=tk.Radiobutton(self,text=exchange,indicatoron = 0,width=10,padx =5,variable=self.se_var,
                command = lambda : change_dropdown(self.se_var.get()),value=val)
                self.rdbtn.grid(row=0,column=val)

            def change_dropdown(widget):
                self.sec_var = StringVar(self)
                sec_code={
                '0':['NC','NF','RN'],
                '1':['BC'],
                '2':['MX','RM'],
                '3':['NX']}

                self.sec_var.set('SelectExchange')

                self.sec_option=ttk.Combobox(self,textvariable=self.sec_var,height=5,width=30)
                self.sec_option['values']=(sec_code[widget])
                self.sec_option.grid(row=1,column=1)



                self.sec_var.trace('w',lambda *args:change_cmbScripType())

                self.expiry_var=StringVar()
                self.expiry_var.set('select expiry')
                self.cmbExpiry=ttk.Combobox(self,textvariable=self.expiry_var,height=10,width=30)

                self.instrument_var=StringVar()
                self.instrument_var.set('select instrument')
                self.cmbInstrument=ttk.Combobox(self,textvariable=self.instrument_var,height=10,width=30)

                self.strike_var=StringVar()
                self.strike_var.set('select strikePrice')
                self.cmbStrike=ttk.Combobox(self,textvariable=self.strike_var,height=10,width=30)

                self.scrip_var=StringVar()
                def change_cmbScripType(*args):
                    def getoption():
                        if len(self.scrip_var.get())!=0 and self.scrip_var.get().isupper()==True:
                            str=set()
                            findScrip=self.scrip_var.get()
                            for (k,v) in MainWindowGUI.FeedRequest.nfScripMaster.items():
                                if k.split(' ')[0]==findScrip:
                                    str.add(int(v[6][0])/100)

                            self.cmbStrike['values']=sorted(str)
                            expiry=set(x[4] for x in MainWindowGUI.FeedRequest.nfScripMaster.values())
                            tempExp=list(expiry)
                            tempExp.sort(key=lambda date: datetime.strptime(date, "%d-%b-%Y"))
                            self.cmbExpiry['values']=tempExp

                            instrument=set(x[5] for x in MainWindowGUI.FeedRequest.nfScripMaster.values())
                            self.cmbInstrument['values']=sorted(instrument)

                    init.selectedSegment=self.sec_var.get()
                    def matches(fieldValue, acListEntry):
                        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
                        return re.match(pattern, acListEntry)

                    if init.selectedSegment=='NF':
                        nfScripMaster=list(x.partition(' ') for x in MainWindowGUI.FeedRequest.nfScripMaster.keys())
                        nfscrip=set(x[0] for x in nfScripMaster)
                        self.scrip_var=StringVar()
                        combobox_autocomplete = Combobox_Autocomplete(self, sorted(nfscrip), highlightthickness=1, textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        combobox_autocomplete.focus()

                        self.select_exp.grid(row=3,column=0)
                        self.select_inst.grid(row=4,column=0)
                        self.select_srike.grid(row=5,column=0)
                        self.cmbExpiry.grid(row=3,column=1)
                        self.cmbInstrument.grid(row=4,column=1)
                        self.cmbStrike.grid(row=5,column=1)

                    elif init.selectedSegment=='NC':
                        nfScripMaster=list(x.partition(' ') for x in MainWindowGUI.FeedRequest.ncScripMaster.keys())
                        nfscrip=set(x[0] for x in nfScripMaster)
                        self.scrip_var=StringVar()
                        combobox_autocomplete = Combobox_Autocomplete(self, sorted(nfscrip), highlightthickness=1,textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        combobox_autocomplete.focus()

                        self.cmbInstrument.grid_remove()
                        self.select_exp.grid_remove()
                        self.select_inst.grid_remove()
                        self.select_srike.grid_remove()
                        self.cmbExpiry.grid_remove()
                        self.cmbStrike.grid_remove()

                    elif init.selectedSegment=='BC':
                        nfScripMaster=list(x.partition(' ') for x in MainWindowGUI.FeedRequest.bcScripMaster.keys())
                        nfscrip=set(x[0] for x in nfScripMaster)
                        combobox_autocomplete = Combobox_Autocomplete(self, nfscrip, highlightthickness=1,textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        combobox_autocomplete.focus()


                        self.select_exp.grid_remove()
                        self.select_inst.grid_remove()
                        self.select_srike.grid_remove()
                        self.cmbExpiry.grid_remove()
                        self.cmbInstrument.grid_remove()
                        self.cmbStrike.grid_remove()

                    elif init.selectedSegment=='RN':
                        self.scrip_var.set('SelectExchange')
                        nfScripMaster=list(x.partition(' ') for x in MainWindowGUI.FeedRequest.rnScripMaster.keys())
                        nfscrip=set(x[0] for x in nfScripMaster)
                        combobox_autocomplete = Combobox_Autocomplete(self, nfscrip, highlightthickness=1,textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        self.select_exp.grid(row=3,column=0)
                        self.select_inst.grid(row=4,column=0)
                        self.select_srike.grid(row=5,column=0)
                        self.cmbExpiry.grid(row=3,column=1)
                        self.cmbInstrument.grid(row=4,column=1)
                        self.cmbStrike.grid(row=5,column=1)

                    elif init.selectedSegment=='RM':
                        self.scrip_var.set('SelectExchange')
                        nfScripMaster=set(x for x in MainWindowGUI.FeedRequest.rmScripMaster.keys())
                        nfscrip=set(x for x in nfScripMaster)
                        combobox_autocomplete = Combobox_Autocomplete(self, nfscrip, highlightthickness=1,textvariable=self.scrip_var)
                        combobox_autocomplete.grid(row=2,column=1)
                        combobox_autocomplete.focus()

                    if init.selectedSegment=='NC' or init.selectedSegment=='RN':
                        self.select_exp.grid_remove()
                        self.select_inst.grid_remove()
                        self.select_srike.grid_remove()
                        self.cmbExpiry.grid_remove()
                        self.cmbInstrument.grid_remove()
                        self.cmbStrike.grid_remove()

                    self.scrip_var.trace('w',lambda *args:getoption())


        except:
            logger.exception(PrintException())



    def or_adddropdown(self):
        self.cmbordereport_var = StringVar(self)
        cmbordereport_choices = ('Equity Order Report','DPRS Report','Cash Order Report','Cash Trade Details Report',
                                'Cash Limit Report','Cash Net Position Report',
                                'Derivative Order Report','Turn Over report','Derivative order Details Report',
                                'Derivative Trade Details Report','Commodity Limit Report','Currency Limit Report')
        self.cmbordereport_var.set('Select Report Type')
        self.cmbordereport_option=ttk.Combobox(self,textvariable=self.cmbordereport_var,height=5,width=30,font=('times',10,'bold'))
        self.cmbordereport_option['values']=(cmbordereport_choices)
        self.cmbordereport_option.grid(row = 1, column =0)

    def or_addLables(self):
        lblFont=('times',13,'bold')
        select_report = tk.Label(self,text='Request for Order Report')
        select_report.configure(height=3,width=50,font=lblFont)
        select_report.grid(row=0,column=0,sticky='n')

    def or_addButtons(self):
        try:
            Feeds=ttk.Button(self,text='GetReport',command=self.getreport)
            Feeds.grid(row=2,columnspan = 2,padx=10,pady=30)
        except:
            logger.exception(PrintException())

    def txtaddLables(self):
        rqSend= tk.Label(self,text='Request Send')
        rqSend.configure(height=3,width=50,font=lblFont)
        rqSend.grid(row=0,column=0)

        rqRecv= tk.Label(self,text='Request Receive')
        rqRecv.configure(height=3,width=50,font=lblFont)
        rqRecv.grid(row=0,column=1)

    def txtscrldText(self):
        init.rqSendText=ScrolledText(self)
        init.rqSendText.grid(row=1,column=0,sticky='nsew')

        init.rqRecvText=ScrolledText(self)
        init.rqRecvText.grid(row=1,column=1,sticky='nsew')

    def feeds_addLables(self,ScripName):
        lblLoginID = tk.Label(self,text=ScripName,height=3,font=lblFont)
        lblLoginID.grid(row=0)

    def st_addLables(self):
        lbl_feeds=tk.Label(self,text="Feeds")
        lbl_feeds.configure(height=2,font=lblFont)

        lbl_depth=tk.Label(self,text="Depth")
        lbl_depth.configure(height=2,font=lblFont)

        lbl_orders=tk.Label(self,text="Orders")
        lbl_orders.configure(height=2,font=lblFont)


        lbl_feeds.grid(row=0,column=0,sticky=N+S+E+W)
        lbl_depth.grid(row=0,column=1,sticky=N+S+E+W)
        lbl_orders.grid(row=0,column=2,sticky=N+S+E+W)

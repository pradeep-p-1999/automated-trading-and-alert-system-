# import TapClient
import struct
import struct
from array import *
from Exception import *
from logging_config import *
class MessageHeader():
    def __init__(self,transcode):
        try:
            self._TransactionCode,self._MessageLength=0,0
        except:
            logger.exception(PrintException())

    @property
    def cMessageLength(self):return self._MessageLength
    @cMessageLength.setter
    def Prop01MessageLength(self,value):self._MessageLength=value

    @property
    def cTransactionCode(self):return self._TransactionCode
    @cTransactionCode.setter
    def Prop02TransactionCode(self,value):self._TransactionCode=value

    def ByteToStruct(self,val):
        try:
            self.Prop01MessageLength=struct.unpack('I',val[0:4])
            self.Prop02TransactionCode=struct.unpack('H',val[4:6])
        except:
            logger.exception(PrintException())

    def ToString(cHeader=None):
        try:
            if cHeader==None:
                return 'MessageLength ='+str(self.cMessageLength) +'|'+'transactionCode='+str(self.cTransactionCode)
            else:
                if cHeader[0]<256:
                    bytarr=array('B')
                    for x in cHeader:
                        bytarr.append(x)
                    return 'MessageLength ='+str(struct.unpack('I',bytarr[0:4])[0]) +'|'+'transactionCode='+str(struct.unpack('H',bytarr[4:6])[0])
                else:
                    return 'MessageLength ='+str(cHeader[0])[0] +'|'+'transactionCode='+str(cHeader[1])[0]
        except:
            logger.exception(PrintException())

class SignOn():
    def __init__(self):
        self._Header=0
        self._LoginId=0
        self._MemberPassword=0
        self._TradingPassword=0
        self._IP=0
        self._Reserved=0

    @property
    def cHeader(self):
        return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cLoginId(self):return self._LoginId
    @cLoginId.setter
    def Prop02LoginId(self,value):self._LoginId=value+'\0'*(30-len(value))

    @property
    def cMemberPassword(self):return self._MemberPassword
    @cMemberPassword.setter
    def Prop03MemberPassword(self,value):self._MemberPassword=value+'\0'*(20-len(value))

    @property
    def cTradingPassword(self):return self._TradingPassword
    @cTradingPassword.setter
    def Prop04TradingPassword(self,value):self._TradingPassword=value+'\0'*(20-len(value))

    @property
    def cIP(self):return self._IP
    @cIP.setter
    def Prop05IP(self,value):self._IP=value+'\0'*(20-len(value))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop06Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def StructToByte(self):
        loginreq=array('B')
        for c in self.cHeader:loginreq.append(c)
        for c in self.cLoginId:loginreq.append(ord(c))
        for c in self.cMemberPassword:loginreq.append(ord(c))
        for c in self.cTradingPassword:loginreq.append(ord(c))
        for c in self.cIP:loginreq.append(ord(c))
        for c in self.cReserved:loginreq.append(ord(c))
        return loginreq

    def ToString(self):
        return '{}{}{}{}{}{}{}{}{}{}{}{}{}{}'.format('\n',MessageHeader.ToString(self.cHeader),'|','LoginId=',self.cLoginId.strip('\x00'),'|','MemberPassword=',self.cMemberPassword.strip('\x00'),'|',"TradingPassword = ",self.cTradingPassword.strip('\x00'),"|","IP = ",self.cIP.strip('\x00'))

class LoginResponse():
    def __init__(self,tranCode):
        self._cHeader=MessageHeader(tranCode)
        self._StatusCode,self._Message,self._ClientInfoList,self._Reserved=1,None,None,None

    @property
    def cHeader(self):return self._cHeader
    @cHeader.setter
    def Prop01Header(self,value):self._cHeader=value

    @property
    def cStatusCode(self):return self._StatusCode
    @cStatusCode.setter
    def Prop02StatusCode(self,value):self._StatusCode=value

    @property
    def cMessage(self):return self._Message
    @cMessage.setter
    def Prop03Message(self,value):self._Message=value

    @property
    def cClientInfoList(self):return self._ClientInfoList
    @cClientInfoList.setter
    def Prop04ClientInfoList(self,value):self._ClientInfoList=value

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop05Reserved(self,value):self._Reserved=value

    def ByteToStruct(self,val):
        try:
            cHeader=MessageHeader(1)
            cHeader.ByteToStruct(val[0:6])
            self.Prop01Header=[cHeader.cMessageLength[0],cHeader.Prop02TransactionCode[0]]
            self.Prop02StatusCode=struct.unpack('h',val[6:8])[0]
            self.Prop03Message=struct.pack("b"*len(val[8:255]),*val[8:255]).decode('utf8').strip('\x00')
            self.Prop04ClientInfoList=struct.pack("b"*len(val[258:333]),*val[258:333]).decode('utf8').strip('\x00')
        except:
            logger.exception(PrintException())

    def ToString(self):
        try:
            return "{}{}{}{}{}{}{}{}{}{}".format(MessageHeader.ToString(self.cHeader),"|","StatusCode = ",self.cStatusCode, "|","Message = ",self.cMessage.strip('\x00'),"|","ClientInfoList = ",self.cClientInfoList.strip('\x00'))
        except:
            logger.exception(PrintException())

class ScripMasterRequest():
    def __init__(self,tranCode):
        self._Header=MessageHeader(tranCode)
        self._ExchangeCode=None
        self._Reserved=None

    @property
    def cHeader(self):return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,value):self._ExchangeCode=value+'\0'*(2-len(value))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop03Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def ByteToStruct(ByteToStruct):
        cHeader=MessageHeader(1)
        cHeader.ByteToStruct()

    def StructToByte(self):
        try:
            scripreq=array('B')
            for c in self.cHeader:scripreq.append(c)
            for c in self.cExchangeCode:scripreq.append(ord(c))
            for c in self.cReserved:scripreq.append(ord(c))
            return scripreq
        except:
            logger.exception(PrintException())

    def ToString(self):
        return ('\n'+MessageHeader.ToString(self.cHeader) + "|" + "ExchangeCode = " + self.cExchangeCode.strip('\x00') + "|" + "Reserved = " +self.cReserved.strip('\x00'));

class ScripMasterResponse():
    def __init__(self,tranCode):
        self._Header=MessageHeader(tranCode)
        self._ExchangeCode=None
        self._Reserved=None

    @property
    def cHeader(self):return self._Header
    @cHeader.setter
    def Prop01Header(self,value):self._Header=value

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,value):self._ExchangeCode=value

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop03Reserved(self,value):self._Reserved=value

    def ByteToStruct(self,val):
        try:
            cHeader=MessageHeader(1)
            cHeader.ByteToStruct(val[0:6])
            self.Prop01Header=[cHeader.cMessageLength[0],cHeader.Prop02TransactionCode[0]]
            self.Prop02ExchangeCode=struct.pack("b"*len(val[6:8]),*val[6:8]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        return "{}{}{}{}{}".format('\n',MessageHeader.ToString(self.cHeader),"|","ExchangeCode = ",self.cExchangeCode.strip('\x00'))

class NFScripMaster():
    def __init__(self,tranCode):
        self._DataLength=0
        self._DerivativeType=0
        self._ScripCode=0
        self._ScripShortName=0
        self._ExpiryDate=0
        self._FutOption=0
        self._StrikePrice=0
        self._LotSize=0
        self._Reserved=0

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cDerivativeType(self):return self._DerivativeType
    @cDerivativeType.setter
    def Prop02DerivativeType(self,val):self._DerivativeType=val

    @property
    def cScripCode(self):return self._ScripCode
    @cScripCode.setter
    def Prop03ScripCode(self,val):self._ScripCode=val

    @property
    def cScripShortName(self):return self._ScripShortName
    @cScripShortName.setter
    def Prop04ScripShortName(self,val):self._ScripShortName=val

    @property
    def cExpiryDate(self):return self._ExpiryDate
    @cExpiryDate.setter
    def Prop05ExpiryDate(self,val):self._ExpiryDate=val

    @property
    def cFutOption(self):return self._FutOption
    @cFutOption.setter
    def Prop06FutOption(self,val):self._FutOption=val

    @property
    def cStrikePrice(self):return self._StrikePrice
    @cStrikePrice.setter
    def Prop07StrikePrice(self,val):self._StrikePrice=val

    @property
    def cLotSize(self):return self._LotSize
    @cLotSize.setter
    def Prop08LotSize(self,val):self._LotSize=val

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop09Reserved(self,val):self._Reserved=val

    def ByteToStruct(self,val):
        try:
            self.Prop01DataLength=struct.unpack('I',val[0:4])
            self.Prop02DerivativeType=struct.pack("B"*len(val[4:14]),*val[4:14]).decode('utf8')
            self.Prop03ScripCode=struct.pack("B"*len(val[14:24]),*val[14:24]).decode('utf8')
            self.Prop04ScripShortName=struct.pack("B"*len(val[24:84]),*val[24:84]).decode('utf8')
            self.Prop05ExpiryDate=struct.pack("B"*len(val[84:99]),*val[84:99]).decode('utf8')
            self.Prop06FutOption=struct.pack("B"*len(val[99:109]),*val[99:109]).decode('utf8')
            self.Prop07StrikePrice=struct.unpack('I',val[109:113])
            self.Prop08LotSize=struct.unpack('I',val[113:117])
            self.Prop09Reserved=struct.pack("B"*len(val[117:217]),*val[117:217]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        return "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format('\n'+"DisplayLotSize = ",self.cDataLength[0:],"|","DerivativeType = ",self.cDerivativeType.strip('\x00'),"|" , "ScripCode = ",self.cScripCode.strip('\x00') + "|","ScripShortName = ", self.cScripShortName.strip('\x00') ,"|" , "ExpiryDate = " , self.cExpiryDate.strip('\x00') , "|" , "FutOption = " , self.cFutOption.strip('\x00') , "|" , "StrikePrice = " , slef.cStrikePrice.strip('\x00'), "|", "LotSize = ",self.cLotSize, "|" ,"Reserved = " ,self.cReserved.strip('\x00'))

class NCScripMaster():
    def __init__(self,tranCode):
        self._DataLength=0
        self._Segment=0
        self._ScripCode=0
        self._ScripShortName=0
        self._Reserved=0

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def CSegment(self):return self._Segment
    @CSegment.setter
    def Prop02Segment(self,val):self._Segment=val

    @property
    def cScripCode(self):return self._ScripCode
    @cScripCode.setter
    def Prop03ScripCode(self,val):self._ScripCode=val

    @property
    def cScripShortName(self):return self._ScripShortName
    @cScripShortName.setter
    def Prop04ScripShortName(self,val):self._ScripShortName=val

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop05Reserved(self,val):self._Reserved=val

    def ByteToStruct(self,val):
        try:
            self.Prop01DataLength=struct.unpack('I',val[0:4])
            self.Prop02Segment=struct.pack("B"*len(val[4:14]),*val[4:14]).decode('utf8')
            self.Prop03ScripCode=struct.pack("B"*len(val[14:24]),*val[14:24]).decode('utf8')
            self.Prop04ScripShortName=struct.pack("B"*len(val[24:84]),*val[24:84]).decode('utf8')
            self.Prop05Reserved=struct.pack("B"*len(val[84:184]),*val[84:184]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}".format("DataLength = ",self.cDataLength[0:],"|","Segment = ",self.cDerivativeType,"|" , "ScripCode = ",self.cScripCode + "|","ScripShortName = ", self.cScripShortName , "|" ,"Reserved = " ,self.cReserved)

class RNScripMaster():
    def __init__(self,tranCode):
        self._DataLength=0
        self._CurrencyType=0
        self._ScripCode=0
        self._ScripShortName=0
        self._ExpiryDate=0
        self._FutOption=0
        self._StrikePrice=0
        self._LotSize=0
        self._DisplayLotSize=0
        self._LotType=0
        self._DisplayLotType=0
        self._OFType=0
        self._MinimumTradeQty=0
        self._PriceTick=0
        self._Multipler=0
        self._Reserved=0

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cCurrencyType(self):return self._DerivativeType
    @cCurrencyType.setter
    def Prop02CurrencyType(self,val):self._DerivativeType=val

    @property
    def cScripCode(self):return self._ScripCode
    @cScripCode.setter
    def Prop03ScripCode(self,val):self._ScripCode=val

    @property
    def cScripShortName(self):return self._ScripShortName
    @cScripShortName.setter
    def Prop04ScripShortName(self,val):self._ScripShortName=val

    @property
    def cExpiryDate(self):return self._ExpiryDate
    @cExpiryDate.setter
    def Prop05ExpiryDate(self,val):self._ExpiryDate=val

    @property
    def cFutOption(self):return self._FutOption
    @cFutOption.setter
    def Prop06FutOption(self,val):self._FutOption=val

    @property
    def cStrikePrice(self):return self._StrikePrice
    @cStrikePrice.setter
    def Prop07StrikePrice(self,val):self._StrikePrice=val

    @property
    def cLotSize(self):return self._LotSize
    @cLotSize.setter
    def Prop08LotSize(self,val):self._LotSize=val

    @property
    def cDisplayLotSize(self):return self._DisplayLotSize
    @cDisplayLotSize.setter
    def Prop09DisplayLotSize(self,val):self._DisplayLotSize=val

    @property
    def cLotType(self):return self._LotType
    @cLotType.setter
    def Prop10LotType(self,val):self._LotType=val

    @property
    def cDisplayLotType(self):return self._DisplayLotType
    @cDisplayLotType.setter
    def Prop11DisplayLotType(self,val):self._DisplayLotType=val

    @property
    def cOFType(self):return self._OFType
    @cOFType.setter
    def Prop12OFType(self,val):self._OFType=val

    @property
    def cMinimumTradeQty(self):return self._MinimumTradeQty
    @cMinimumTradeQty.setter
    def Prop13MinimumTradeQty(self,val):self._MinimumTradeQty=val

    @property
    def cPriceTick(self):return self._PriceTick
    @cPriceTick.setter
    def Prop14PriceTick(self,val):self._PriceTick=val

    @property
    def cMultipler(self):return self._Multipler
    @cMultipler.setter
    def Prop15Multipler(self,val):self._Multipler=val

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop16Reserved(self,val):self._Reserved=val

    def ByteToStruct(self,val):
        try:
            self.Prop01DataLength=struct.unpack('I',val[0:4])
            self.Prop02CurrencyType=struct.pack("B"*len(val[4:14]),*val[4:14]).decode('utf8')
            self.Prop03ScripCode=struct.pack("B"*len(val[14:24]),*val[14:24]).decode('utf8')
            self.Prop04ScripShortName=struct.pack("B"*len(val[24:84]),*val[24:84]).decode('utf8')
            self.Prop05ExpiryDate=struct.pack("B"*len(val[84:99]),*val[84:99]).decode('utf8')
            self.Prop06FutOption=struct.pack("B"*len(val[99:109]),*val[99:109]).decode('utf8')
            self.Prop07StrikePrice=struct.unpack('I',val[109:113])
            self.Prop08LotSize=struct.unpack('I',val[113:117])
            self.Prop09DisplayLotSize=struct.unpack('I',val[117:121])
            self.Prop10LotType=struct.pack("B"*len(val[121:146]),*val[121:146]).decode('utf8')
            self.Prop11DisplayLotType=struct.pack("B"*len(val[146:181]),*val[146:181]).decode('utf8')
            self.Prop12OFType=struct.pack("B"*len(val[181:196]),*val[181:196]).decode('utf8')
            self.Prop13MinimumTradeQty=struct.unpack('I',val[196:200])
            self.Prop14PriceTick=struct.pack("B"*len(val[200:225]),*val[200:225]).decode('utf8')
            self.Prop15Multipler=struct.unpack('I',val[225:229])
            self.Prop16Reserved=struct.pack("B"*len(val[229:329]),*val[229:329]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}{17}{18}{19}{20}{21}{22}{23}{24}{25}{26}{27}{28}{29}{30}{31}{32}{33}{34}{35}{36}{37}{38}{39}{40}{41}{42}{43}{44}{45}{46}{47}".format(
                "DisplayLotSize = ",self.cDataLength[0:],"|","DerivativeType = ",self.cCurrencyType,"|" , "ScripCode = ",self.cScripCode + "|","ScripShortName = ", self.cScripShortName ,"|" , "ExpiryDate = " , self.cExpiryDate , "|" , "FutOption = " ,
                self.cFutOption , "|" , "StrikePrice = " , slef.cStrikePrice, "|", "LotSize = ",self.cLotSize, "|" ,"DisplayLotSize = ",self.cDisplayLotSize, "|" ,"LotType = ",self.cLotType, "|" ,"DisplayLotType = ",self.cDisplayLotType, "|" ,
                "OFType = ",self.cOFType, "|" ,"MinimumTradeQty = ",self.cMinimumTradeQty, "|" ,"PriceTick = ",self.cPriceTick, "|" ,"Multipler = ",self.cMultipler, "|" ,"Reserved = " ,self.cReserved)

class OrderItem():
    def __init__(self,transcode):
        self._DataLength = 0
        self._OrderID = 0
        self._CustomerID =0
        self._S2KID = 0
        self._ScripToken = set()
        self._BuySell =0
        self._OrderQty = 0
        self._OrderPrice = 0
        self._TriggerPrice = 0
        self._DisclosedQty = 0
        self._ExecutedQty = 0
        self._RMSCode = 0
        self._ExecutedPrice = 0
        self._AfterHour = 0
        self._GTDFlag = 0
        self._GTD =0
        self._Reserved = 0

    @property
    def cDataLength(self):
        return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):
        self._DataLength=val

    @property
    def cOrderID(self):
        return self._OrderID
    @cOrderID.setter
    def Prop02OrderID(self,val):
        self._OrderID=val+'\0'*(20-len(val))

    @property
    def cCustomerID(self):
        return self._CustomerID
    @cCustomerID.setter
    def Prop03CustomerID(self,val):
        self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cS2KID(self):
        return self._S2KID
    @cS2KID.setter
    def Prop04S2KID(self,val):
        self._S2KID=val+'\0'*(10-len(val))

    @property
    def cScripToken(self):
        return self._ScripToken
    @cScripToken.setter
    def Prop05ScripToken(self,val):
        self._ScripToken=val+'\0'*(10-len(val))

    @property
    def cBuySell(self):
        return self._BuySell
    @cBuySell.setter
    def Prop06BuySell(self,val):
        self._BuySell=val+'\0'*(3-len(val))

    @property
    def cOrderQty(self):
        return self._OrderQty
    @cOrderQty.setter
    def Prop07OrderQty(self,val):
        self._OrderQty=val

    @property
    def cOrderPrice(self):
        return self._OrderPrice
    @cOrderPrice.setter
    def Prop08OrderPrice(self,val):
        self._OrderPrice=val

    @property
    def cTriggerPrice(self):
        return self._TriggerPrice
    @cTriggerPrice.setter
    def Prop09TriggerPrice(self,val):
        self._TriggerPrice=val

    @property
    def cDisclosedQty(self):
        return self._DisclosedQty
    @cDisclosedQty.setter
    def Prop10DisclosedQty(self,val):
        self._DisclosedQty=val

    @property
    def cExecutedQty(self):
        return self._ExecutedQty
    @cExecutedQty.setter
    def Prop11ExecutedQty(self,val):
        self._ExecutedQty=val

    @property
    def cRMSCode(self):
        return self._RMSCode
    @cRMSCode.setter
    def Prop12RMSCode(self,val):
        self._RMSCode=val+'\0'*(15-len(val))

    @property
    def cExecutedPrice(self):
        return self._ExecutedPrice
    @cExecutedPrice.setter
    def Prop13ExecutedPrice(self,val):
        self._ExecutedPrice=val

    @property
    def cAfterHour(self):
        return self._AfterHour
    @cAfterHour.setter
    def Prop14AfterHour(self,val):
        self._AfterHour=val+'\0'*(1-len(val))

    @property
    def cGTDFlag(self):
        return self._GTDFlag
    @cGTDFlag.setter
    def Prop15GTDFlag(self,val):
        self._GTDFlag=val+'\0'*(5-len(val))

    @property
    def cGTD(self):
        return self._GTD
    @cGTD.setter
    def Prop16GTD(self,val):
        self._GTD=val+'\0'*(25-len(val))

    @property
    def cReserved(self):
        return self._Reserved
    @cReserved.setter
    def Prop17Reserved(self,val):
        self._Reserved=val+'\0'*(100-len(val))

    def StructToByte(self):
        try:
            orderData=array('B')

            DataLength=struct.pack('I',self.cDataLength)
            DataLength1=struct.unpack('B'*4,DataLength)
            for c in DataLength1:orderData.append(c)

            for c in self.cOrderID:orderData.append(ord(c))
            for c in self.cCustomerID:orderData.append(ord(c))
            for c in self.cS2KID:orderData.append(ord(c))
            for c in self.cScripToken:orderData.append(ord(c))
            for c in self.cBuySell:orderData.append(ord(c))

            OrderQty=struct.pack('I',self.cOrderQty)
            OrderQty1=struct.unpack('B'*4,OrderQty)
            for c in OrderQty1:orderData.append(c)

            OrderPrice=struct.pack('I',self.cOrderPrice)
            OrderPrice1=struct.unpack('B'*4,OrderPrice)
            for c in OrderPrice1:orderData.append(c)

            TriggerPrice=struct.pack('I',self.cTriggerPrice)
            TriggerPrice1=struct.unpack('B'*4,TriggerPrice)
            for c in TriggerPrice1:orderData.append(c)

            DisclosedQty=struct.pack('I',self.cDisclosedQty)
            DisclosedQty1=struct.unpack('B'*4,DisclosedQty)
            for c in DisclosedQty1:orderData.append(c)

            ExecutedQty=struct.pack('I',self.cExecutedQty)
            ExecutedQty1=struct.unpack('B'*4,ExecutedQty)
            for c in ExecutedQty1:orderData.append(c)
            for c in self.cRMSCode:orderData.append(ord(c))

            ExecutedPrice=struct.pack('I',self.cExecutedPrice)
            ExecutedPrice1=struct.unpack('B'*4,ExecutedPrice)
            for c in ExecutedPrice1:orderData.append(c)
            for c in self.cAfterHour:orderData.append(ord(c))
            for c in self.cGTDFlag:orderData.append(ord(c))
            for c in self.cGTD:orderData.append(ord(c))
            for c in self.cReserved:orderData.append(ord(c))
            return orderData
        except:
            logger.exception(PrintException())

    def ToString():
        pass

class OrderRequest():
    def __init__(self,transcode):
        self._Header =None
        self._RequestID = None
        self._OrderType1 =None
        self._ExchangeCode = None
        self._OrderCount = 0
        self._lstOrderItems =[]
        self._Reserved =None

    @property
    def cHeader(self):
        return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cRequestID(self):return self._RequestID
    @cRequestID.setter
    def Prop02RequestID(self,value):self._RequestID=value+'\0'*(10-len(value))

    @property
    def cOrderCount(self):return self._OrderCount
    @cOrderCount.setter
    def Prop03OrderCount(self,value):self._OrderCount=value

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop04ExchangeCode(self,value):self._ExchangeCode=value+'\0'*(2-len(value))

    @property
    def cOrderType1(self):return self._OrderType1
    @cOrderType1.setter
    def Prop05OrderType1(self,value):self._OrderType1=value+'\0'*(10-len(value))

    @property
    def clstOrderItems(self):return self._lstOrderItems
    @clstOrderItems.setter
    def Prop06OrderItems(self,value):self._lstOrderItems=value

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop07Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def StructToByte(self,orderData):
        try:
            placeOrder=array('B')
            for c in self.cHeader:placeOrder.append(c)
            for c in self.cRequestID:placeOrder.append(ord(c))
            orderC=struct.pack('H',self.cOrderCount)
            orderC1=struct.unpack('B'*2,orderC)
            for c in orderC1:placeOrder.append(c)
            for c in self.cExchangeCode:placeOrder.append(ord(c))
            for c in self.cOrderType1:placeOrder.append(ord(c))
            placeOrder=placeOrder+orderData
            for c in self.cReserved:placeOrder.append(ord(c))
            return placeOrder
        except:
            logger.exception(PrintException())

    def ToString(self):
        try:
            return "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(
                '\n',MessageHeader.ToString(self.cHeader),"|", "RequestID = " ,self.cRequestID.strip('\x00') , "|" ,"OrderCount = " ,self.cOrderCount,"|","ExchangeCode = ",self.cExchangeCode, "|","OrderType1 = ",self.cOrderType1.strip('\x00'), "|" , "selfs = " ,self.clstOrderItems[0:], "|" , "Reserved = " ,self.cReserved
            )
        except:
            logger.exception(PrintException())

class FeedRequestF():
    def __init__(self,transcode):
        self._Header =None
        self._Count =None
        self._ScripList =None
        self._Reserved =None

    @property
    def cHeader(self):
        return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cCount(self):return self._Count
    @cCount.setter
    def Prop02Count(self,value):self._Count=value

    @property
    def cScripList(self):return self._ScripList
    @cScripList.setter
    def Prop03ScripList(self,value):self._ScripList=value+'\0'*(12-len(value))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop04Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def StructToByte(self):
        try:
            FeedRequest=array('B')
            for c in self.cHeader:FeedRequest.append(c)
            Count=struct.pack('H',self.cCount)
            Count1=struct.unpack('B'*2,Count)
            for c in Count1:FeedRequest.append(c)
            for c in self.cScripList:FeedRequest.append(ord(c))
            for c in self.cReserved:FeedRequest.append(ord(c))
            return FeedRequest
        except:
            logger.exception(PrintException())

    def ToString(self):
        try:
            return "{}{}{}{}{}{}{}{}{}{}{}".format(
                '\n',MessageHeader.ToString(self.cHeader),"|", "Count = " ,self.cCount , "|" ,"ScripList = " ,self.cScripList.strip('\x00'),"|","Reserved = ",self.cReserved.strip('\x00')
            )
        except:
            logger.exception(PrintException())

class FeedResponse():
    # __slots__=['_Header','_Exchange','_ScripToken','_LTPrice','_LTQuantity','_LTDate','_BidPrice','_BidQuantity','_OfferPrice','_OfferQuantity','_TotalTradedQty','_TradedQuantity','_AverageTradePrice','_Open','_High','_Low','_Close','_PerChange','_TurnOver','_YearlyHigh','_YearlyLow','_UpperCkt','_LowerCkt','_Difference','_CostofCarry1','_CostOfCarry2','_ChangeIndicator','_SpotPrice','_OITime','_OI','_OIHigh','_OILow','_TotalTrades','_TradeValueFlag','_Trend','_SunFlag','_AllnoneFlag','_Tender','_PriceQuotation','_TotalBuyQty','_TotalSellQty','_SegmentId','_OIDifference','_OIDiffPercentage','_Reserved']
    def __init__(self,tranCode):
        try:
            self._Header = None
            self._Exchange = None
            self._ScripToken = None
            self._LTPrice = 0
            self._LTQuantity = 0
            self._LTDate= None
            self._BidPrice = 0
            self._BidQuantity = 0
            self._OfferPrice = 0
            self._OfferQuantity = 0
            self._TotalTradedQty = 0
            self._TradedQuantity = 0
            self._AverageTradePrice = 0
            self._Open = 0
            self._High = 0
            self._Low = 0
            self._Close = 0
            self._PerChange = 0
            self._TurnOver = 0
            self._YearlyHigh = 0
            self._YearlyLow = 0
            self._UpperCkt = 0
            self._LowerCkt = 0
            self._Difference = 0
            self._CostofCarry1 = 0
            self._CostOfCarry2 = 0
            self._ChangeIndicator = None
            self._SpotPrice = 0
            self._OITime =None
            self._OI = 0
            self._OIHigh = 0
            self._OILow = 0
            self._TotalTrades = 0
            self._TradeValueFlag = None
            self._Trend = None
            self._SunFlag= None
            self._AllnoneFlag =None
            self._Tender = 0
            self._PriceQuotation = None
            self._TotalBuyQty = 0
            self._TotalSellQty = 0
            self._SegmentId = None
            self._OIDifference = 0
            self._OIDiffPercentage = 0
            self._Reserved = None
        except:
            logger.exception(PrintException())

    @property
    def cHeader(self):
        return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cExchange(self):return self._Exchange
    @cExchange.setter
    def Prop02Exchange(self,val):self._Exchange=val+'\0'*(2-len(val))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop03ScripToken(self,val):self._ScripToken=val+'\0'*(100-len(val))

    @property
    def cLTPrice(self):return self._LTPrice
    @cLTPrice.setter
    def Prop04LTPrice(self,val):self._LTPrice=val

    @property
    def cLTQuantity(self):return self._LTQuantity
    @cLTQuantity.setter
    def Prop05LTQuantity(self,val):self._LTQuantity=val

    @property
    def cLTDate(self):return self._LTDate
    @cLTDate.setter
    def Prop06LTDate(self,val):self._LTDate=val+'\0'*(25-len(val))

    @property
    def cBidPrice(self):return self._BidPrice
    @cBidPrice.setter
    def Prop07BidPrice(self,val):self._BidPrice=val

    @property
    def cBidQuantity(self):return self._BidQuantity
    @cBidQuantity.setter
    def Prop08BidQuantity(self,val):self._BidQuantity=val

    @property
    def cOfferPrice(self):return self._OfferPrice
    @cOfferPrice.setter
    def Prop09OfferPrice(self,val):self._OfferPrice=val

    @property
    def cOfferQuantity(self):return self._OfferQuantity
    @cOfferQuantity.setter
    def Prop10OfferQuantity(self,val):self._OfferQuantity=val

    @property
    def cTotalTradedQty(self):return self._TotalTradedQty
    @cTotalTradedQty.setter
    def Prop11TotalTradedQty(self,val):self._TotalTradedQty=val

    @property
    def cTradedQuantity(self):return self._TradedQuantity
    @cTradedQuantity.setter
    def Prop12TradedQuantity(self,val):self._TradedQuantity=val

    @property
    def cAverageTradePrice(self):return self._AverageTradePrice
    @cAverageTradePrice.setter
    def Prop13AverageTradePrice(self,val):self._AverageTradePrice=val

    @property
    def cOpen(self):return self._Open
    @cOpen.setter
    def Prop14Open(self,val):self._Open=val

    @property
    def cHigh(self):return self._High
    @cHigh.setter
    def Prop15High(self,val):self._High=val

    @property
    def cLow(self):return self._Low
    @cLow.setter
    def Prop16Low(self,val):self._Low=val

    @property
    def cClose(self):return self._Close
    @cClose.setter
    def Prop17Close(self,val):self._Close=val

    @property
    def cPerChange(self):return self._PerChange
    @cPerChange.setter
    def Prop18PerChange(self,val):self._PerChange=val

    @property
    def cTurnOver(self):return self._TurnOver
    @cTurnOver.setter
    def Prop19TurnOver(self,val):self._TurnOver=val

    @property
    def cYearlyHigh(self):return self._YearlyHigh
    @cYearlyHigh.setter
    def Prop20YearlyHigh(self,val):self._YearlyHigh=val

    @property
    def cYearlyLow(self):return self._YearlyLow
    @cYearlyLow.setter
    def Prop21YearlyLow(self,val):self._YearlyLow=val

    @property
    def cUpperCkt(self):return self._UpperCkt
    @cUpperCkt.setter
    def Prop22UpperCkt(self,val):self._UpperCkt=val

    @property
    def cLowerCkt(self):return self._LowerCkt
    @cLowerCkt.setter
    def Prop23LowerCkt(self,val):self._LowerCkt=val

    @property
    def cDifference(self):return self._Difference
    @cDifference.setter
    def Prop24Difference(self,val):self._Difference=val

    @property
    def cCostofCarry1(self):return self._CostofCarry1
    @cCostofCarry1.setter
    def Prop25CostofCarry1(self,val):self._CostofCarry1=val

    @property
    def cCostOfCarry2(self):return self._CostOfCarry2
    @cCostOfCarry2.setter
    def Prop26CostOfCarry2(self,val):self._CostOfCarry2=val

    @property
    def cChangeIndicator(self):return self._ChangeIndicator
    @cChangeIndicator.setter
    def Prop27ChangeIndicator(self,val):self._ChangeIndicator=val+'\0'*(10-len(val))

    @property
    def cSpotPrice(self):return self._SpotPrice
    @cSpotPrice.setter
    def Prop28SpotPrice(self,val):self._SpotPrice=val

    @property
    def cOITime(self):return self._OITime
    @cOITime.setter
    def Prop29OITime(self,val):self._OITime=val+'\0'*(20-len(val))

    @property
    def cOI(self):return self._OI
    @cOI.setter
    def Prop30OI(self,val):self._OI=val

    @property
    def cOIHigh(self):return self._OIHigh
    @cOIHigh.setter
    def Prop31OIHigh(self,val):self._OIHigh=val

    @property
    def cOILow(self):return self._OILow
    @cOILow.setter
    def Prop32OILow(self,val):self._OILow=val

    @property
    def cTotalTrades(self):return self._TotalTrades
    @cTotalTrades.setter
    def Prop33TotalTrades(self,val):self._TotalTrades=val

    @property
    def cTradeValueFlag(self):return self._TradeValueFlag
    @cTradeValueFlag.setter
    def Prop34TradeValueFlag(self,val):self._TradeValueFlag=val+'\0'*(10-len(val))

    @property
    def cTrend(self):return self._Trend
    @cTrend.setter
    def Prop35Trend(self,val):self._Trend=val+'\0'*(10-len(val))

    @property
    def cSunFlag(self):return self._SunFlag
    @cSunFlag.setter
    def Prop36SunFlag(self,val):self._SunFlag=val+'\0'*(10-len(val))

    @property
    def cAllnoneFlag(self):return self._AllnoneFlag
    @cAllnoneFlag.setter
    def Prop37AllnoneFlag(self,val):self._AllnoneFlag=val+'\0'*(10-len(val))

    @property
    def cTender(self):return self._Tender
    @cTender.setter
    def Prop38Tender(self,val):self._Tender=val

    @property
    def cPriceQuotation(self):return self._PriceQuotation
    @cPriceQuotation.setter
    def Prop39PriceQuotation(self,val):self._PriceQuotation=val+'\0'*(20-len(val))

    @property
    def cTotalBuyQty(self):return self._TotalBuyQty
    @cTotalBuyQty.setter
    def Prop40TotalBuyQty(self,val):self._TotalBuyQty=val

    @property
    def cTotalSellQty(self):return self._TotalSellQty
    @cTotalSellQty.setter
    def Prop41TotalSellQty(self,val):self._TotalSellQty=val

    @property
    def cSegmentId(self):return self._SegmentId
    @cSegmentId.setter
    def Prop42SegmentId(self,val):self._SegmentId=val+'\0'*(20-len(val))

    @property
    def cOIDifference(self):return self._OIDifference
    @cOIDifference.setter
    def Prop43OIDifference(self,val):self._OIDifference=val

    @property
    def cOIDiffPercentage(self):return self._OIDiffPercentage
    @cOIDiffPercentage.setter
    def Prop44OIDiffPercentage(self,val):self._OIDiffPercentage=val

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop45Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def ByteToStruct(self,val):
        try:
            cHeader=MessageHeader(1)
            cHeader.ByteToStruct(val[0:6])
            self.Prop01Header=[cHeader.cMessageLength[0],cHeader.Prop02TransactionCode[0]]
            self.Prop02Exchange=struct.pack("B"*len(val[6:11]),*val[6:11]).decode('utf8')
            self.Prop03ScripToken =struct.pack("B"*len(val[11:21]),*val[11:21]).decode('utf8')
            self.Prop04LTPrice =struct.unpack('I',val[21:25])[0]
            self.Prop05LTQuantity =struct.unpack('I',val[25:29])[0]
            self.Prop06LTDate =struct.pack("B"*len(val[29:54]),*val[29:54]).decode('utf8')
            self.Prop07BidPrice =struct.unpack('I',val[54:58])[0]
            self.Prop08BidQuantity =struct.unpack('I',val[58:62])[0]
            self.Prop09OfferPrice =struct.unpack('I',val[62:66])[0]
            self.Prop10OfferQuantity =struct.unpack('I',val[66:70])[0]
            self.Prop11TotalTradedQty =  struct.unpack('I',val[70:74])[0]
            self.Prop12TradedQuantity =  struct.unpack('I',val[74:78])[0]
            self.Prop13AverageTradePrice=struct.unpack('I',val[78:82])[0]
            self.Prop14Open =            struct.unpack('I',val[82:86])[0]
            self.Prop15High =            struct.unpack('I',val[86:90])[0]
            self.Prop16Low =             struct.unpack('I',val[90:94])[0]
            self.Prop17Close =           struct.unpack('I',val[94:98])[0]
            self.Prop18PerChange =       struct.unpack('I',val[98:102])[0]
            self.Prop19TurnOver =        struct.unpack('I',val[102:106])[0]
            self.Prop20YearlyHigh =      struct.unpack('I',val[106:110])[0]
            self.Prop21YearlyLow =       struct.unpack('I',val[110:114])[0]
            self.Prop22UpperCkt =        struct.unpack('I',val[114:118])[0]
            self.Prop23LowerCkt =        struct.unpack('I',val[118:122])[0]
            self.Prop24Difference =      struct.unpack('I',val[122:126])[0]
            self.Prop25CostofCarry1 =    struct.unpack('I',val[126:130])[0]
            self.Prop26CostOfCarry2 =    struct.unpack('I',val[130:134])[0]
            self.Prop27ChangeIndicator = struct.pack("B"*len(val[134:144]),*val[134:144]).decode('utf8')
            self.Prop28SpotPrice =       struct.unpack('I',val[144:148])[0]
            self.Prop29OITime =          struct.pack("B"*len(val[148:168]),*val[148:168]).decode('utf8')
            self.Prop30OI =              struct.unpack('I',val[168:172])[0]
            self.Prop31OIHigh =          struct.unpack('I',val[172:176])[0]
            self.Prop32OILow =           struct.unpack('I',val[176:180])[0]
            self.Prop33TotalTrades =     struct.unpack('I',val[180:184])[0]
            self.Prop34TradeValueFlag =  struct.pack("B"*len(val[184:194]),*val[184:194]).decode('utf8')
            self.Prop35Trend =           struct.pack("B"*len(val[194:204]),*val[194:204]).decode('utf8')
            self.Prop36SunFlag =         struct.pack("B"*len(val[204:214]),*val[204:214]).decode('utf8')
            self.Prop37AllnoneFlag =     struct.pack("B"*len(val[214:224]),*val[214:224]).decode('utf8')
            self.Prop38Tender =          struct.unpack('I',val[224:228])[0]
            self.Prop39PriceQuotation =  struct.pack("B"*len(val[228:248]),*val[228:248]).decode('utf8')
            self.Prop40TotalBuyQty =     struct.unpack('I',val[248:252])[0]
            self.Prop41TotalSellQty =    struct.unpack('I',val[252:256])[0]
            self.Prop42SegmentId =       struct.pack("B"*len(val[256:276]),*val[256:276]).decode('cp1252')
            self.Prop43OIDifference =    struct.unpack('I',val[276:280])[0]
            self.Prop44OIDiffPercentage =struct.unpack('I',val[280:284])[0]
            self.Prop45Reserved =        struct.pack("B"*len(val[284:384]),*val[284:384]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        try:
            return ('\n'+MessageHeader.ToString(self.cHeader)+"|"+"Exchange ="+self.cExchange +"|"+" ScripToken="+self.cScripToken.strip('\x00')+"|" +"LTPrice ="+str(self.cLTPrice)
            +"|"+"LTQuantity ="+str(self.cLTQuantity) +"|"+" LTDate="+str(self.cLTDate).strip('\x00') +"|"+"BidPrice ="+str( self.cBidPrice)
            +"|"+"BidQuantity ="+str(self.cBidQuantity) +"|"+"OfferPrice ="+str(self.cOfferPrice) +"|"+"OfferQuantity ="+str(self.cOfferQuantity)
            +"|"+"TotalTradedQty ="+str(self.cTotalTradedQty) +"|"+"TradedQuantity ="+str(self.cTradedQuantity)
            +"|"+"AverageTradePrice ="+str(self.cAverageTradePrice) +"|"+"Open ="+ str(self.cOpen)+"|"+"High ="+ str(self.cHigh)
            +"|"+"Low ="+str(self.cLow) +"|"+"Close ="+str(self.cClose) +"|"+"PerChange ="+ str(self.cPerChange)+"|"+"TurnOver ="+str(self.cTurnOver)
            +"|"+"YearlyHigh ="+str(self.cYearlyHigh) +"|"+"YearlyLow ="+str(self.cYearlyLow )+"|"+"UpperCkt ="+str(self.cUpperCkt)
            +"|"+"LowerCkt ="+str(self.cLowerCkt) +"|"+"Difference ="+str(self.cDifference) +"|"+"CostofCarry1 ="+str(self.cCostofCarry1)
            +"|"+"CostOfCarry2 ="+str(self.cCostOfCarry2) +"|"+"ChangeIndicator ="+str(self.cChangeIndicator).strip('\x00') +"|"+"SpotPrice ="+str(self.cSpotPrice)
            +"|"+"OITime ="+str(self.cOITime).strip('\x00') +"|"+"OI ="+str(self.cOI) +"|"+"High ="+str(self.cHigh) +"|"+"OILow ="+str(self.cOILow)
            +"|"+"TotalTrades ="+str(self.cTotalTrades) +"|"+"TradeValueFlag ="+str(self.cTradeValueFlag).strip('\x00') +"|"+"Trend ="+str(self.cTrend).strip('\x00')
            +"|"+"SunFlag ="+str(self.cSunFlag).strip('\x00') +"|"+"AllnoneFlag ="+str(self.cAllnoneFlag).strip('\x00') +"|"+"Tender ="+str(self.cTender)
            +"|"+"PriceQuotation ="+str(self.cPriceQuotation).strip('\x00')
            +"|"+"TotalBuyQty ="+str(self.cTotalBuyQty)
            +"|"+"SellQty ="+str(self.cTotalSellQty)
            +"|"+"SegmentId ="+str(self.cSegmentId).strip('\x00')
            +"|"+"OIDifference ="+str(self.cOIDifference) +"|"+"DiffPercentage ="+str(self.cOIDiffPercentage)
            +"|"+"Reserved ="+str(self.cReserved).strip('\x00'))

        except:
            logger.exception(PrintException())

class MarketDepthRequest():
    def __init__(self,transcode):
        self._Header =None
        self._ExchangeCode =None
        self._ScripCode =None
        self._Reserved =None

    @property
    def cHeader(self):
        return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cScripCode(self):return self._ScripCode
    @cScripCode.setter
    def Prop03ScripCode(self,value):self._ScripCode=value+'\0'*(10-len(value))

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,value):self._ExchangeCode=value+'\0'*(5-len(value))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop04Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def StructToByte(self):
        try:
            DepthRequest=array('B')
            for c in self.cHeader:DepthRequest.append(c)
            for c in self.cExchangeCode:DepthRequest.append(ord(c))
            for c in self.cScripCode:DepthRequest.append(ord(c))
            for c in self.cReserved:DepthRequest.append(ord(c))
            return DepthRequest
        except:
            logger.exception(PrintException())

    def ByteToStruct(self,val):
        cHeader=MessageHeader(1)
        cHeader.ByteToStruct(val[0:6])
        self.Prop01Header=[cHeader.cMessageLength[0],cHeader.Prop02TransactionCode[0]]
        self.Prop02ExchangeCode=struct.pack("B"*len(val[6:11]),*val[6:11]).decode('utf8')
        self.Prop03ScripCode=struct.pack("B"*len(val[11:21]),*val[11:21]).decode('utf8')
        self.Prop04Reserved=struct.pack("B"*len(val[21:121]),*val[21:121]).decode('utf8')

    def ToString(self):
        try:
            return "{}{}{}{}{}{}{}{}{}{}".format(
                MessageHeader.ToString(self.cHeader),"|", "ExchangeCode = " ,self.cExchangeCode , "|" ,"ScripList = " ,self.cScripCode,"|","Reserved = ",self.cReserved)
        except:
            logger.exception(PrintException())

class MarketDepthResponse():
    def __init__(self,tranCode):
        self._Header = None
        self._ExchangeCode = None
        self._Exchange = None
        self._LastTradedTime = None
        self._ScripCode = None
        self._TotalBuyQuantity = 0
        self._TotSellQuantity = 0
        self._BuyPrice1 = 0
        self._BuyQuantity1 = 0
        self._BuyNumberOfOrder1 = 0
        self._BuyPrice2 = 0
        self._BuyQuantity2 = 0
        self._BuyNumberOfOrder2 = 0
        self._BuyPrice3 = 0
        self._BuyQuantity3 = 0
        self._BuyNumberOfOrder3 = 0
        self._BuyPrice4 = 0
        self._BuyQuantity4 = 0
        self._BuyNumberOfOrder4 = 0
        self._BuyPrice5 = 0
        self._BuyQuantity5 = 0
        self._BuyNumberOfOrder5 = 0
        self._SellPrice1 = 0
        self._SellQuantity1 = 0
        self._SellNumberOfOrder1 = 0
        self._SellPrice2 = 0
        self._SellQuantity2 = 0
        self._SellNumberOfOrder2 = 0
        self._SellPrice3 = 0
        self._SellQuantity3 = 0
        self._SellNumberOfOrder3 = 0
        self._SellPrice4 = 0
        self._SellQuantity4 = 0
        self._SellNumberOfOrder4 = 0
        self._SellPrice5 = 0
        self._SellQuantity5 = 0
        self._SellNumberOfOrder5 = 0
        self._Reserved = None

    @property
    def cHeader(self):
        return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,val):self._ExchangeCode=val+'\0'*(5-len(val))

    @property
    def cExchange(self):return self._Exchange
    @cExchange.setter
    def Prop03Exchange(self,val):self._Exchange=val+'\0'*(10-len(val))

    @property
    def cLastTradedTime(self):return self._LastTradedTime
    @cLastTradedTime.setter
    def Prop04LastTradedTime(self,val):self._LastTradedTime=val+'\0'*(25-len(val))

    @property
    def cScripCode(self):return self._ScripCode
    @cScripCode.setter
    def Prop05ScripCode(self,val):self._ScripCode=val+'\0'*(10-len(val))

    @property
    def cTotalBuyQuantity(self):return self._TotalBuyQuantity
    @cTotalBuyQuantity.setter
    def Prop06TotalBuyQuantity(self,val):self._TotalBuyQuantity=val

    @property
    def cTotSellQuantity(self):return self._TotSellQuantity
    @cTotSellQuantity.setter
    def Prop07TotSellQuantity(self,val):self._TotSellQuantity=val

    @property
    def cBuyPrice1(self):return self._BuyPrice1
    @cBuyPrice1.setter
    def Prop08BuyPrice1(self,val):self._BuyPrice1=val

    @property
    def cBuyQuantity1(self):return self._BuyQuantity1
    @cBuyQuantity1.setter
    def Prop09BuyQuantity1(self,val):self._BuyQuantity1=val

    @property
    def cBuyNumberOfOrder1(self):return self._BuyNumberOfOrder1
    @cBuyNumberOfOrder1.setter
    def Prop10BuyNumberOfOrder1(self,val):self._BuyNumberOfOrder1=val

    @property
    def cBuyPrice2(self):return self._BuyPrice2
    @cBuyPrice2.setter
    def Prop11BuyPrice2(self,val):self._BuyPrice2=val

    @property
    def cBuyQuantity2(self):return self._BuyQuantity2
    @cBuyQuantity2.setter
    def Prop12BuyQuantity2(self,val):self._BuyQuantity2=val

    @property
    def cBuyNumberOfOrder2(self):return self._BuyNumberOfOrder2
    @cBuyNumberOfOrder2.setter
    def Prop13BuyNumberOfOrder2(self,val):self._BuyNumberOfOrder2=val

    @property
    def cBuyPrice3(self):return self._BuyPrice3
    @cBuyPrice3.setter
    def Prop14BuyPrice3(self,val):self._BuyPrice3=val

    @property
    def cBuyQuantity3(self):return self._BuyQuantity3
    @cBuyQuantity3.setter
    def Prop15BuyQuantity3(self,val):self._BuyQuantity3=val

    @property
    def cBuyNumberOfOrder3(self):return self._BuyNumberOfOrder3
    @cBuyNumberOfOrder3.setter
    def Prop16BuyNumberOfOrder3(self,val):self._BuyNumberOfOrder3=val

    @property
    def cBuyPrice4(self):return self._BuyPrice4
    @cBuyPrice4.setter
    def Prop17BuyPrice4(self,val):self._BuyPrice4=val

    @property
    def cBuyQuantity4(self):return self._BuyQuantity4
    @cBuyQuantity4.setter
    def Prop18BuyQuantity4(self,val):self._BuyQuantity4=val

    @property
    def cBuyNumberOfOrder4(self):return self._BuyNumberOfOrder4
    @cBuyNumberOfOrder4.setter
    def Prop19BuyNumberOfOrder4(self,val):self._BuyNumberOfOrder4=val

    @property
    def cBuyPrice5(self):return self._BuyPrice5
    @cBuyPrice5.setter
    def Prop20BuyPrice5(self,val):self._BuyPrice5=val

    @property
    def cBuyQuantity5(self):return self._BuyQuantity5
    @cBuyQuantity5.setter
    def Prop21BuyQuantity5(self,val):self._BuyQuantity5=val

    @property
    def cBuyNumberOfOrder5(self):return self._BuyNumberOfOrder5
    @cBuyNumberOfOrder5.setter
    def Prop22BuyNumberOfOrder5(self,val):self._BuyNumberOfOrder5=val

    @property
    def cSellPrice1(self):return self._SellPrice1
    @cSellPrice1.setter
    def Prop23SellPrice1(self,val):self._SellPrice1=val

    @property
    def cSellQuantity1(self):return self._SellQuantity1
    @cSellQuantity1.setter
    def Prop24SellQuantity1(self,val):self._SellQuantity1=val

    @property
    def cSellNumberOfOrder1(self):return self._SellNumberOfOrder1
    @cSellNumberOfOrder1.setter
    def Prop25SellNumberOfOrder1(self,val):self._SellNumberOfOrder1=val

    @property
    def cSellPrice2(self):return self._SellPrice2
    @cSellPrice2.setter
    def Prop26SellPrice2(self,val):self._SellPrice2=val

    @property
    def cSellQuantity2(self):return self._SellQuantity2
    @cSellQuantity2.setter
    def Prop27SellQuantity2(self,val):self._SellQuantity2=val

    @property
    def cSellNumberOfOrder2(self):return self._SellNumberOfOrder2
    @cSellNumberOfOrder2.setter
    def Prop28SellNumberOfOrder2(self,val):self._SellNumberOfOrder2=val

    @property
    def cSellPrice3(self):return self._SellPrice3
    @cSellPrice3.setter
    def Prop29SellPrice3(self,val):self._SellPrice3=val

    @property
    def cSellQuantity3(self):return self._SellQuantity3
    @cSellQuantity3.setter
    def Prop30SellQuantity3(self,val):self._SellQuantity3=val

    @property
    def cSellNumberOfOrder3(self):return self._SellNumberOfOrder3
    @cSellNumberOfOrder3.setter
    def Prop31SellNumberOfOrder3(self,val):self._SellNumberOfOrder3=val

    @property
    def cSellPrice4(self):return self._SellPrice4
    @cSellPrice4.setter
    def Prop32SellPrice4(self,val):self._SellPrice4=val

    @property
    def cSellQuantity4(self):return self._SellQuantity4
    @cSellQuantity4.setter
    def Prop33SellQuantity4(self,val):self._SellQuantity4=val

    @property
    def cSellNumberOfOrder4(self):return self._SellNumberOfOrder4
    @cSellNumberOfOrder4.setter
    def Prop34SellNumberOfOrder4(self,val):self._SellNumberOfOrder4=val

    @property
    def cSellPrice5(self):return self._SellPrice5
    @cSellPrice5.setter
    def Prop35SellPrice5(self,val):self._SellPrice5=val

    @property
    def cSellQuantity5(self):return self._SellQuantity5
    @cSellQuantity5.setter
    def Prop36SellQuantity5(self,val):self._SellQuantity5=val

    @property
    def cSellNumberOfOrder5(self):return self._SellNumberOfOrder5
    @cSellNumberOfOrder5.setter
    def Prop37SellNumberOfOrder5(self,val):self._SellNumberOfOrder5=val

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop38Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))

    def ByteToStruct(self,val):
        try:
            cHeader=MessageHeader(1)
            cHeader.ByteToStruct(val[0:6])
            self.Prop01Header=[cHeader.cMessageLength[0],cHeader.Prop02TransactionCode[0]]
            self.Prop02ExchangeCode=struct.pack("B"*len(val[6:11]),*val[6:11]).decode('utf8')
            self.Prop03Exchange=struct.pack("B"*len(val[11:21]),*val[11:21]).decode('utf8')
            self.Prop04LastTradedTime=struct.pack("B"*len(val[21:46]),*val[21:46]).decode('utf8')
            self.Prop05ScripCode=struct.pack("B"*len(val[46:56]),*val[46:56]).decode('utf8')
            self.Prop06TotalBuyQuantity=struct.unpack('I',val[56:60])
            self.Prop07TotSellQuantity=struct.unpack('I',val[60:64])
            self.Prop08BuyPrice1=struct.unpack('I',val[64:68])
            self.Prop09BuyQuantity1=struct.unpack('I',val[68:72])
            self.Prop10BuyNumberOfOrder1=struct.unpack('I',val[72:76])
            self.Prop11BuyPrice2=struct.unpack('I',val[76:80])
            self.Prop12BuyQuantity2=struct.unpack('I',val[80:84])
            self.Prop13BuyNumberOfOrder2=struct.unpack('I',val[84:88])
            self.Prop14BuyPrice3=struct.unpack('I',val[88:92])
            self.Prop15BuyQuantity3=struct.unpack('I',val[92:96])
            self.Prop16BuyNumberOfOrder3=struct.unpack('I',val[96:100])
            self.Prop17BuyPrice4=struct.unpack('I',val[100:104])
            self.Prop18BuyQuantity4=struct.unpack('I',val[104:108])
            self.Prop19BuyNumberOfOrder4=struct.unpack('I',val[108:112])
            self.Prop20BuyPrice5=struct.unpack('I',val[112:116])
            self.Prop21BuyQuantity5=struct.unpack('I',val[116:120])
            self.Prop22BuyNumberOfOrder5=struct.unpack('I',val[120:124])
            self.Prop23SellPrice1=struct.unpack('I',val[124:128])
            self.Prop24SellQuantity1=struct.unpack('I',val[128:132])
            self.Prop25SellNumberOfOrder1=struct.unpack('I',val[132:136])
            self.Prop26SellPrice2=struct.unpack('I',val[136:140])
            self.Prop27SellQuantity2=struct.unpack('I',val[140:144])
            self.Prop28SellNumberOfOrder2=struct.unpack('I',val[144:148])
            self.Prop29SellPrice3=struct.unpack('I',val[148:152])
            self.Prop30SellQuantity3=struct.unpack('I',val[152:156])
            self.Prop31SellNumberOfOrder3=struct.unpack('I',val[156:160])
            self.Prop32SellPrice4=struct.unpack('I',val[160:164])
            self.Prop33SellQuantity4=struct.unpack('I',val[164:168])
            self.Prop34SellNumberOfOrder4=struct.unpack('I',val[168:172])
            self.Prop35SellPrice5=struct.unpack('I',val[172:176])
            self.Prop36SellQuantity5=struct.unpack('I',val[176:180])
            self.Prop37SellNumberOfOrder5=struct.unpack('I',val[180:184])
            self.Prop38Reserved=struct.pack("B"*len(val[184:284]),*val[184:284]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        try:
             return (MessageHeader.ToString(self.cHeader) + "|" + "ExchangeCode = " + str(self.cExchangeCode) + "|" + "Exchange = " + str(self.cExchange) + "|" + "LastTradedTime = " + str(self.cLastTradedTime).strip() + "|" + "ScripCode = " + str(self.cScripCode) + "|" + "TotalBuyQuantity  = " + str(self.cTotalBuyQuantity) + "|" + "TotSellQuantity = " + str(self.cTotSellQuantity) + "|" + "BuyPrice1 = " + str(self.cBuyPrice1)
                    + "|" + "BuyQuantity1 = " + str(self.cBuyQuantity1) + "|" + "BuyNumberOfOrder1 = " + str(self.cBuyNumberOfOrder1) + "|" + "Reserved = " + str(self.cBuyPrice2) + "|" + "BuyQuantity2 = "
                    + str(self.cBuyQuantity2) + "|" + "BuyNumberOfOrder2 = " + str(self.cBuyNumberOfOrder2)+ "|" + "BuyPrice3 = " + str(self.cBuyPrice3) + "|" + "BuyQuantity3 = " + str(self.cBuyQuantity3) + "|" + "BuyNumberOfOrder3 = " + str(self.cBuyNumberOfOrder3) + "|" + "BuyPrice4 = " + str(self.cBuyPrice4) + "|" + "BuyQuantity4 = " + str(self.cBuyQuantity4) + "|" + "BuyNumberOfOrder4 = " + str(self.cBuyNumberOfOrder4) + "|" + "BuyPrice5 = " + str(self.cBuyPrice5) + "|" + "BuyQuantity5 = " + str(self.cBuyQuantity5)+ "|" + "BuyNumberOfOrder5 = " + str(self.cBuyNumberOfOrder5) + "|" + "SellPrice1 = " + str(self.cSellPrice1) + "|" + "SellQuantity1 = " + str(self.cSellQuantity1) + "|" + "SellNumberOfOrder1 = " + str(self.cSellNumberOfOrder1) + str(self.cSellPrice2) + "|" + "SellQuantity2 = " + str(self.cSellQuantity2) + "|" + "NumberOfOrder2 = " + str(self.cSellNumberOfOrder2) + "|" + "SellPrice3  = " + str(self.cSellPrice3) + "|" + "Quantity3 = " + str(self.cSellQuantity3)+ "|" + "SellNumberOfOrder3 = " + str(self.cSellNumberOfOrder3) + "|" + "SellPrice4 = " + str(self.cSellPrice4) + "|" + "SellQuantity4 = " + str(self.cSellQuantity4) + "|" + "SellNumberOfOrder4 = " + str(self.cSellNumberOfOrder4) + "|" + "SellPrice5 = " + str(self.cSellPrice5)
                    + "|" + "SellQuantity5 = " + str(self.cSellQuantity5) + "|" + "SellNumberOfOrder5 = " + str(self.cSellNumberOfOrder5) + "|" + "Reserved = " + str(self.cReserved).strip())
        except:
            logger.exception(PrintException())

class SharekhanOrderConfirmation(): #order confirmation
    def __init__(self,tranCode):
        self._Header = MessageHeader(1)
        self._RequestID = None
        self._ExchangeCode =None
        self._Count = 0
        self._OrderConfirmationItems =None
        self._Reserved =None

    @property
    def cHeader(self):
        return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cRequestID(self):return self._RequestID
    @cRequestID.setter
    def Prop02RequestID(self,value):self._RequestID=value+'\0'*(10-len(value))

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop03ExchangeCode(self,value):self._ExchangeCode=value+'\0'*(2-len(value))

    @property
    def cCount(self):return self._OrderCount
    @cCount.setter
    def Prop04Count(self,value):self._OrderCount=value

    @property
    def cOrderConfirmationItems(self):return self._OrderConfirmationItems
    @cOrderConfirmationItems.setter
    def Prop05OrderConfirmationItems(self,value):self._OrderConfirmationItems=value

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop06Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def ByteToStruct(self,val):
        try:
            cHeader=MessageHeader(1)
            cHeader.ByteToStruct(val[0:6])
            self.Prop01Header=[cHeader.cMessageLength[0],cHeader.Prop02TransactionCode[0]]
            self.Prop02RequestID=struct.pack("B"*len(val[6:16]),*val[6:16]).decode('utf8')
            self.Prop03ExchangeCode=struct.pack("B"*len(val[16:18]),*val[16:18]).decode('utf8')
            self.Prop04Count=struct.unpack('H',val[18:20])
            items=[]
            startIndex = 20
            for i in self.cCount:
                item=OrderConfirmationItem(1)
                orderConfirmation=array('B')
                orderConfirmation.extend(val[startIndex:startIndex+459])
                item.ByteToStruct(orderConfirmation[0:])
                startIndex+=459
                items.append([x[0]+":"+str(x[1]).strip("\x00 ") for x in vars(item).items()])
            self.Prop05OrderConfirmationItems=items[0:]
            self.Prop06Reserved=struct.pack("B"*len(val[56:156]),*val[56:156]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        return (MessageHeader.ToString(self.cHeader) + "|" + "RequestID = " + self.cRequestID + "|" + "ExchangeCode = " + self.cExchangeCode + "|" + "Count = " + str(self.cCount) + "|" + "OrderConfirmationItems = " + str(self.cOrderConfirmationItems[0]) + "|" + "Reserved = " + self.cReserved)

class OrderConfirmationItem():
    def __init__(self,transCode):
        self._DataLength = 0
        self._StatusCode =None
        self._Message = None
        self._SharekhanOrderID =None
        self._OrderDateTime = None
        self._RMSCode = None
        self._CoverOrderID =None
        self._Reserved =None

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cStatusCode(self):return self._StatusCode
    @cStatusCode.setter
    def Prop02StatusCode(self,val):self._StatusCode=val+'\0'*(25-len(val))

    @property
    def cMessage(self):return self._Message
    @cMessage.setter
    def Prop03Message(self,val):self._Message=val+'\0'*(250-len(val))

    @property
    def cSharekhanOrderID(self):return self._SharekhanOrderID
    @cSharekhanOrderID.setter
    def Prop04SharekhanOrderID(self,val):self._SharekhanOrderID=val+'\0'*(20-len(val))

    @property
    def cOrderDateTime(self):return self._OrderDateTime
    @cOrderDateTime.setter
    def Prop05OrderDateTime(self,val):self._OrderDateTime=val+'\0'*(25-len(val))

    @property
    def cRMSCode(self):return self._RMSCode
    @cRMSCode.setter
    def Prop06RMSCode(self,val):self._RMSCode=val+'\0'*(15-len(val))

    @property
    def cCoverOrderID(self):return self._CoverOrderID
    @cCoverOrderID.setter
    def Prop07CoverOrderID(self,val):self._CoverOrderID=val+'\0'*(20-len(val))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop08Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))

    def ByteToStruct(self,val):
        self.Prop01DataLength =struct.unpack('I',val[0:4])[0]
        self.Prop02StatusCode=struct.pack("B"*len(val[4:29]),*val[4:29]).decode('utf8').strip('\x00')
        self.Prop03Message=struct.pack("B"*len(val[29:279]),*val[29:279]).decode('utf8').strip('\x00')
        self.Prop04SharekhanOrderID=struct.pack("B"*len(val[279:299]),*val[279:299]).decode('utf8').strip('\x00')
        self.Prop05OrderDateTime=struct.pack("B"*len(val[299:324]),*val[299:324]).decode('utf8').strip('\x00')
        self.Prop06RMSCode=struct.pack("B"*len(val[324:339]),*val[324:339]).decode('utf8').strip('\x00')
        self.Prop07CoverOrderID=struct.pack("B"*len(val[339:359]),*val[339:359]).decode('utf8').strip('\x00')
        self.Prop08Reserved =struct.pack("B"*len(val[359:459]),*val[359:459]).decode('utf8').strip('\x00')

    def ToString(self):
        return (str(self.cDataLength) + "|" + "StatusCode  = " + self.cStatusCode + "|" + "Message = " + self.cMessage + "|" + "SharekhanOrderID = " + self.cSharekhanOrderID + "|" + "OrderDateTime = " + self.cOrderDateTime + "|" + "RMSCode = " + self.cRMSCode + "|" + "CoverOrderID = " + self.cCoverOrderID + "|" + "Reserved = " + self.cReserved)

class ExchangeTradeConfirmation():
    def __init__(self,transCode):
        self._Header =MessageHeader(1)
        self._ExchangeCode =None
        self._AckCode = 0
        self._MsgLength = 0
        self._SharekhanOrderID = None
        self._ExchangeOrderId = None
        self._ExchangeDateTime = None
        self._TradeID = None
        self._CustomerId = None
        self._ScripToken = None
        self._BuySell = None
        self._OrderQty = 0
        self._RemainingQty = 0
        self._TradeQty = 0
        self._DisclosedQty = 0
        self._DisclosedRemainingQty = 0
        self._OrderPrice = 0
        self._TriggerPrice = 0
        self._TradePrice = 0
        self._ExchangeGTD = None
        self._ExchangeGTDDate = None
        self._ChannelCode = None
        self._ChannelUser = None
        self._ErrorMessage = None
        self._OrderTrailingPrice = 0
        self._OrderTargetPrice = 0
        self._UpperPrice = 0
        self._ChildSLPrice = 0
        self._LowerPrice = 0
        self._Reserved = None

    @property
    def cHeader(self):return self._Header
    @cHeader.setter
    def Prop01Header(self,value):self._Header=value

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,value):self._ExchangeCode=value+'\0'*(2-len(value))

    @property
    def cAckCode(self):return self._AckCode
    @cAckCode.setter
    def Prop03AckCode(self,value):self._AckCode=value

    @property
    def cMsgLength(self):return self._MsgLength
    @cMsgLength.setter
    def Prop04MsgLength(self,value):self._MsgLength=value

    @property
    def cSharekhanOrderID(self):return self._SharekhanOrderID
    @cSharekhanOrderID.setter
    def Prop05SharekhanOrderID(self,value):self._SharekhanOrderID=value+'\0'*(20-len(value))

    @property
    def cExchangeOrderId(self):return self._ExchangeOrderId
    @cExchangeOrderId.setter
    def Prop06ExchangeOrderId(self,value):self._ExchangeOrderId=value+'\0'*(20-len(value))

    @property
    def cExchangeDateTime(self):return self._ExchangeDateTime
    @cExchangeDateTime.setter
    def Prop07ExchangeDateTime(self,value):self._ExchangeDateTime=value+'\0'*(25-len(value))

    @property
    def cTradeID(self):return self._TradeID
    @cTradeID.setter
    def Prop08TradeID(self,value):self._TradeID=value+'\0'*(20-len(value))

    @property
    def cCustomerId(self):return self._CustomerId
    @cCustomerId.setter
    def Prop09CustomerId(self,value):self._CustomerId=value+'\0'*(10-len(value))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop10ScripToken(self,value):self._ScripToken=value+'\0'*(10-len(value))

    @property
    def cBuySell(self):return self._BuySell
    @cBuySell.setter
    def Prop11BuySell(self,value):self._BuySell=value+'\0'*(10-len(value))

    @property
    def cOrderQty(self):return self._OrderQty
    @cOrderQty.setter
    def Prop12OrderQty(self,value):self._OrderQty=value

    @property
    def cRemainingQty(self):return self._RemainingQty
    @cRemainingQty.setter
    def Prop13RemainingQty(self,value):self._RemainingQty=value

    @property
    def cTradeQty(self):return self._TradeQty
    @cTradeQty.setter
    def Prop14TradeQty(self,value):self._TradeQty=value

    @property
    def cDisclosedQty(self):return self._DisclosedQty
    @cDisclosedQty.setter
    def Prop15DisclosedQty(self,value):self._DisclosedQty=value

    @property
    def cDisclosedRemainingQty(self):return self._DisclosedRemainingQty
    @cDisclosedRemainingQty.setter
    def Prop16DisclosedRemainingQty(self,value):self._DisclosedRemainingQty=value

    @property
    def cOrderPrice(self):return self._OrderPrice
    @cOrderPrice.setter
    def Prop17OrderPrice(self,value):self._OrderPrice=value

    @property
    def cTriggerPrice(self):return self._TriggerPrice
    @cTriggerPrice.setter
    def Prop18TriggerPrice(self,value):self._TriggerPrice=value

    @property
    def cTradePrice(self):return self._TradePrice
    @cTradePrice.setter
    def Prop19TradePrice(self,value):self._TradePrice=value

    @property
    def cExchangeGTD(self):return self._ExchangeGTD
    @cExchangeGTD.setter
    def Prop20ExchangeGTD(self,value):self._ExchangeGTD=value+'\0'*(5-len(value))

    @property
    def cExchangeGTDDate(self):return self._ExchangeGTDDate
    @cExchangeGTDDate.setter
    def Prop21ExchangeGTDDate(self,value):self._ExchangeGTDDate=value+'\0'*(25-len(value))

    @property
    def cChannelCode(self):return self._ChannelCode
    @cChannelCode.setter
    def Prop22ChannelCode(self,value):self._ChannelCode=value+'\0'*(10-len(value))

    @property
    def cChannelUser(self):return self._ChannelUser
    @cChannelUser.setter
    def Prop23ChannelUser(self,value):self._ChannelUser=value+'\0'*(30-len(value))

    @property
    def cErrorMessage(self):return self._ErrorMessage
    @cErrorMessage.setter
    def Prop24ErrorMessage(self,value):self._ErrorMessage=value+'\0'*(250-len(value))

    @property
    def cOrderTrailingPrice(self):return self._OrderTrailingPrice
    @cOrderTrailingPrice.setter
    def Prop25OrderTrailingPrice(self,value):self._OrderTrailingPrice=value

    @property
    def cOrderTargetPrice(self):return self._OrderTargetPrice
    @cOrderTargetPrice.setter
    def Prop26OrderTargetPrice(self,value):self._OrderTargetPrice=value

    @property
    def cUpperPrice(self):return self._UpperPrice
    @cUpperPrice.setter
    def Prop27UpperPrice(self,value):self._UpperPrice=value

    @property
    def cChildSLPrice(self):return self._ChildSLPrice
    @cChildSLPrice.setter
    def Prop28ChildSLPrice(self,value):self._ChildSLPrice=value

    @property
    def cLowerPrice(self):return self._LowerPrice
    @cLowerPrice.setter
    def Prop29LowerPrice(self,value):self._LowerPrice=value

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop30Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def ByteToStruct(self,val):
        cHeader=MessageHeader(1)
        cHeader.ByteToStruct(val[0:6])
        self.Prop01Header=[cHeader.cMessageLength[0],cHeader.Prop02TransactionCode[0]]
        self.Prop02ExchangeCode =struct.pack("B"*len(val[6:8]),*val[6:8]).decode('utf8')
        self.Prop03AckCode =struct.unpack('H',val[8:10])
        self.Prop04MsgLength =struct.unpack('H',val[10:12])
        self.Prop05SharekhanOrderID =struct.pack("B"*len(val[12:32]),*val[12:32]).decode('utf8')
        self.Prop06ExchangeOrderId =struct.pack("B"*len(val[32:52]),*val[32:52]).decode('utf8')
        self.Prop07ExchangeDateTime =struct.pack("B"*len(val[52:77]),*val[52:77]).decode('utf8')
        self.Prop08TradeID =struct.pack("B"*len(val[77:97]),*val[77:97]).decode('utf8')
        self.Prop09CustomerId =struct.pack("B"*len(val[97:107]),*val[97:107]).decode('utf8')
        self.Prop10ScripToken =struct.pack("B"*len(val[107:117]),*val[107:117]).decode('utf8')
        self.Prop11BuySell =struct.pack("B"*len(val[117:127]),*val[117:127]).decode('utf8')
        self.Prop12OrderQty =struct.unpack('I',val[127:131])
        self.Prop13RemainingQty =struct.unpack('I',val[131:135])
        self.Prop14TradeQty =struct.unpack('I',val[135:139])
        self.Prop15DisclosedQty =struct.unpack('I',val[139:143])
        self.Prop16DisclosedRemainingQty=struct.unpack('I',val[143:147])
        self.Prop17OrderPrice =struct.unpack('I',val[147:151])
        self.Prop18TriggerPrice =struct.unpack('I',val[151:155])
        self.Prop19TradePrice =struct.unpack('I',val[155:159])
        self.Prop20ExchangeGTD =struct.pack("B"*len(val[159:164]),*val[159:164]).decode('utf8')
        self.Prop21ExchangeGTDDate =struct.pack("B"*len(val[164:189]),*val[164:189]).decode('utf8')
        self.Prop22ChannelCode =struct.pack("B"*len(val[189:199]),*val[189:199]).decode('utf8')
        self.Prop23ChannelUser =struct.pack("B"*len(val[199:229]),*val[199:229]).decode('utf8')
        self.Prop24ErrorMessage =struct.pack("B"*len(val[229:479]),*val[229:479]).decode('utf8')
        self.Prop25OrderTrailingPrice=struct.unpack('I',val[479:483])
        self.Prop26OrderTargetPrice =struct.unpack('I',val[483:487])
        self.Prop27UpperPrice =struct.unpack('I',val[487:491])
        self.Prop28ChildSLPrice =struct.unpack('I',val[491:495])
        self.Prop29LowerPrice =struct.unpack('I',val[495:499])
        self.Prop30Reserved =struct.pack("B"*len(val[499:599]),*val[499:599]).decode('utf8')

    def ToString(self):
        return (Prop01Header.ToString() + "|" + "ExchangeCode  = " + self.cExchangeCode + "|" + "AckCode   = " + self.cAckCode + "|" + "MsgLength  = " + self.cMsgLength + "|" + "SharekhanOrderID = " + self.cSharekhanOrderID + "|" + "ExchangeOrderId  = " + self.cExchangeOrderId + "|" + "ExchangeDateTime = " + self.cExchangeDateTime + "|" + "TradeID  = " + self.cTradeID
                    + "|" + "CustomerId  = " + self.cCustomerId + "|" + "ScripToken  = " + self.cScripToken + "|" + "BuySell   = " + self.cBuySell + "|" + "OrderQty  = "
                    + self.cOrderQty + "|" + "RemainingQty  = " + self.cRemainingQty + "|" + "TradeQty  = " + self.cTradeQty + "|" + "DisclosedQty  = " + self.cDisclosedQty + "|" + "DisclosedRemainingQty  = " + self.cDisclosedRemainingQty + "|" + "OrderPrice  = " + self.cOrderPrice + "|" + "TriggerPrice  = " + self.cTriggerPrice + "|" + "TradePrice  = " + self.cTradePrice + "|" + "ExchangeGTD  = " + self.cExchangeGTD + "|" + "ExchangeGTDDate  = " + self.cExchangeGTDDate + "|" + "ChannelCode = "
                    + self.cChannelCode + "|" + "ChannelUser  = " + self.cChannelUser + "|" + "ErrorMessage  = " + self.cErrorMessage + "|" + "OrderTrailingPrice  = " + self.cOrderTrailingPrice + "|" + "OrderTargetPrice  = " + self.cOrderTargetPrice + "UpperPrice = " + self.cUpperPrice + "|" + "ChildSLPrice  = " + self.cChildSLPrice + "|" + "LowerPrice  = " + self.cLowerPrice + "|" + "Reserved  = " + self.cReserved)

class ReportRequest():
    def __init__(self,transcode):
        self._Header =None
        self._LoginID = None
        self._CustomerID = None
        self._DateTime = None
        self._ScripCode =None
        self._OrderId = None
        self._Reserved =None

    @property
    def cHeader(self):
        return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cLoginID(self):return self._LoginID
    @cLoginID.setter
    def Prop02LoginID(self,value):self._LoginID=value+'\0'*(20-len(value))

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop03CustomerID(self,value):self._CustomerID=value+'\0'*(10-len(value))

    @property
    def cDateTime(self):return self._DateTime
    @cDateTime.setter
    def Prop04DateTime(self,value):self._DateTime=value+'\0'*(25-len(value))

    @property
    def cScripCode(self):return self._ScripCode
    @cScripCode.setter
    def Prop05ScripCode(self,value):self._ScripCode=value+'\0'*(10 -len(value))

    @property
    def cOrderId(self):return self._OrderId
    @cOrderId.setter
    def Prop06OrderId(self,value):self._OrderId=value+'\0'*(10-len(value))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop07Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def StructToByte(self):
        try:
            ReportRequest=array('B')
            for c in self.cHeader:ReportRequest.append(c)
            for c in self.cLoginID:ReportRequest.append(ord(c))
            for c in self.cCustomerID:ReportRequest.append(ord(c))
            for c in self.cDateTime:ReportRequest.append(ord(c))
            for c in self.cScripCode:ReportRequest.append(ord(c))
            for c in self.cOrderId:ReportRequest.append(ord(c))
            for c in self.cReserved:ReportRequest.append(ord(c))
            return ReportRequest
        except:
            logger.exception(PrintException())

    def ToString(self):
        return (MessageHeader.ToString(self.cHeader) + "|" + "LoginID = " + self.cLoginID + "|" + "CustomerID = " + self.cCustomerID + "|" + "DateTime = " + self.cDateTime + "|" + "ScripCode = " + self.cScripCode + "|" + "OrderId = " + self.cOrderId + "|" + "Reserved = " + self.cReserved)

class ReportResponse():
    def __init__(self,tranCode):
        self._Header = None
        self._RecordCount =0
        self._Reserved = None

    @property
    def cHeader(self):
        return self._Header
    @cHeader.setter
    def Prop01Header(self,value):
        val1=struct.pack('I',value[0])
        val2=struct.pack('H',value[1])
        self._Header=struct.unpack('B'*4,val1)+struct.unpack('B'*2,val2)

    @property
    def cRecordCount(self):return self._RecordCount
    @cRecordCount.setter
    def Prop02RecordCount(self,value):self._RecordCount=value

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop03Reserved(self,value):self._Reserved=value+'\0'*(100-len(value))

    def ByteToStruct(self,val):
        try:
            cHeader=MessageHeader(1)
            cHeader.ByteToStruct(val[0:6])
            self.Prop01Header=[cHeader.cMessageLength[0],cHeader.Prop02TransactionCode[0]]
            self.Prop02RecordCount=struct.unpack('I',val[6:10])
            self.Prop03Reserved=struct.pack("B"*len(val[10:100]),*val[10:100]).decode( errors='ignore')
        except:
            logger.exception(PrintException())

    def ToString(self):
        try:
            return ("".join([" Header :" , MessageHeader.ToString(self.cHeader)  , "|" ,"Record Count : " , str(self.cRecordCount) , "|" , "ReportItem  ", " ", "|", "Reserved : ",str(self.cReserved)]))
        except:
            logger.exception(PrintException())

class EquityOrderReportItem():
    def __init__(self,transCode):
        self._DataLength=0
        self._ExchangeCode=None
        self._OrderStatus=None
        self._OrderID=None
        self._ExchangeOrderID=None
        self._ExchangeAckDateTime=None
        self._CustomerID=None
        self._S2KID=None
        self._ScripToken=None
        self._BuySell=None
        self._OrderQty=0
        self._DisclosedQuantity=0
        self._ExecutedQuantity=0
        self._OrderPrice=0
        self._ExecutedPrice=0
        self._TriggerPrice=0
        self._RequestStatus=None
        self._DateTime=None
        self._AfterHour=None
        self._RMScode=None
        self._GoodTill=None
        self._GoodTillDate=None
        self._ChannelCode=None
        self._ChannelUser=None
        self._OrderTrailingPrice=0
        self._OrderTargetPrice=0
        self._UpperPrice=0
        self._LowerPrice=0
        self._BracketSLPrice=0
        self._Order_Type=None
        self._TrailingStatus=None
        self._CoverOrderID=None
        self._UpperLowerFlag=None
        self._Reserved=None

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,val):self._ExchangeCode=val+'\0'*(2-len(val))

    @property
    def cOrderStatus(self):return self._OrderStatus
    @cOrderStatus.setter
    def Prop03OrderStatus(self,val):self._OrderStatus=val+'\0'*(20-len(val))

    @property
    def cOrderID(self):return self._OrderID
    @cOrderID.setter
    def Prop04OrderID(self,val):self._OrderID=val+'\0'*(20-len(val))

    @property
    def cExchangeOrderID(self):return self._ExchangeOrderID
    @cExchangeOrderID.setter
    def Prop05ExchangeOrderID(self,val):self._ExchangeOrderID=val+'\0'*(20-len(val))

    @property
    def cExchangeAckDateTime(self):return self._ExchangeAckDateTime
    @cExchangeAckDateTime.setter
    def Prop06ExchangeAckDateTime(self,val):self._ExchangeAckDateTime=val+'\0'*(25-len(val))

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop07CustomerID(self,val):self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cS2KID(self):return self._S2KID
    @cS2KID.setter
    def Prop08S2KID(self,val):self._S2KID=val+'\0'*(10-len(val))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop09ScripToken(self,val):self._ScripToken=val+'\0'*(10-len(val))

    @property
    def cBuySell(self):return self._BuySell
    @cBuySell.setter
    def Prop10BuySell(self,val):self._BuySell=val+'\0'*(2-len(val))

    @property
    def cOrderQty(self):return self._OrderQty
    @cOrderQty.setter
    def Prop11OrderQty(self,val):self._OrderQty=val

    @property
    def cDisclosedQuantity(self):return self._DisclosedQuantity
    @cDisclosedQuantity.setter
    def Prop12DisclosedQuantity(self,val):self._DisclosedQuantity=val

    @property
    def cExecutedQuantity(self):return self._ExecutedQuantity
    @cExecutedQuantity.setter
    def Prop13ExecutedQuantity(self,val):self._ExecutedQuantity=val

    @property
    def cOrderPrice(self):return self._OrderPrice
    @cOrderPrice.setter
    def Prop14OrderPrice(self,val):self._OrderPrice=val

    @property
    def cExecutedPrice(self):return self._ExecutedPrice
    @cExecutedPrice.setter
    def Prop15ExecutedPrice(self,val):self._ExecutedPrice=val

    @property
    def cTriggerPrice(self):return self._TriggerPrice
    @cTriggerPrice.setter
    def Prop16TriggerPrice(self,val):self._TriggerPrice=val

    @property
    def cRequestStatus(self):return self._RequestStatus
    @cRequestStatus.setter
    def Prop17RequestStatus(self,val):self._RequestStatus=val+'\0'*(15-len(val))

    @property
    def cDateTime(self):return self._DateTime
    @cDateTime.setter
    def Prop18DateTime(self,val):self._DateTime=val+'\0'*(25-len(val))

    @property
    def cAfterHour(self):return self._AfterHour
    @cAfterHour.setter
    def Prop19AfterHour(self,val):self._AfterHour=val+'\0'*(1-len(val))

    @property
    def cRMScode(self):return self._RMScode
    @cRMScode.setter
    def Prop20RMScode(self,val):self._RMScode=val+'\0'*(15-len(val))

    @property
    def cGoodTill(self):return self._GoodTill
    @cGoodTill.setter
    def Prop21GoodTill(self,val):self._GoodTill=val+'\0'*(5-len(val))

    @property
    def cGoodTillDate(self):return self._GoodTillDate
    @cGoodTillDate.setter
    def Prop22GoodTillDate(self,val):self._GoodTillDate=val+'\0'*(25-len(val))

    @property
    def cChannelCode(self):return self._ChannelCode
    @cChannelCode.setter
    def Prop23ChannelCode(self,val):self._ChannelCode=val+'\0'*(10-len(val))

    @property
    def cChannelUser(self):return self._ChannelUser
    @cChannelUser.setter
    def Prop24ChannelUser(self,val):self._ChannelUser=val+'\0'*(20-len(val))

    @property
    def cOrderTrailingPrice(self):return self._OrderTrailingPrice
    @cOrderTrailingPrice.setter
    def Prop25OrderTrailingPrice(self,val):self._OrderTrailingPrice=val

    @property
    def cOrderTargetPrice(self):return self._OrderTargetPrice
    @cOrderTargetPrice.setter
    def Prop26OrderTargetPrice(self,val):self._OrderTargetPrice=val

    @property
    def cUpperPrice(self):return self._UpperPrice
    @cUpperPrice.setter
    def Prop27UpperPrice(self,val):self._UpperPrice=val

    @property
    def cLowerPrice(self):return self._LowerPrice
    @cLowerPrice.setter
    def Prop28LowerPrice(self,val):self._LowerPrice=val

    @property
    def cBracketSLPrice(self):return self._BracketSLPrice
    @cBracketSLPrice.setter
    def Prop29BracketSLPrice(self,val):self._BracketSLPrice=val

    @property
    def cOrder_Type(self):return self._Order_Type
    @cOrder_Type.setter
    def Prop30Order_Type(self,val):self._Order_Type=val+'\0'*(25-len(val))

    @property
    def cTrailingStatus(self):return self._TrailingStatus
    @cTrailingStatus.setter
    def Prop31TrailingStatus(self,val):self._TrailingStatus=val+'\0'*(25-len(val))

    @property
    def cCoverOrderID(self):return self._CoverOrderID
    @cCoverOrderID.setter
    def Prop32CoverOrderID(self,val):self._CoverOrderID=val+'\0'*(25-len(val))

    @property
    def cUpperLowerFlag(self):return self._UpperLowerFlag
    @cUpperLowerFlag.setter
    def Prop33UpperLowerFlag(self,val):self._UpperLowerFlag=val+'\0'*(1-len(val))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop34Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))

    def ByteToStruct(self,val):
        try:
            self.Prop01DataLenght=struct.unpack('I',val[10:14])
            self.Prop02ExchangeCode=struct.pack("B"*len(val[14:16]),*val[14:16]).decode('utf8')
            self.Prop03OrderStatus=struct.pack("B"*len(val[16:36]),*val[16:36]).decode(errors='ignore')
            self.Prop04OrderID=struct.pack("B"*len(val[36:56]),*val[36:56]).decode('utf8')
            self.Prop05ExchangeOrderID=struct.pack("B"*len(val[56:76]),*val[56:76]).decode('utf8')
            self.Prop06ExchangeAckDateTime=struct.pack("B"*len(val[76:101]),*val[76:101]).decode('utf8')
            self.Prop07CustomerID=struct.pack("B"*len(val[101:111]),*val[101:111]).decode('utf8')
            self.Prop08S2KID=struct.pack("B"*len(val[111:121]),*val[111:121]).decode('utf8')
            self.Prop09ScripToken=struct.pack("B"*len(val[121:131]),*val[121:131]).decode('utf8')
            self.Prop10BuySell=struct.pack("B"*len(val[131:133]),*val[131:133]).decode('utf8')
            self.Prop11OrderQty=struct.unpack('I',val[133:137])
            self.Prop12DisclosedQuantity=struct.unpack('I',val[137:141])
            self.Prop13ExecutedQuantity=struct.unpack('I',val[141:145])
            self.Prop14OrderPrice=struct.unpack('I',val[145:149])
            self.Prop15ExecutedPrice=struct.unpack('I',val[149:153])
            self.Prop16TriggerPrice=struct.unpack('I',val[153:157])
            self.Prop17RequestStatus=struct.pack("B"*len(val[157:172]),*val[157:172]).decode('utf8')
            self.Prop18DateTime=struct.pack("B"*len(val[172:197]),*val[172:197]).decode('utf8')
            self.Prop19AfterHour=struct.pack("B"*len(val[197:198]),*val[197:198]).decode('utf8')
            self.Prop20RMScode=struct.pack("B"*len(val[198:213]),*val[198:213]).decode('utf8')
            self.Prop21GoodTill=struct.pack("B"*len(val[213:218]),*val[213:218]).decode('utf8')
            self.Prop22GoodTillDate=struct.pack("B"*len(val[218:243]),*val[218:243]).decode('utf8')
            self.Prop23ChannelCode=struct.pack("B"*len(val[243:253]),*val[243:253]).decode('utf8')
            self.Prop24ChannelUser=struct.pack("B"*len(val[253:273]),*val[253:273]).decode('utf8')
            self.Prop25OrderTrailingPrice=struct.unpack('I',val[273:277])
            self.Prop26OrderTargetPrice=struct.unpack('I',val[277:281])
            self.Prop27UpperPrice=struct.unpack('I',val[281:285])
            self.Prop28LowerPrice=struct.unpack('I',val[285:289])
            self.Prop29BracketSLPrice=struct.unpack('I',val[289:293])
            self.Prop30Order_Type=struct.pack("B"*len(val[293:318]),*val[293:318]).decode('utf8')
            self.Prop31TrailingStatus=struct.pack("B"*len(val[318:343]),*val[318:343]).decode('utf8')
            self.Prop32CoverOrderID=struct.pack("B"*len(val[343:368]),*val[343:368]).decode('utf8')
            self.Prop33UpperLowerFlag=struct.pack("B"*len(val[368:369]),*val[368:369]).decode('utf8')
            self.Prop34Reserved=struct.pack("B"*len(val[369:469]),*val[369:469]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        return ('DataLength = '+str(self.cDataLength) + "|" + 'ExchangeCode =  '+self.cExchangeCode + "|" +'OrderStatus = '+self.cOrderStatus + "|"
                +'OrderID = '+self.cOrderID + "|" +'ExchangeOrderID = ' +self.cExchangeOrderID + "|" +'ExchangeAckDateTime = '+self.cExchangeAckDateTime + "|"
                + 'CustomerID= '+self.cCustomerID + "|" +'S2KID = '+ self.cS2KID + "|" + 'ScripToken = '+self.cScripToken + "|" +'BuySell = '+ self.cBuySell + "|"
                + 'OrderQty = '+str(self.cOrderQty) + "|"+'OrderDisclosedQty = '+str(self.cDisclosedQuantity) + "|" +'OrderExecutedQty ='+ str(self.cExecutedQuantity)+ "|"
                + 'OrderPrice = '+str(self.cOrderPrice) + "|" + 'OrderExecutedPrice = '+str(self.cExecutedPrice) + "|" +'OrderTriggerPrice = '+ str(self.cTriggerPrice) + "|"
                + 'RequestStatus = '+self.cRequestStatus + "|" +'OrderDateTime = '+ self.cDateTime + "|" + 'AfterHour = '+self.cAfterHour + "|" +'RMSCode = '+ self.cRMScode + "|"
                +'GoodTill = '+ self.cGoodTill + "|" +' GoodTillDate = '+ self.cGoodTillDate + "|" + ' ChannelCode = '+self.cChannelCode + "|"
                + 'ChannelUser = '+self.cChannelUser + "|" +'OrderTrailingPrice = '+ str(self.cOrderTrailingPrice)
                + "|" +'OrderTargetPrice = '+ str(self.cOrderTargetPrice)+ "|" + 'UpperPrice = '+str(self.cUpperPrice) + "|"
                + 'LowerPrice = '+str(self.cLowerPrice) + "|" + 'BracketSLPrice = '+str(self.cBracketSLPrice) + "|" +'Order_Type = '+ self.cOrder_Type + "|"
                + 'TrailingStatus = '+self.cTrailingStatus + "|" + 'CoverOrderID = '+ self.cCoverOrderID + "|" + 'UpperLowerFlag = '+self.cUpperLowerFlag + "|" + 'Reserved = '+self.cReserved)

# DataLength=459|TransCode=123| ExchangeCode = NC|OrderStatus = FullyExecuted|OrderID = 243520884|ExchangeOrderID = 2011112800000001|ExchangeAckDateTime =|TradeID =|CustomerID = 123456|S2KID = W78089|ScripToken = 10634|BuySell = B|OrderQty = 1|OrderDisclosedQty = 0|OrderExecutedQty = 1|OrderPrice = 4345|OrderExecutedPrice = 4205|OrderTriggerPrice = 0|RequestStatus = NEW|OrderDateTime = 2011-11-28 11:04:33.0|AfterHour = N|RMSCode = SKSIMNSE1|GoodTill = GFD|GoodTillDate =|ChannelCode = PWR_TRD|ChannelUser = SIDPOWERB|OrderTrailingPrice = 0|OrderTargetPrice = 0|UpperPrice = 0|LowerPrice = 0|BracketSLPrice = 0|Order_Type = NOR|TrailingStatus =|CoverOrderID = 0|UpperLowerFlag = 0 | Reserved =
class DerivativeOrderReportItem():
    def __init__(self,transCode):
        self._DataLength=0
        self._ExchangeCode=None
        self._OrderStatus=None
        self._OrderID=None
        self._ExchangeOrderID=None
        self._CustomerID=None
        self._S2KID=None
        self._ScripToken=None
        self._OrderType=None
        self._BuySell=None
        self._OrderQty=0
        self._ExecutedQuantity=0
        self._OrderPrice=0
        self._AveragePrice=0
        self._DateTime=None
        self._RequestStatus=None
        self._ChannelCode=None
        self._ChannelUser=None
        self._LastModTime=None
        self._OpenQty=0
        self._POI=None
        self._DisclosedQuantity=0
        self._MIF=None
        self._TriggerPrice=0
        self._RMScode=None
        self._AfterHour=None
        self._GoodTill=None
        self._GoodTillDate=None
        self._UpdateDate=None
        self._UpdateUser=None
        self._CALevel=None
        self._AON=None
        self._OPOC=None
        self._FnoOrderType=None
        self._BuySellFlag=None
        self._Reserved=None

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,val):self._ExchangeCode=val+'\0'*(2-len(val))

    @property
    def cOrderStatus(self):return self._OrderStatus
    @cOrderStatus.setter
    def Prop03OrderStatus(self,val):self._OrderStatus=val+'\0'*(20-len(val))

    @property
    def cOrderID(self):return self._OrderID
    @cOrderID.setter
    def Prop04OrderID(self,val):self._OrderID=val+'\0'*(20-len(val))

    @property
    def cExchangeOrderID(self):return self._ExchangeOrderID
    @cExchangeOrderID.setter
    def Prop05ExchangeOrderID(self,val):self._ExchangeOrderID=val+'\0'*(25-len(val))

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop06CustomerID(self,val):self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cS2KID(self):return self._S2KID
    @cS2KID.setter
    def Prop07S2KID(self,val):self._S2KID=val+'\0'*(25-len(val))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop08ScripToken(self,val):self._ScripToken=val+'\0'*(10-len(val))

    @property
    def cOrderType(self):return self._OrderType
    @cOrderType.setter
    def Prop09OrderType(self,val):self._OrderType=val+'\0'*(10-len(val))

    @property
    def cBuySell(self):return self._BuySell
    @cBuySell.setter
    def Prop10BuySell(self,val):self._BuySell=val+'\0'*(2-len(val))

    @property
    def cOrderQty(self):return self._OrderQty
    @cOrderQty.setter
    def Prop11OrderQty(self,val):self._OrderQty=val

    @property
    def cExecutedQuantity(self):return self._ExecutedQuantity
    @cExecutedQuantity.setter
    def Prop12ExecutedQuantity(self,val):self._ExecutedQuantity=val

    @property
    def cOrderPrice(self):return self._OrderPrice
    @cOrderPrice.setter
    def Prop13OrderPrice(self,val):self._OrderPrice=val

    @property
    def cAveragePrice(self):return self._AveragePrice
    @cAveragePrice.setter
    def Prop14AveragePrice(self,val):self._AveragePrice=val

    @property
    def cDateTime(self):return self._DateTime
    @cDateTime.setter
    def Prop15DateTime(self,val):self._DateTime=val+'\0'*(25-len(val))

    @property
    def cRequestStatus(self):return self._RequestStatus
    @cRequestStatus.setter
    def Prop16RequestStatus(self,val):self._RequestStatus=val+'\0'*(15-len(val))

    @property
    def cChannelCode(self):return self._ChannelCode
    @cChannelCode.setter
    def Prop17ChannelCode(self,val):self._ChannelCode=val+'\0'*(10-len(val))

    @property
    def cChannelUser(self):return self._ChannelUser
    @cChannelUser.setter
    def Prop18ChannelUser(self,val):self._ChannelUser=val+'\0'*(20-len(val))

    @property
    def cLastModTime(self):return self._LastModTime
    @cLastModTime.setter
    def Prop19LastModTime(self,val):self._LastModTime=val+'\0'*(25-len(val))

    @property
    def cOpenQty(self):return self._OpenQty
    @cOpenQty.setter
    def Prop20OpenQty(self,val):self._OpenQty=val

    @property
    def cPOI(self):return self._POI
    @cPOI.setter
    def Prop21POI(self,val):self._POI=val+'\0'*(25-len(val))

    @property
    def cDisclosedQuantity(self):return self._cDisclosedQuantity
    @cDisclosedQuantity.setter
    def Prop22DisclosedQuantity(self,val):self._cDisclosedQuantity=val

    @property
    def cMIF(self):return self._MIF
    @cMIF.setter
    def Prop23MIF(self,val):self._MIF=val+'\0'*(50-len(val))

    @property
    def cTriggerPrice(self):return self._TriggerPrice
    @cTriggerPrice.setter
    def Prop24TriggerPrice(self,val):self._TriggerPrice=val

    @property
    def cRMScode(self):return self._RMScode
    @cRMScode.setter
    def Prop25RMScode(self,val):self._RMScode=val+'\0'*(15-len(val))

    @property
    def cAfterHour(self):return self._AfterHour
    @cAfterHour.setter
    def Prop26AfterHour(self,val):self._AfterHour=val+'\0'*(1-len(val))

    @property
    def cGoodTill(self):return self._GoodTill
    @cGoodTill.setter
    def Prop27GoodTill(self,val):self._GoodTill=val+'\0'*(5-len(val))

    @property
    def cGoodTillDate(self):return self._GoodTillDate
    @cGoodTillDate.setter
    def Prop28GoodTillDate(self,val):self._GoodTillDate=val+'\0'*(25-len(val))

    @property
    def cUpdateDate(self):return self._UpdateDate
    @cUpdateDate.setter
    def Prop29UpdateDate(self,val):self._UpdateDate=val+'\0'*(25-len(val))

    @property
    def cUpdateUser(self):return self._UpdateUser
    @cUpdateUser.setter
    def Prop30UpdateUser(self,val):self._UpdateUser=val+'\0'*(25-len(val))

    @property
    def cCALevel(self):return self._cCALevel
    @cCALevel.setter
    def Prop31CALevel(self,val):self._cCALevel=val+'\0'*(15-len(val))

    @property
    def cAON(self):return self._AON
    @cAON.setter
    def Prop32AON(self,val):self._AON=val+'\0'*(25-len(val))

    @property
    def cOPOC(self):return self._OPOC
    @cOPOC.setter
    def Prop33OPOC(self,val):self._OPOC=val+'\0'*(25-len(val))

    @property
    def cFnoOrderType(self):return self._FnoOrderType
    @cFnoOrderType.setter
    def Prop34FnoOrderType(self,val):self._FnoOrderType=val+'\0'*(25-len(val))

    @property
    def cBuySellFlag(self):return self._BuySellFlag
    @cBuySellFlag.setter
    def Prop35BuySellFlag(self,val):self._BuySellFlag=val+'\0'*(1-len(val))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop36Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))



    def ByteToStruct(self,val):
        try:
            self.Prop01DataLenght=struct.unpack('I',val[10:14])
            self.Prop02ExchangeCode=struct.pack("B"*len(val[14:16]),*val[14:16]).decode('utf8')
            self.Prop03OrderStatus=struct.pack("B"*len(val[16:36]),*val[16:36]).decode('utf8')
            self.Prop04OrderID=struct.pack("B"*len(val[36:56]),*val[36:56]).decode('utf8')
            self.Prop05ExchangeOrderID=struct.pack("B"*len(val[56:81]),*val[56:81]).decode('utf8')
            self.Prop06CustomerID=struct.pack("B"*len(val[81:91]),*val[81:91]).decode('utf8')
            self.Prop07S2KID=struct.pack("B"*len(val[91:116]),*val[91:116]).decode('utf8')
            self.Prop08ScripToken=struct.pack("B"*len(val[116:126]),*val[116:126]).decode('utf8')
            self.Prop09OrderType=struct.pack("B"*len(val[126:136]),*val[126:136]).decode('utf8')
            self.Prop10BuySell=struct.pack("B"*len(val[136:138]),*val[136:138]).decode('utf8')
            self.Prop11OrderQty=struct.unpack('I',val[138:142])
            self.Prop12ExecutedQuantity=struct.unpack('I',val[142:146])
            self.Prop13OrderPrice=struct.unpack('I',val[146:150])
            self.Prop14AveragePrice=struct.unpack('I',val[150:154])
            self.Prop15DateTime=struct.pack("B"*len(val[154:179]),*val[154:179]).decode('utf8')
            self.Prop16RequestStatus=struct.pack("B"*len(val[179:194]),*val[179:194]).decode('utf8')
            self.Prop17ChannelCode=struct.pack("B"*len(val[194:204]),*val[194:204]).decode('utf8')
            self.Prop18ChannelUser=struct.pack("B"*len(val[204:224]),*val[204:224]).decode('utf8')
            self.Prop19LastModTime=struct.pack("B"*len(val[224:249]),*val[224:249]).decode('utf8')
            self.Prop20OpenQty=struct.unpack('I',val[249:253])
            self.Prop21POI=struct.pack("B"*len(val[253:278]),*val[253:278]).decode('utf8')
            self.Prop22DisclosedQuantity=struct.unpack('I',val[278:282])
            self.Prop23MIF=struct.pack("B"*len(val[282:332]),*val[282:332]).decode('utf8')
            self.Prop24TriggerPrice=struct.unpack('I',val[332:336])
            self.Prop25RMScode=struct.pack("B"*len(val[336:351]),*val[336:351]).decode('utf8')
            self.Prop26AfterHour=struct.pack("B"*len(val[351:352]),*val[351:352]).decode('utf8')
            self.Prop27GoodTill=struct.pack("B"*len(val[352:357]),*val[352:357]).decode('utf8')
            self.Prop28GoodTillDate=struct.pack("B"*len(val[357:382]),*val[357:382]).decode('utf8')
            self.Prop29UpdateDate=struct.pack("B"*len(val[382:407]),*val[382:407]).decode('utf8')
            self.Prop30UpdateUser=struct.pack("B"*len(val[407:432]),*val[407:432]).decode('utf8')
            self.Prop31CALevel=struct.pack("B"*len(val[432:447]),*val[432:447]).decode('utf8')
            self.Prop32AON=struct.pack("B"*len(val[447:472]),*val[447:472]).decode('utf8')
            self.Prop33OPOC=struct.pack("B"*len(val[472:497]),*val[472:497]).decode('utf8')
            self.Prop34FnoOrderType=struct.pack("B"*len(val[497:522]),*val[497:522]).decode('utf8')
            self.Prop35BuySellFlag=struct.pack("B"*len(val[522:523]),*val[522:523]).decode('utf8')
            self.Prop36Reserved=struct.pack("B"*len(val[523:623]),*val[523:623]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
         return ('DataLength= '+str(self.cDataLength) + "|" +'Exchange= '+str(self.cExchangeCode) + "|" + 'OrderStatus= '+str(self.cOrderStatus) + "|" + 'OrderID= '+str(self.cOrderID) + "|" +'ExchangeOrderID= '+ str(self.cExchangeOrderID) + "|" + 'CustomerID= '+str(self.cCustomerID) + "|" + 'S2KID = '+str(self.cS2KID) + "|" + 'ScripToken = '+str(self.cScripToken) + "|" +'OrderType = '+ str(self.cOrderType) + "|" +'BuySell = '+ str(self.cBuySell)
                    + "|" + 'OrderQty = '+str(self.cOrderQty) + "|" +'OrderExecutedQty = '+ str(self.cExecutedQuantity) + "|" + 'OrderPrice = '+str(self.cOrderPrice) + "|" + 'AveragePrice = '+str(self.cAveragePrice) + "|" +'OrderDateTime = '+ str(self.cDateTime) + "|" +'RequestStatus = '+ str(self.cRequestStatus) + "|" +'ChannelCode = '+ str(self.cChannelCode) + "|" + 'ChannelUser = '+str(self.cChannelUser) + "|" +'LastModTime = '+ str(self.cLastModTime)
                + "|" +'OpenQty = '+ str(self.cOpenQty) + "|" +'POI = '+ str(self.cPOI) + "|" + 'DisclosedQty = '+str(self.cDisclosedQuantity) + "|" +'MIF = '+ str(self.cMIF) + "|" + 'OrderTriggerPrice = '+str(self.cTriggerPrice) + "|" + 'RMSCode = '+str(self.cRMScode) + "|" +'AfterHour = '+ str(self.cAfterHour) + "|" + 'GoodTill = '+str(self.cGoodTill) + "|" +'GoodTillDate = '+ str(self.cGoodTillDate) + "|" + 'UpdateDate = '+str(self.cUpdateDate) + "|" + 'UpdateUser = '+str(self.cUpdateUser)
                + "|" +'CALevel = '+ str(self.cCALevel) + "|" +'AON = '+ str(self.cAON) + "|" +'OPOC = '+ str(self.cOPOC) + "|" + 'FnoOrderType = '+str(self.cFnoOrderType) + "|" + 'BuySellFlag = '+str(self.cBuySellFlag) + "|" + 'Reserved = '+str(self.cReserved) + "\n")

class DPSRReportItem():
    def __init__(self,tranCode):
        self._DataLength=0
        self._Exchange=None
        self._CustomerID=None
        self._S2KID=None
        self._ScripToken=None
        self._Receivable=0
        self._DpMarginQty=0
        self._DP=0
        self._Pool=0
        self._MF=0
        self._Pledge=0
        self._InvstQty=0
        self._MarginQty=0
        self._AvailableQty=0
        self._HoldPrice=0
        self._MktPrice=0
        self._MktValue=0
        self._DpMarginValue=0
        self._Reserved=None

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cExchange(self):return self._Exchange
    @cExchange.setter
    def Prop02Exchange(self,val):self._Exchange=val+'\0'*(2-len(val))

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop03CustomerID(self,val):self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cS2KID(self):return self._S2KID
    @cS2KID.setter
    def Prop04S2KID(self,val):self._S2KID=val+'\0'*(10-len(val))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop05ScripToken(self,val):self._ScripToken=val+'\0'*(10-len(val))

    @property
    def cReceivable(self):return self._Receivable
    @cReceivable.setter
    def Prop06Receivable(self,val):self._Receivable=val

    @property
    def cDpMarginQty(self):return self._DpMarginQty
    @cDpMarginQty.setter
    def Prop07DpMarginQty(self,val):self._DpMarginQty=val

    @property
    def cDP(self):return self._DP
    @cDP.setter
    def Prop08DP(self,val):self._DP=val

    @property
    def cPool(self):return self._Pool
    @cPool.setter
    def Prop09Pool(self,val):self._Pool=val

    @property
    def cMF(self):return self._MF
    @cMF.setter
    def Prop10cMF(self,val):self._MF=val

    @property
    def cPledge(self):return self._Pledge
    @cPledge.setter
    def Prop11Pledge(self,val):self._Pledge=val

    @property
    def cInvstQty(self):return self._InvstQty
    @cInvstQty.setter
    def Prop12InvstQty(self,val):self._InvstQty=val

    @property
    def cMarginQty(self):return self._MarginQty
    @cMarginQty.setter
    def Prop13MarginQty(self,val):self._MarginQty=val

    @property
    def cAvailableQty(self):return self._AvailableQty
    @cAvailableQty.setter
    def Prop14AvailableQty(self,val):self._AvailableQty=val

    @property
    def cHoldPrice(self):return self._HoldPrice
    @cHoldPrice.setter
    def Prop15HoldPrice(self,val):self._HoldPrice=val

    @property
    def cMktPrice(self):return self._MktPrice
    @cMktPrice.setter
    def Prop16MktPrice(self,val):self._MktPrice=val

    @property
    def cMktValue(self):return self._MktValue
    @cMktValue.setter
    def Prop17MktValue(self,val):self._MktValue=val

    @property
    def cDpMarginValue(self):return self._DpMarginValue
    @cDpMarginValue.setter
    def Prop18cDpMarginValue(self,val):self._DpMarginValue=val

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop19Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))


    def ByteToStruct(self,val):
        self.Prop01DataLenght=struct.unpack('I',val[0:4])
        self.Prop02Exchange=struct.pack("B"*len(val[4:6]),*val[4:6]).decode('utf8')
        self.Prop03CustomerID=struct.pack("B"*len(val[6:16]),*val[6:16]).decode('utf8')
        self.Prop04S2KID=struct.pack("B"*len(val[16:26]),*val[16:26]).decode('utf8')
        self.Prop05ScripToken=struct.pack("B"*len(val[26:36]),*val[26:36]).decode('utf8')
        self.Prop06Receivable=struct.unpack('I',val[36:40])
        self.Prop07DpMarginQty=struct.unpack('I',val[40:44])
        self.Prop08DP=struct.unpack('I',val[44:48])
        self.Prop09Pool=struct.unpack('I',val[48:52])
        self.Prop10cMF=struct.unpack('I',val[52:56])
        self.Prop11Pledge=struct.unpack('I',val[56:60])
        self.Prop12InvstQty=struct.unpack('I',val[60:64])
        self.Prop13MarginQty=struct.unpack('I',val[64:68])
        self.Prop14AvailableQty=struct.unpack('I',val[68:72])
        self.Prop15HoldPrice=struct.unpack('I',val[72:76])
        self.Prop16MktPrice=struct.unpack('I',val[76:80])
        self.Prop17MktValue=struct.unpack('I',val[80:84])
        self.Prop18cDpMarginValue=struct.unpack('i',val[84:88])
        self.Prop19Reserved=struct.pack("B"*len(val[88:108]),*val[88:108]).decode('utf8')

class CashNetPositionReportItem():
    def __init__(self,tranCode):
        self._DataLength=0
        self._Exchange=None
        self._ScripName=None
        self._ScripToken=None
        self._Segment=None
        self._ProductType=None
        self._NetPosition=0
        self._AVGRate=0
        self._MKTRate=0
        self._MTMP=0
        self._BookedPL=0
        self._BuyQty=0
        self._AVGBuyRate=0
        self._BuyValue=0
        self._SellQty=0
        self._AVGSellRate=0
        self._SellValue=0
        self._DPQty=0
        self._Reserved=0

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cExchange(self):return self._Exchange
    @cExchange.setter
    def Prop02Exchange(self,val):self._Exchange=val+'\0'*(2-len(val))

    @property
    def cScripName(self):return self._ScripName
    @cScripName.setter
    def Prop03ScripName(self,val):self._ScripName=val+'\0'*(100-len(val))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop04ScripToken(self,val):self._ScripToken=val+'\0'*(10-len(val))

    @property
    def cSegment(self):return self._Segment
    @cSegment.setter
    def Prop05Segment(self,val):self._Segment=val+'\0'*(20-len(val))

    @property
    def cProductType(self):return self._ProductType
    @cProductType.setter
    def Prop06ProductType(self,val):self._ProductType=val+'\0'*(20-len(val))

    @property
    def cNetPosition(self):return self._NetPosition
    @cNetPosition.setter
    def Prop07NetPosition(self,val):self._NetPosition=val

    @property
    def cAVGRate(self):return self._AVGRate
    @cAVGRate.setter
    def Prop08AVGRate(self,val):self._AVGRate=val

    @property
    def cMKTRate(self):return self._MKTRate
    @cMKTRate.setter
    def Prop09MKTRate(self,val):self._MKTRate=val

    @property
    def cMTMP(self):return self._MTMP
    @cMTMP.setter
    def Prop10MTMP(self,val):self._MTMP=val

    @property
    def cBookedPL(self):return self._BookedPL
    @cBookedPL.setter
    def Prop11BookedPL(self,val):self._BookedPL=val

    @property
    def cBuyQty(self):return self._BuyQty
    @cBuyQty.setter
    def Prop12BuyQty(self,val):self._BuyQty=val

    @property
    def cAVGBuyRate(self):return self._AVGBuyRate
    @cAVGBuyRate.setter
    def Prop13AVGBuyRate(self,val):self._AVGBuyRate=val

    @property
    def cBuyValue(self):return self._BuyValue
    @cBuyValue.setter
    def Prop14BuyValue(self,val):self._BuyValue=val

    @property
    def cSellQty(self):return self._SellQty
    @cSellQty.setter
    def Prop15SellQty(self,val):self._SellQty=val

    @property
    def cAVGSellRate(self):return self._AVGSellRate
    @cAVGSellRate.setter
    def Prop16AVGSellRate(self,val):self._AVGSellRate=val

    @property
    def cSellValue(self):return self._SellValue
    @cSellValue.setter
    def Prop17SellValue(self,val):self._SellValue=val

    @property
    def cDPQty(self):return self._DPQty
    @cDPQty.setter
    def Prop18DPQty(self,val):self._DPQty=val

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop19Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))


    def ByteToStruct(self,val):
        try:
            self.Prop01DataLenght=struct.unpack('I',val[10:14])
            self.Prop02Exchange=struct.pack("B"*len(val[14:16]),*val[14:16]).decode('utf8')
            self.Prop03ScripName=struct.pack("B"*len(val[16:116]),*val[16:116]).decode('utf8')
            self.Prop04ScripToken=struct.pack("B"*len(val[116:126]),*val[116:126]).decode('utf8')
            self.Prop05Segment=struct.pack("B"*len(val[126:146]),*val[126:146]).decode('utf8')
            self.Prop06ProductType=struct.pack("B"*len(val[146:166]),*val[146:166]).decode('utf8')
            self.Prop07NetPosition=struct.unpack('I',val[166:170])
            self.Prop08AVGRate=struct.unpack('I',val[170:174])
            self.Prop09MKTRate=struct.unpack('I',val[174:178])
            self.Prop10MTMP=struct.unpack('I',val[178:182])
            self.Prop11BookedPL=struct.unpack('i',val[182:186])
            self.Prop12BuyQty=struct.unpack('i',val[186:190])
            self.Prop13AVGBuyRate=struct.unpack('I',val[190:194])
            self.Prop14BuyValue=struct.unpack('I',val[194:198])
            self.Prop15SellQty=struct.unpack('I',val[198:202])
            self.Prop16AVGSellRate=struct.unpack('i',val[202:206])
            self.Prop17SellValue=struct.unpack('i',val[206:210])
            self.Prop18DPQty=struct.unpack('i',val[210:214])
            self.Prop19Reserved=struct.pack("B"*len(val[214:314]),*val[214:314]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        return ('DataLength= '+str(self.cDataLength) + "|" +'Exchange= '+ self.cExchange + "|" + 'ScripName= '+self.cScripName + "|" + 'ScripToken = '+self.cScripToken + "|" + 'Segment= '+self.cSegment + "|" +'ProductType= '+ self.cProductType + "|" +'NetPosition= '+ str(self.cNetPosition)
                    + "|" +'AVGRate = '+ str(self.cAVGRate) + "|" +'MKTRate= '+ str(self.cMKTRate) + "|" +'MTMP= '+ str(self.cMTMP) + "|" +'BookedPL= '+ str(self.cBookedPL) + "|" +'BuyQty= '+ str(self.cBuyQty) + "|" +'AvgBuyRate= '+ str(self.cAVGBuyRate)
                    + "|" + 'BuyValue= '+str(self.cBuyValue) + "|" + 'SellQty= '+str(self.cSellQty) + "|" +'AVGSellRate= '+ str(self.cAVGSellRate) + "|" +'SellValue= '+ str(self.cSellValue) + "|"+'DPQty= '+ str(self.cDPQty) + "|" + 'Reserved = '+self.cReserved)

class TurnOverReportItem():
    def __init__(self,tranCode):
        self._DataLength=0
        self._Exchange=None
        self._CustomerID=None
        self._ScripToken=None
        self._S2KID=None
        self._OpenQty=0
        self._BuyQty=0
        self._SellQty=0
        self._NetQty=0
        self._OpeningRate=0
        self._BuyRate=0
        self._SellRate=0
        self._NetRate=0
        self._IntradayRate=0
        self._IntradayQty=0
        self._SqOffQty=0
        self._PrevClose=0
        self._MktPrice=0
        self._MTM=0
        self._Bpl=0
        self._StatementDate=None
        self._OpenSettMTM=0
        self._NetSettledMTM=0
        self._BookedSettledMTM=0
        self._TotalMTM=0
        self._TotalBpl=0
        self._InvstType=None
        self._Reserved=None

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cExchange(self):return self._Exchange
    @cExchange.setter
    def Prop02Exchange(self,val):self._Exchange=val+'\0'*(2-len(val))

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop03CustomerID(self,val):self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop04ScripToken(self,val):self._ScripToken=val+'\0'*(10-len(val))

    @property
    def cS2KID(self):return self._S2KID
    @cS2KID.setter
    def Prop05S2KID(self,val):self._S2KID=val+'\0'*(10-len(val))

    @property
    def cOpenQty(self):return self._OpenQty
    @cOpenQty.setter
    def Prop06OpenQty(self,val):self._OpenQty=val

    @property
    def cBuyQty(self):return self._BuyQty
    @cBuyQty.setter
    def Prop07BuyQty(self,val):self._BuyQty=val

    @property
    def cSellQty(self):return self._SellQty
    @cSellQty.setter
    def Prop08SellQty(self,val):self._SellQty=val

    @property
    def cNetQty(self):return self._NetQty
    @cNetQty.setter
    def Prop09NetQty(self,val):self._NetQty=val

    @property
    def cOpeningRate(self):return self._OpeningRate
    @cOpeningRate.setter
    def Prop10OpeningRate(self,val):self._OpeningRate=val

    @property
    def cBuyRate(self):return self._BuyRate
    @cBuyRate.setter
    def Prop11BuyRate(self,val):self._BuyRate=val

    @property
    def cSellRate(self):return self._SellRate
    @cSellRate.setter
    def Prop12SellRate(self,val):self._SellRate=val

    @property
    def cNetRate(self):return self._NetRate
    @cNetRate.setter
    def Prop13NetRate(self,val):self._NetRate=val

    @property
    def cIntradayRate(self):return self._IntradayRate
    @cIntradayRate.setter
    def Prop14IntradayRate(self,val):self._IntradayRate=val

    @property
    def cIntradayQty(self):return self._IntradayQty
    @cIntradayQty.setter
    def Prop15IntradayQty(self,val):self._IntradayQty=val

    @property
    def cSqOffQty(self):return self._SqOffQty
    @cSqOffQty.setter
    def Prop16SqOffQty(self,val):self._SqOffQty=val

    @property
    def cPrevClose(self):return self._PrevClose
    @cPrevClose.setter
    def Prop17PrevClose(self,val):self._PrevClose=val

    @property
    def cMktPrice(self):return self._MktPrice
    @cMktPrice.setter
    def Prop18MktPrice(self,val):self._MktPrice=val

    @property
    def cMTM(self):return self._MTM
    @cMTM.setter
    def Prop19MTM(self,val):self._MTM=val

    @property
    def cBpl(self):return self._Bpl
    @cBpl.setter
    def Prop20Bpl(self,val):self._Bpl=val

    @property
    def cStatementDate(self):return self._StatementDate
    @cStatementDate.setter
    def Prop21StatementDate(self,val):self._StatementDate=val+'\0'*(25-len(val))

    @property
    def cOpenSettMTM(self):return self._OpenSettMTM
    @cOpenSettMTM.setter
    def Prop22OpenSettMTM(self,val):self._OpenSettMTM=val

    @property
    def cNetSettledMTM(self):return self._NetSettledMTM
    @cNetSettledMTM.setter
    def Prop23NetSettledMTM(self,val):self._NetSettledMTM=val

    @property
    def cBookedSettledMTM(self):return self._BookedSettledMTM
    @cBookedSettledMTM.setter
    def Prop24BookedSettledMTM(self,val):self._BookedSettledMTM=val

    @property
    def cTotalMTM(self):return self._TotalMTM
    @cTotalMTM.setter
    def Prop25TotalMTM(self,val):self._TotalMTM=val

    @property
    def cTotalBpl(self):return self._TotalBpl
    @cTotalBpl.setter
    def Prop26TotalBpl(self,val):self._TotalBpl=val

    @property
    def cInvstType(self):return self._InvstType
    @cInvstType.setter
    def Prop27InvstType(self,val):self._InvstType=val+'\0'*(15-len(val))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop28Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))


    def ByteToStruct(self,val):
        self.Prop01DataLenght=struct.unpack('I',val[0:4])
        self.Prop02Exchange=struct.pack("B"*len(val[4:6]),*val[4:6]).decode('utf8')
        self.Prop03CustomerID=struct.pack("B"*len(val[6:16]),*val[6:16]).decode('utf8')
        self.Prop04ScripToken=struct.pack("B"*len(val[16:26]),*val[16:26]).decode('utf8')
        self.Prop05S2KID=struct.pack("B"*len(val[26:36]),*val[26:36]).decode('utf8')
        self.Prop06OpenQty=struct.unpack('i',val[36:40])
        self.Prop07BuyQty=struct.unpack('i',val[40:44])
        self.Prop08SellQty=struct.unpack('I',val[44:48])
        self.Prop09NetQty=struct.unpack('I',val[48:52])
        self.Prop10OpeningRate=struct.unpack('I',val[52:56])
        self.Prop11BuyRate=struct.unpack('I',val[56:60])
        self.Prop12SellRate=struct.unpack('I',val[60:64])
        self.Prop13NetRate=struct.unpack('I',val[64:68])
        self.Prop14IntradayRate=struct.unpack('I',val[68:72])
        self.Prop15IntradayQty=struct.unpack('I',val[72:76])
        self.Prop16SqOffQty=struct.unpack('I',val[76:80])
        self.Prop17PrevClose=struct.unpack('I',val[80:84])
        self.Prop18MktPrice=struct.unpack('I',val[84:88])
        self.Prop19MTM=struct.unpack('I',val[88:92])
        self.Prop20Bpl=struct.unpack('i',val[92:96])
        self.Prop21StatementDate=struct.pack("B"*len(val[96:121]),*val[96:121]).decode('utf8')
        self.Prop22OpenSettMTM=struct.unpack('I',val[121:125])
        self.Prop23NetSettledMTM=struct.unpack('I',val[125:129])
        self.Prop24BookedSettledMTM=struct.unpack('I',val[129:133])
        self.Prop25TotalMTM=struct.unpack('I',val[133:137])
        self.Prop26TotalBpl=struct.unpack('i',val[137:141])
        self.Prop27InvstType=struct.pack("B"*len(val[141:145]),*val[141:145]).decode('utf8')
        self.Prop28Reserved=struct.pack("B"*len(val[145:245]),*val[145:245]).decode('utf8')

    def ToString(self):
        return (self.cDataLenght + "|" + self.cExchange + "|" + self.cCustomerID + "|" + self.cScripToken + "|" + self.cS2KID + "|" + self.cOpenQty + "|" + self.cBuyQty + "|" + self.cSellQty + "|" + self.cNetQty + "|" + self.cOpeningRate
                    + "|" + self.cBuyRate + "|" + self.cSellRate + "|" + self.cNetRate + "|" + self.cIntradayRate + "|" + self.cIntradayQty + "|" + self.cSqOffQty + "|" + self.cPrevClose + "|" + self.cMktPrice + "|" + self.cMTM + "|" + self.cBpl
                    + "|" + self.cStatementDate + "|" + self.cOpenSettMTM + "|" + self.cNetSettledMTM + "|" + self.cBookedSettledMTM + "|" + self.cTotalMTM + "|" + self.cTotalBpl + "|" + self.cInvstType + "|" + self.cReserved)

class CashOrderDetailsReportItem():
    def __init__(self,tranCode):
        self._DataLength=0
        self._OrderDisplayStatus=None
        self._OrderID=None
        self._ExchAckDateTime=None
        self._OrderQty=0
        self._OrderPrice=0
        self._OrderTriggerPrice=0
        self._RequestStatus=None
        self._OrderTrailingPrice=0
        self._OrderTargetPrice=0
        self._UpperPrice=0
        self._ChildSLPrice=0
        self._LowerPrice=0
        self._ErrorMsg=None
        self._Reserved=None

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLenght(self,val):self._DataLength=val

    @property
    def cOrderDisplayStatus(self):return self._OrderDisplayStatus
    @cOrderDisplayStatus.setter
    def Prop02OrderDisplayStatus(self,val):self._OrderDisplayStatus=val+'\0'*(15-len(val))

    @property
    def cOrderID(self):return self._OrderID
    @cOrderID.setter
    def Prop03OrderID(self,val):self._OrderID=val+'\0'*(20-len(val))

    @property
    def cExchAckDateTime(self):return self._ExchAckDateTime
    @cExchAckDateTime.setter
    def Prop04ExchAckDateTime(self,val):self._ExchAckDateTime=val+'\0'*(25-len(val))

    @property
    def cOrderQty(self):return self._OrderQty
    @cOrderQty.setter
    def Prop05OrderQty(self,val):self._OrderQty=val

    @property
    def cOrderPrice(self):return self._OrderPrice
    @cOrderPrice.setter
    def Prop06OrderPrice(self,val):self._OrderPrice=val

    @property
    def cOrderTriggerPrice(self):return self._OrderTriggerPrice
    @cOrderTriggerPrice.setter
    def Prop07OrderTriggerPrice(self,val):self._OrderTriggerPrice=val

    @property
    def cRequestStatus(self):return self._RequestStatus
    @cRequestStatus.setter
    def Prop08RequestStatus(self,val):self._RequestStatus=val+'\0'*(15-len(val))

    @property
    def cOrderTrailingPrice(self):return self._OrderTrailingPrice
    @cOrderTrailingPrice.setter
    def Prop09OrderTrailingPrice(self,val):self._OrderTrailingPrice=val

    @property
    def cOrderTargetPrice(self):return self._OrderTargetPrice
    @cOrderTargetPrice.setter
    def Prop10OrderTargetPrice(self,val):self._OrderTargetPrice=val

    @property
    def cUpperPrice(self):return self._UpperPrice
    @cUpperPrice.setter
    def Prop11UpperPrice(self,val):self._UpperPrice=val

    @property
    def cChildSLPrice(self):return self._ChildSLPrice
    @cChildSLPrice.setter
    def Prop12ChildSLPrice(self,val):self._ChildSLPrice=val

    @property
    def cLowerPrice(self):return self._LowerPrice
    @cLowerPrice.setter
    def Prop13LowerPrice(self,val):self._LowerPrice=val

    @property
    def cErrorMsg(self):return self._ErrorMsg
    @cErrorMsg.setter
    def Prop14ErrorMsg(self,val):self._ErrorMsg=val+'\0'*(250-len(val))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop15Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))


    def ByteToStruct(self,val):
        try:
            self.Prop01DataLenght=struct.unpack('I',val[10:14])
            self.Prop02OrderDisplayStatus=struct.pack("B"*len(val[14:29]),*val[14:29]).decode('utf8')
            self.Prop03OrderID=struct.pack("B"*len(val[29:49]),*val[29:49]).decode('utf8')
            self.Prop04ExchAckDateTime=struct.pack("B"*len(val[49:74]),*val[49:74]).decode('utf8')
            self.Prop05OrderQty=struct.unpack('i',val[74:78])
            self.Prop06OrderPrice=struct.unpack('I',val[78:82])
            self.Prop07OrderTriggerPrice=struct.unpack('I',val[82:86])
            self.Prop08RequestStatus=struct.pack("B"*len(val[86:101]),*val[86:101]).decode('utf8')
            self.Prop09OrderTrailingPrice=struct.unpack('I',val[101:105])
            self.Prop10OrderTargetPrice=struct.unpack('I',val[105:109])
            self.Prop11UpperPrice=struct.unpack('I',val[109:113])
            self.Prop12ChildSLPrice=struct.unpack('I',val[113:117])
            self.Prop13LowerPrice=struct.unpack('I',val[117:121])
            self.Prop14ErrorMsg=struct.pack("B"*len(val[121:271]),*val[121:271]).decode('utf8')
            self.Prop15Reserved=struct.pack("B"*len(val[271:371]),*val[271:371]).decode('utf8')
        except:
            logger.exception(PrintException())

    def ToString(self):
        return ("DatatLength = " + str(self.cDataLength) + "|" + "OrderDisplayStatus = " + str(self.cOrderDisplayStatus) + "|" + "OrderID = " + str(self.cOrderID) + "|" + "ExchAckDateTime = " + str(self.cExchAckDateTime) + "|" + "OrderQty =" + str(self.cOrderQty) + "|" + "OrderPrice = " + str(self.cOrderPrice) + "|" +
                    'OrderTriggerPrice = '+str(self.cOrderTriggerPrice) + "|" + "RequestStatus = " + str(self.cRequestStatus) + "|" + "OrderTrailingPrice = " + str(self.cOrderTrailingPrice) + "|" + "OrderTargetPrice = " + str(self.cOrderTargetPrice) + "|" + "UpperPrice = " + str(self.cUpperPrice) + "|" + "ChildSLPrice = " + str(self.cChildSLPrice)
                    + "|" + "LowerPrice = " + str(self.cLowerPrice) + "|" + "ErrorMsg = " + str(self.cErrorMsg) + "|" + "Reserved = " + str(self.cReserved))

class CashTradeDetailsReportItem():
    def __init__(self,transCode):
        self._DataLength=0
        self._ExchangeCode=None
        self._OrderID=None
        self._ExchOrderID=None
        self._ExchAckDateTime=None
        self._TradeDateTime=None
        self._InternalTradeID=None
        self._TradeID=None
        self._CustomerID=None
        self._ScripToken=None
        self._BuySell=None
        self._TradeQty=0
        self._TradePrice=0
        self._TradeAmount=0
        self._TotalTradeAmount=0
        self._ChannelCode=None
        self._OrsExchangeMarketCode=None
        self._Reserved=None

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,val):self._ExchangeCode=val+'\0'*(2-len(val))

    @property
    def cOrderID(self):return self._OrderID
    @cOrderID.setter
    def Prop03OrderID(self,val):self._OrderID=val+'\0'*(20-len(val))

    @property
    def cExchOrderID(self):return self._ExchOrderID
    @cExchOrderID.setter
    def Prop04ExchOrderID(self,val):self._ExchOrderID=val+'\0'*(25-len(val))

    @property
    def cExchAckDateTime(self):return self._ExchAckDateTime
    @cExchAckDateTime.setter
    def Prop05ExchAckDateTime(self,val):self._ExchAckDateTime=val+'\0'*(25-len(val))

    @property
    def cTradeDateTime(self):return self._TradeDateTime
    @cTradeDateTime.setter
    def Prop06TradeDateTime(self,val):self._TradeDateTime=val+'\0'*(25-len(val))

    @property
    def cInternalTradeID(self):return self._InternalTradeID
    @cInternalTradeID.setter
    def Prop07InternalTradeID(self,val):self._InternalTradeID=val+'\0'*(15-len(val))

    @property
    def cTradeID(self):return self._TradeID
    @cTradeID.setter
    def Prop08TradeID(self,val):self._TradeID=val+'\0'*(20-len(val))

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop09CustomerID(self,val):self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop10ScripToken(self,val):self._ScripToken=val+'\0'*(10-len(val))

    @property
    def cBuySell(self):return self._BuySell
    @cBuySell.setter
    def Prop11BuySell(self,val):self._BuySell=val+'\0'*(2-len(val))

    @property
    def cTradeQty(self):return self._TradeQty
    @cTradeQty.setter
    def Prop12TradeQty(self,val):self._TradeQty=val

    @property
    def cTradePrice(self):return self._TradePrice
    @cTradePrice.setter
    def Prop13TradePrice(self,val):self._TradePrice=val

    @property
    def cTradeAmount(self):return self._TradeAmount
    @cTradeAmount.setter
    def Prop14TradeAmount(self,val):self._TradeAmount=val

    @property
    def cTotalTradeAmount(self):return self._TotalTradeAmount
    @cTotalTradeAmount.setter
    def Prop15TradeAmount(self,val):self._TotalTradeAmount=val

    @property
    def cChannelCode(self):return self._ChannelCode
    @cChannelCode.setter
    def Prop16ChannelCode(self,val):self._ChannelCode=val+'\0'*(10-len(val))

    @property
    def cOrsExchangeMarketCode(self):return self._OrsExchangeMarketCode
    @cOrsExchangeMarketCode.setter
    def Prop17OrsExchangeMarketCode(self,val):self._OrsExchangeMarketCode=val+'\0'*(10-len(val))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop18Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))


    def ByteToStruct(self,val):
        self.Prop01DataLenght=struct.unpack('I',val[0:4])
        self.Prop02ExchangeCode=struct.pack("B"*len(val[4:6]),*val[4:6]).decode('utf8')
        self.Prop03OrderID=struct.pack("B"*len(val[6:26]),*val[6:26]).decode('utf8')
        self.Prop04ExchOrderID=struct.pack("B"*len(val[26:51]),*val[26:51]).decode('utf8')
        self.Prop05ExchAckDateTime=struct.pack("B"*len(val[51:76]),*val[51:76]).decode('utf8')
        self.Prop06TradeDateTime=struct.pack("B"*len(val[76:101]),*val[76:101]).decode('utf8')
        self.Prop07InternalTradeID=struct.pack("B"*len(val[101:116]),*val[101:116]).decode('utf8')
        self.Prop08TradeID=struct.pack("B"*len(val[116:136]),*val[116:136]).decode('utf8')
        self.Prop09CustomerID=struct.pack("B"*len(val[136:146]),*val[136:146]).decode('utf8')
        self.Prop10ScripToken=struct.pack("B"*len(val[146:156]),*val[146:156]).decode('utf8')
        self.Prop11BuySell=struct.pack("B"*len(val[156:158]),*val[156:158]).decode('utf8')
        self.Prop12TradeQty=struct.unpack('I',val[158:162])
        self.Prop13TradePrice=struct.unpack('I',val[162:166])
        self.Prop14TradeAmount=struct.unpack('I',val[166:170])
        self.Prop15TradeAmount=struct.unpack('I',val[170:174])
        self.Prop16ChannelCode=struct.pack("B"*len(val[174:184]),*val[174:184]).decode('utf8')
        self.Prop17OrsExchangeMarketCode=struct.pack("B"*len(val[184:194]),*val[184:194]).decode('utf8')
        self.Prop18Reserved=struct.pack("B"*len(val[194:294]),*val[194:294]).decode('utf8')

    def ToString(self):
        return ("DataLenght = " + str(self.cDataLenght) + "|" + "ExchangeCode = " + str(self.cExchangeCode) + "|" + "LowerPrice = " + str(self.cOrderID) + "|" + "ExchOrderID = " + str(self.cExchOrderID) + "|" + "ExchAckDateTime = " + str(self.cExchAckDateTime) + "|" + "TradeDateTime = " + str(self.cTradeDateTime) + "|" + "InternalTradeID = " + str(self.cInternalTradeID) + "|" + "TradeID = " + str(self.cTradeID)
                    + "|" + "CustomerID  = " + str(self.cCustomerID) + "|" + "ScripToken = " + str(self.cScripToken) + "|" + "BuySell = " + str(self.cBuySell) + "|" + "TradeQty = " + str(self.cTradeQty) + "|" + "TradePrice = " + str(self.cTradePrice) + "|" + "TradeAmount = " + str(self.cTradeAmount) + "|" + "TradeAmount = " + str(self.cTradeAmount) + "|" + "ChannelCode = " + str(self.cChannelCode)
                    + "|" + "ChannelCode  = " + str(self.cChannelCode) + "|" + "OrsExchangeMarketCode = " + str(self.cOrsExchangeMarketCode) + "|" + "Reserved = " + str(self.cReserved))

class DerivativeOrderDetailReportItem():
    def __init__(self,transcode):
        self._DataLength=0
        self._ExchangeCode=None
        self._OrderStatus=None
        self._OrderID=None
        self._ExchangeOrderID=None
        self._OrderDateTime=None
        self._CustomerID=None
        self._DpClientId=None
        self._OrsOrderID=None
        self._ScripToken=None
        self._OrderType=None
        self._BuySell=None
        self._OrderQty=0
        self._OrderExecutedQty=0
        self._OrderDisclosedQty=0
        self._OrderMIFQty=0
        self._OrderPrice=0
        self._OrderTriggerPrice=0
        self._RMSCode=None
        self._AfterHour=None
        self._BranchTraderID=None
        self._AveragePrice=0
        self._RequestStatus=None
        self._GoodTill=None
        self._GoodTillDate=None
        self._DpId=None
        self._OrsExchangeMktCode=None
        self._ChannelCode=None
        self._ChannelUser=None
        self._LastModDateTime=None
        self._OpenQty=0
        self._PvtOrderInd=0
        self._ClientAccount=None
        self._ClientGroup=None
        self._OhEntryDateTime=None
        self._WebResponseTime=None
        self._FohExitDateTime=None
        self._ExchangeAckDateTime=None
        self._Brokerage=0
        self._ParticipantCode=None
        self._UpdateDate=None
        self._UpdateUser=None
        self._CALevel=None
        self._AllOrNone=None
        self._OpenOrClose=None
        self._FnoOrderType=None
        self._FnoSquareOff=None
        self._Reserved=None
    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,val):self._ExchangeCode=val+'\0'*(2-len(val))

    @property
    def cOrderStatus(self):return self._OrderStatus
    @cOrderStatus.setter
    def Prop03OrderStatus(self,val):self._OrderStatus=val+'\0'*(20-len(val))

    @property
    def cOrderID(self):return self._OrderID
    @cOrderID.setter
    def Prop04OrderID(self,val):self._OrderID=val+'\0'*(20-len(val))

    @property
    def cExchangeOrderID(self):return self._ExchangeOrderID
    @cExchangeOrderID.setter
    def Prop05ExchangeOrderID(self,val):self._ExchangeOrderID=val+'\0'*(20-len(val))

    @property
    def cOrderDateTime(self):return self._OrderDateTime
    @cOrderDateTime.setter
    def Prop06OrderDateTime(self,val):self._OrderDateTime=val+'\0'*(25-len(val))

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop07CustomerID(self,val):self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cDpClientId(self):return self._DpClientId
    @cDpClientId.setter
    def Prop08DpClientId(self,val):self._DpClientId=val+'\0'*(25-len(val))

    @property
    def cOrsOrderID(self):return self._OrsOrderID
    @cOrsOrderID.setter
    def Prop09OrsOrderID(self,val):self._OrsOrderID=val+'\0'*(10-len(val))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop10ScripToken(self,val):self._ScripToken=val+'\0'*(10-len(val))

    @property
    def cOrderType(self):return self._OrderType
    @cOrderType.setter
    def Prop11OrderType(self,val):self._OrderType=val+'\0'*(10-len(val))

    @property
    def cBuySell(self):return self._BuySell
    @cBuySell.setter
    def Prop12BuySell(self,val):self._BuySell=val+'\0'*(2-len(val))

    @property
    def cOrderQty(self):return self._OrderQty
    @cOrderQty.setter
    def Prop13OrderQty(self,val):self._OrderQty=val

    @property
    def cOrderExecutedQty(self):return self._OrderExecutedQty
    @cOrderExecutedQty.setter
    def Prop14OrderExecutedQty(self,val):self._OrderExecutedQty=val

    @property
    def cOrderDisclosedQty(self):return self._OrderDisclosedQty
    @cOrderDisclosedQty.setter
    def Prop15OrderDisclosedQty(self,val):self._OrderDisclosedQty=val

    @property
    def cOrderMIFQty(self):return self._OrderMIFQty
    @cOrderMIFQty.setter
    def Prop16OrderMIFQty(self,val):self._OrderMIFQty=val

    @property
    def cOrderPrice(self):return self._OrderPrice
    @cOrderPrice.setter
    def Prop17OrderPrice(self,val):self._OrderPrice=val

    @property
    def cOrderTriggerPrice(self):return self._OrderTriggerPrice
    @cOrderTriggerPrice.setter
    def Prop18OrderTriggerPrice(self,val):self._OrderTriggerPrice=val

    @property
    def cRMSCode(self):return self._RMSCode
    @cRMSCode.setter
    def Prop19RMSCode(self,val):self._RMSCode=val+'\0'*(15-len(val))

    @property
    def cAfterHour(self):return self._AfterHour
    @cAfterHour.setter
    def Prop20AfterHour(self,val):self._AfterHour=val+'\0'*(1-len(val))

    @property
    def cBranchTraderID(self):return self._BranchTraderID
    @cBranchTraderID.setter
    def Prop21BranchTraderID(self,val):self._BranchTraderID=val+'\0'*(15-len(val))

    @property
    def cAveragePrice(self):return self._AveragePrice
    @cAveragePrice.setter
    def Prop22AveragePrice(self,val):self._AveragePrice=val

    @property
    def cRequestStatus(self):return self._RequestStatus
    @cRequestStatus.setter
    def Prop23RequestStatus(self,val):self._RequestStatus=val+'\0'*(15-len(val))

    @property
    def cGoodTill(self):return self._GoodTill
    @cGoodTill.setter
    def Prop24GoodTill(self,val):self._GoodTill=val+'\0'*(5-len(val))

    @property
    def cGoodTillDate(self):return self._GoodTillDate
    @cGoodTillDate.setter
    def Prop25GoodTillDate(self,val):self._GoodTillDate=val+'\0'*(25-len(val))

    @property
    def cDpId(self):return self._DpId
    @cDpId.setter
    def Prop26DpId(self,val):self._DpId=val+'\0'*(10-len(val))

    @property
    def cOrsExchangeMktCode(self):return self._OrsExchangeMktCode
    @cOrsExchangeMktCode.setter
    def Prop27OrsExchangeMktCode(self,val):self._OrsExchangeMktCode=val+'\0'*(10-len(val))

    @property
    def cChannelCode(self):return self._ChannelCode
    @cChannelCode.setter
    def Prop28ChannelCode(self,val):self._ChannelCode=val+'\0'*(10-len(val))

    @property
    def cChannelUser(self):return self._ChannelUser
    @cChannelUser.setter
    def Prop29ChannelUser(self,val):self._ChannelUser=val+'\0'*(20-len(val))

    @property
    def cLastModDateTime(self):return self._LastModDateTime
    @cLastModDateTime.setter
    def Prop30LastModDateTime(self,val):self._LastModDateTime=val+'\0'*(25-len(val))

    @property
    def cOpenQty(self):return self._OpenQty
    @cOpenQty.setter
    def Prop31OpenQty(self,val):self._OpenQty=val

    @property
    def cPvtOrderInd(self):return self._PvtOrderInd
    @cPvtOrderInd.setter
    def Prop32PvtOrderInd(self,val):self._PvtOrderInd=val

    @property
    def cClientAccount(self):return self._ClientAccount
    @cClientAccount.setter
    def Prop33ClientAccount(self,val):self._ClientAccount=val+'\0'*(20-len(val))

    @property
    def cClientGroup(self):return self._ClientGroup
    @cClientGroup.setter
    def Prop34ClientGroup(self,val):self._ClientGroup=val+'\0'*(20-len(val))

    @property
    def cOhEntryDateTime(self):return self._OhEntryDateTime
    @cOhEntryDateTime.setter
    def Prop35OhEntryDateTime(self,val):self._OhEntryDateTime=val+'\0'*(25-len(val))

    @property
    def cWebResponseTime(self):return self._WebResponseTime
    @cWebResponseTime.setter
    def Prop36WebResponseTime(self,val):self._WebResponseTime=val+'\0'*(25-len(val))

    @property
    def cFohExitDateTime(self):return self._FohExitDateTime
    @cFohExitDateTime.setter
    def Prop37FohExitDateTime(self,val):self._FohExitDateTime=val+'\0'*(25-len(val))

    @property
    def cExchangeAckDateTime(self):return self._ExchangeAckDateTime
    @cExchangeAckDateTime.setter
    def Prop38ExchangeAckDateTime(self,val):self._ExchangeAckDateTime=val+'\0'*(25-len(val))

    @property
    def cBrokerage(self):return self._Brokerage
    @cBrokerage.setter
    def Prop39Brokerage(self,val):self._Brokerage=val

    @property
    def cParticipantCode(self):return self._ParticipantCode
    @cParticipantCode.setter
    def Prop40ParticipantCode(self,val):self._ParticipantCode=val+'\0'*(10-len(val))

    @property
    def cUpdateDate(self):return self._UpdateDate
    @cUpdateDate.setter
    def Prop41UpdateDate(self,val):self._UpdateDate=val+'\0'*(25-len(val))

    @property
    def cUpdateUser(self):return self._UpdateUser
    @cUpdateUser.setter
    def Prop42UpdateUser(self,val):self._UpdateUser=val+'\0'*(25-len(val))

    @property
    def cCALevel(self):return self._CALevel
    @cCALevel.setter
    def Prop43CALevel(self,val):self._CALevel=val+'\0'*(15-len(val))

    @property
    def cAllOrNone(self):return self._AllOrNone
    @cAllOrNone.setter
    def Prop44AllOrNone(self,val):self._AllOrNone=val+'\0'*(25-len(val))

    @property
    def cOpenOrClose(self):return self._OpenOrClose
    @cOpenOrClose.setter
    def Prop45OpenOrClose(self,val):self._OpenOrClose=val+'\0'*(25-len(val))

    @property
    def cFnoOrderType(self):return self._FnoOrderType
    @cFnoOrderType.setter
    def Prop46FnoOrderType(self,val):self._FnoOrderType=val+'\0'*(25-len(val))

    @property
    def cFnoSquareOff(self):return self._FnoSquareOff
    @cFnoSquareOff.setter
    def Prop47FnoSquareOff(self,val):self._FnoSquareOff=val+'\0'*(25-len(val))

    @property
    def cReserved(self):return self._cReserved
    @cReserved.setter
    def Prop48Reserved(self,val):self._cReserved=val+'\0'*(100-len(val))


    def ByteToStruct(self,val):
        self.Prop01DataLenght=struct.unpack('I',val[0:4])
        self.Prop02ExchangeCode=struct.pack("B"*len(val[4:6]),*val[4:6]).decode('utf8')
        self.Prop03OrderStatus=struct.pack("B"*len(val[6:26]),*val[6:26]).decode('utf8')
        self.Prop04OrderID=struct.pack("B"*len(val[26:46]),*val[26:46]).decode('utf8')
        self.Prop05ExchangeOrderID=struct.pack("B"*len(val[46:66]),*val[46:66]).decode('utf8')
        self.Prop06OrderDateTime=struct.pack("B"*len(val[66:91]),*val[66:91]).decode('utf8')
        self.Prop07CustomerID=struct.pack("B"*len(val[91:101]),*val[91:101]).decode('utf8')
        self.Prop08DpClientId=struct.pack("B"*len(val[101:126]),*val[101:126]).decode('utf8')
        self.Prop09OrsOrderID=struct.pack("B"*len(val[126:136]),*val[126:136]).decode('utf8')
        self.Prop10ScripToken=struct.pack("B"*len(val[136:146]),*val[136:146]).decode('utf8')
        self.Prop11OrderType=struct.pack("B"*len(val[146:156]),*val[146:156]).decode('utf8')
        self.Prop12BuySell=struct.pack("B"*len(val[156:158]),*val[156:158]).decode('utf8')
        self.Prop13OrderQty=struct.unpack('I',val[158:162])
        self.Prop14OrderExecutedQty=struct.unpack('I',val[162:166])
        self.Prop15OrderDisclosedQty=struct.unpack('I',val[166:170])
        self.Prop16OrderMIFQty=struct.unpack('I',val[170:174])
        self.Prop17OrderPrice=struct.unpack('I',val[174:178])
        self.Prop18OrderTriggerPrice=struct.unpack('I',val[178:182])
        self.Prop19RMSCode=struct.pack("B"*len(val[182:197]),*val[182:197]).decode('utf8')
        self.Prop20AfterHour=struct.pack("B"*len(val[197:198]),*val[197:198]).decode('utf8')
        self.Prop21BranchTraderID=struct.pack("B"*len(val[198:213]),*val[198:213]).decode('utf8')
        self.Prop22AveragePrice=struct.unpack('I',val[213:217])
        self.Prop23RequestStatus=struct.pack("B"*len(val[217:232]),*val[217:232]).decode('utf8')
        self.Prop24GoodTill=struct.pack("B"*len(val[232:237]),*val[232:237]).decode('utf8')
        self.Prop25GoodTillDate=struct.pack("B"*len(val[237:262]),*val[237:262]).decode('utf8')
        self.Prop26DpId=struct.pack("B"*len(val[262:272]),*val[262:272]).decode('utf8')
        self.Prop27OrsExchangeMktCode=struct.pack("B"*len(val[272:282]),*val[272:282]).decode('utf8')
        self.Prop28ChannelCode=struct.pack("B"*len(val[282:292]),*val[282:292]).decode('utf8')
        self.Prop29ChannelUser=struct.pack("B"*len(val[292:312]),*val[292:312]).decode('utf8')
        self.Prop30LastModDateTime=struct.pack("B"*len(val[312:337]),*val[312:337]).decode('utf8')
        self.Prop31OpenQty=struct.unpack('I',val[337:441])
        self.Prop32PvtOrderInd=struct.unpack('I',val[441:445])
        self.Prop33ClientAccount=struct.pack("B"*len(val[445:465]),*val[445:465]).decode('utf8')
        self.Prop34ClientGroup=struct.pack("B"*len(val[465:485]),*val[465:485]).decode('utf8')
        self.Prop35OhEntryDateTime=struct.pack("B"*len(val[485:510]),*val[485:510]).decode('utf8')
        self.Prop36WebResponseTime=struct.pack("B"*len(val[510:535]),*val[510:535]).decode('utf8')
        self.Prop37FohExitDateTime=struct.pack("B"*len(val[535:560]),*val[535:560]).decode('utf8')
        self.Prop38ExchangeAckDateTime=struct.pack("B"*len(val[560:585]),*val[560:585]).decode('utf8')
        self.Prop39Brokerage=struct.unpack('I',val[585:589])
        self.Prop40ParticipantCode=struct.pack("B"*len(val[589:599]),*val[589:599]).decode('utf8')
        self.Prop41UpdateDate=struct.pack("B"*len(val[599:624]),*val[599:624]).decode('utf8')
        self.Prop42UpdateUser=struct.pack("B"*len(val[624:649]),*val[624:649]).decode('utf8')
        self.Prop43CALevel=struct.pack("B"*len(val[649:664]),*val[649:664]).decode('utf8')
        self.Prop44AllOrNone=struct.pack("B"*len(val[664:689]),*val[664:689]).decode('utf8')
        self.Prop45OpenOrClose=struct.pack("B"*len(val[689:714]),*val[689:714]).decode('utf8')
        self.Prop46FnoOrderType=struct.pack("B"*len(val[714:739]),*val[714:739]).decode('utf8')
        self.Prop47FnoSquareOff=struct.pack("B"*len(val[739:764]),*val[739:764]).decode('utf8')
        self.Prop48Reserved=struct.pack("B"*len(val[764:864]),*val[764:864]).decode('utf8')

    def ToString(self):
        return (str(self.cDataLenght) + "|" + str(self.cExchangeCode) + "|" + str(self.cOrderStatus) + "|" + str(self.cOrderID) + "|" + str(self.cOrderID) + "|" + str(self.cExchangeOrderID) + "|" + str(self.cOrderDateTime) + "|" + str(self.cCustomerID) + "|" + str(self.cDpClientId) + "|" + str(self.cOrsOrderID) + "|" + str(self.cScripToken)
                    + "|" + str(self.cOrderType) + "|" + str(self.cBuySell) + "|" + str(self.cOrderQty) + "|" + str(self.cOrderExecutedQty) + "|" + str(self.cOrderDisclosedQty) + "|" + str(self.cOrderMIFQty) + "|" + str(self.cOrderPrice) + "|" + str(self.cOrderTriggerPrice) + "|" + str(self.cRMSCode) + "|" + str(self.cAfterHour)
                    + "|" + str(self.cBranchTraderID) + "|" + str(self.cAveragePrice) + "|" + str(self.cRequestStatus) + "|" + str(self.cGoodTill) + "|" + str(self.cGoodTillDate) + "|" + str(self.cDpId) + "|" + str(self.cOrsExchangeMktCode) + "|" + str(self.cChannelCode) + "|" + str(self.cChannelUser) + "|" + str(self.cLastModDateTime)
                    + "|" + str(self.cOpenQty) + "|" + str(self.cPvtOrderInd) + "|" + str(self.cClientAccount) + "|" + str(self.cClientGroup) + str(self.cOhEntryDateTime) + "|" + str(self.cWebResponseTime) + "|" + str(self.cFohExitDateTime) + "|" + str(self.cExchangeAckDateTime) + "|" + str(self.cBrokerage) + "|" + str(self.cParticipantCode)
                    + "|" + str(self.cUpdateDate) + "|" + str(self.cUpdateUser) + "|" + str(self.cCALevel) + "|" + str(self.cAllOrNone) + "|" + str(self.cOpenOrClose) + "|" + str(self.cFnoOrderType) + "|" + str(self.cFnoSquareOff) + "|" + str(self.cReserved))

class DerivativeTradeDetailsReportItem():
    def __init__(self,transCode):
        self._DataLength=0
        self._ExchangeCode=None
        self._InternalTradeId=None
        self._TradeId=None
        self._ChannelCode=None
        self._ChannelUser=None
        self._OrderId=None
        self._CustomerID=None
        self._BuySell=None
        self._OrsExchMktCode=None
        self._ScripToken=None
        self._TradeQty=0
        self._TradePrice=0
        self._TradeAmount=0
        self._TradeDateTime=None
        self._ExchAckDateTime=None
        self._Brokerage=None
        self._TotalTradeAmount=0
        self._UpdateDate=None
        self._UpdateUser=None
        self._CALevel=None
        self._Reserved=None
    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cExchangeCode(self):return self._ExchangeCode
    @cExchangeCode.setter
    def Prop02ExchangeCode(self,val):self._ExchangeCode=val+'\0'*(2-len(val))

    @property
    def cInternalTradeId(self):return self._InternalTradeId
    @cInternalTradeId.setter
    def Prop03InternalTradeId(self,val):self._InternalTradeId=val+'\0'*(15-len(val))

    @property
    def cTradeId(self):return self._TradeId
    @cTradeId.setter
    def Prop04TradeId(self,val):self._TradeId=val+'\0'*(20-len(val))

    @property
    def cChannelCode(self):return self._ChannelCode
    @cChannelCode.setter
    def Prop05ChannelCode(self,val):self._ChannelCode=val+'\0'*(10-len(val))

    @property
    def cChannelUser(self):return self._ChannelUser
    @cChannelUser.setter
    def Prop06ChannelUser(self,val):self._ChannelUser=val+'\0'*(20-len(val))

    @property
    def cOrderId(self):return self._OrderId
    @cOrderId.setter
    def Prop07OrderId(self,val):self._OrderId=val+'\0'*(20-len(val))

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop08CustomerID(self,val):self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cBuySell(self):return self._BuySell
    @cBuySell.setter
    def Prop09BuySell(self,val):self._BuySell=val+'\0'*(2-len(val))

    @property
    def cOrsExchMktCode(self):return self._OrsExchMktCode
    @cOrsExchMktCode.setter
    def Prop10OrsExchMktCode(self,val):self._OrsExchMktCode=val+'\0'*(10-len(val))

    @property
    def cScripToken(self):return self._ScripToken
    @cScripToken.setter
    def Prop11ScripToken(self,val):self._ScripToken=val+'\0'*(10-len(val))

    @property
    def cTradeQty(self):return self._TradeQty
    @cTradeQty.setter
    def Prop12TradeQty(self,val):self._TradeQty=val

    @property
    def cTradePrice(self):return self._TradePrice
    @cTradePrice.setter
    def Prop13TradePrice(self,val):self._TradePrice=val

    @property
    def cTradeAmount(self):return self._TradeAmount
    @cTradeAmount.setter
    def Prop14TradeAmount(self,val):self._TradeAmount=val

    @property
    def cTradeDateTime(self):return self._TradeDateTime
    @cTradeDateTime.setter
    def Prop15TradeDateTime(self,val):self._TradeDateTime=val+'\0'*(25-len(val))

    @property
    def cExchAckDateTime(self):return self._ExchAckDateTime
    @cExchAckDateTime.setter
    def Prop16ExchAckDateTime(self,val):self._ExchAckDateTime=val+'\0'*(25-len(val))

    @property
    def cBrokerage(self):return self._Brokerage
    @cBrokerage.setter
    def Prop17Brokerage(self,val):self._Brokerage=val+'\0'*(10-len(val))

    @property
    def cTotalTradeAmount(self):return self._TotalTradeAmount
    @cTotalTradeAmount.setter
    def Prop18TotalTradeAmount(self,val):self._TotalTradeAmount=val

    @property
    def cUpdateDate(self):return self._UpdateDate
    @cUpdateDate.setter
    def Prop19UpdateDate(self,val):self._UpdateDate=val+'\0'*(25-len(val))

    @property
    def cUpdateUser(self):return self._UpdateUser
    @cUpdateUser.setter
    def Prop20UpdateUser(self,val):self._UpdateUser=val+'\0'*(25-len(val))

    @property
    def cCALevel(self):return self._CALevel
    @cCALevel.setter
    def Prop21CALevel(self,val):self._CALevel=val+'\0'*(15-len(val))

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop22Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))

    def ByteToStruct(self,val):
        self.Prop01DataLenght=struct.unpack('I',val[0:4])
        self.Prop02ExchangeCode=struct.pack("B"*len(val[4:6]),*val[4:6]).decode('utf8')
        self.Prop03InternalTradeId=struct.pack("B"*len(val[6:21]),*val[6:21]).decode('utf8')
        self.Prop04TradeId=struct.pack("B"*len(val[21:41]),*val[21:41]).decode('utf8')
        self.Prop05ChannelCode=struct.pack("B"*len(val[41:51]),*val[41:51]).decode('utf8')
        self.Prop06ChannelUser=struct.pack("B"*len(val[51:71]),*val[51:71]).decode('utf8')
        self.Prop07OrderId=struct.pack("B"*len(val[71:91]),*val[71:91]).decode('utf8')
        self.Prop08CustomerID=struct.pack("B"*len(val[91:101]),*val[91:101]).decode('utf8')
        self.Prop09BuySell=struct.pack("B"*len(val[101:103]),*val[101:103]).decode('utf8')
        self.Prop10OrsExchMktCode=struct.pack("B"*len(val[103:113]),*val[103:113]).decode('utf8')
        self.Prop11ScripToken=struct.pack("B"*len(val[113:123]),*val[113:123]).decode('utf8')
        self.Prop12TradeQty=struct.unpack('I',val[123:127])
        self.Prop13TradePrice=struct.unpack('I',val[127:131])
        self.Prop14TradeAmount=struct.unpack('I',val[131:135])
        self.Prop15TradeDateTime=struct.pack("B"*len(val[135:160]),*val[135:160]).decode('utf8')
        self.Prop16ExchAckDateTime=struct.pack("B"*len(val[160:185]),*val[:]).decode('utf8')
        self.Prop17Brokerage=struct.pack("B"*len(val[185:195]),*val[185:195]).decode('utf8')
        self.Prop18TotalTradeAmount=struct.unpack('I',val[195:199])
        self.Prop19UpdateDate=struct.pack("B"*len(val[199:224]),*val[199:224]).decode('utf8')
        self.Prop20UpdateUser=struct.pack("B"*len(val[224:249]),*val[224:249]).decode('utf8')
        self.Prop21CALevel=struct.pack("B"*len(val[249:259]),*val[249:259]).decode('utf8')
        self.Prop22Reserved=struct.pack("B"*len(val[259:359]),*val[259:359]).decode('utf8')

    def ToString(self):
        return (str(self.cDataLenght) + "|" + str(self.cExchangeCode) + "|" + str(self.cInternalTradeId) + "|" + str(self.cTradeId) + "|" + str(self.cChannelCode) + "|" + str(self.cChannelUser) + "|" + str(self.cOrderId) + "|" + str(self.cCustomerID) + "|" + str(self.cBuySell) + "|" + str(self.cOrsExchMktCode)
                    + "|" + str(self.cScripToken) + "|" + str(self.cTradeQty) + "|" + str(self.cTradePrice) + "|" + str(self.cTradeAmount) + "|" + str(self.cTradeDateTime) + "|" + str(self.cExchAckDateTime) + "|" + str(self.cBrokerage) + "|" + str(self.cTotalTradeAmount) + "|" + str(self.cUpdateDate) + "|" + str(self.cUpdateUser)
                    + "|" + str(self.cCALevel) + "|" + str(self.cReserved))

class CashLimitReportItem():
    def __init__(self,transCode):
        self._DataLength=0
        self._CustomerID=None
        self._CurrentCashBalance=0
        self._PendingWithdrawalRequest=0
        self._NonCashLimit=0
        self._CashBpl=0
        self._CashMTM=0
        self._LimitAgainstShares=0
        self._CashPreviousSettlementExposure=0
        self._IntradayMarginCash=0
        self._FnoMTM=0
        self._FnoPremium=0
        self._FnoBpl=0
        self._IntradayMarginFno=0
        self._IntradayMarginComm=0
        self._HoldFunds=0
        self._Total=0
        self._Reserved=None

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop02CustomerID(self,val):self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cCurrentCashBalance(self):return self._CurrentCashBalance
    @cCurrentCashBalance.setter
    def Prop03CurrentCashBalance(self,val):self._CurrentCashBalance=val

    @property
    def cPendingWithdrawalRequest(self):return self._PendingWithdrawalRequest
    @cPendingWithdrawalRequest.setter
    def Prop04PendingWithdrawalRequest(self,val):self._PendingWithdrawalRequest=val

    @property
    def cNonCashLimit(self):return self._NonCashLimit
    @cNonCashLimit.setter
    def Prop05NonCashLimit(self,val):self._NonCashLimit=val

    @property
    def cCashBpl(self):return self._CashBpl
    @cCashBpl.setter
    def Prop06CashBpl(self,val):self._CashBpl=val

    @property
    def cCashMTM(self):return self._CashMTM
    @cCashMTM.setter
    def Prop07CashMTM(self,val):self._CashMTM=val

    @property
    def cLimitAgainstShares(self):return self._LimitAgainstShares
    @cLimitAgainstShares.setter
    def Prop08LimitAgainstShares(self,val):self._LimitAgainstShares=val

    @property
    def cCashPreviousSettlementExposure(self):return self._CashPreviousSettlementExposure
    @cCashPreviousSettlementExposure.setter
    def Prop09CashPreviousSettlementExposure(self,val):self._CashPreviousSettlementExposure=val

    @property
    def cIntradayMarginCash(self):return self._IntradayMarginCash
    @cIntradayMarginCash.setter
    def Prop10IntradayMarginCash(self,val):self._IntradayMarginCash=val

    @property
    def cFnoMTM(self):return self._FnoMTM
    @cFnoMTM.setter
    def Prop11FnoMTM(self,val):self._FnoMTM=val

    @property
    def cFnoPremium(self):return self._FnoPremium
    @cFnoPremium.setter
    def Prop12FnoPremium(self,val):self._FnoPremium=val

    @property
    def cFnoBpl(self):return self._FnoBpl
    @cFnoBpl.setter
    def Prop13FnoBpl(self,val):self._FnoBpl=val

    @property
    def cIntradayMarginFno(self):return self._IntradayMarginFno
    @cIntradayMarginFno.setter
    def Prop14IntradayMarginFno(self,val):self._IntradayMarginFno=val

    @property
    def cIntradayMarginComm(self):return self._IntradayMarginComm
    @cIntradayMarginComm.setter
    def Prop15IntradayMarginComm(self,val):self._IntradayMarginComm=val

    @property
    def cHoldFunds(self):return self._HoldFunds
    @cHoldFunds.setter
    def Prop16HoldFunds(self,val):self._HoldFunds=val

    @property
    def cTotal(self):return self._Total
    @cTotal.setter
    def Prop17Total(self,val):self._Total=val

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop18Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))

    def ByteToStruct(self,val):
        self.Prop01DataLenght=struct.unpack('I',val[10:14])
        self.Prop02CustomerID=struct.pack("B"*len(val[14:24]),*val[14:24]).decode('utf8')
        self.Prop03CurrentCashBalance=struct.unpack('i',val[24:28])
        self.Prop04PendingWithdrawalRequest=struct.unpack('i',val[28:32])
        self.Prop05NonCashLimit=struct.unpack('i',val[32:36])
        self.Prop06CashBpl=struct.unpack('i',val[36:40])
        self.Prop07CashMTM=struct.unpack('i',val[40:44])
        self.Prop08LimitAgainstShares=struct.unpack('i',val[44:48])
        self.Prop09CashPreviousSettlementExposure=struct.unpack('i',val[48:52])
        self.Prop10IntradayMarginCash=struct.unpack('i',val[52:56])
        self.Prop11FnoMTM=struct.unpack('i',val[56:60])
        self.Prop12FnoPremium=struct.unpack('i',val[60:64])
        self.Prop13FnoBpl=struct.unpack('i',val[64:68])
        self.Prop14IntradayMarginFno=struct.unpack('i',val[68:72])
        self.Prop15IntradayMarginComm=struct.unpack('i',val[72:76])
        self.Prop16HoldFunds=struct.unpack('i',val[76:80])
        self.Prop17Total=struct.unpack('i',val[80:84])
        self.Prop18Reserved=struct.pack("B"*len(val[84:184]),*val[84:184]).decode('utf8')

    def ToString(self):
         return ('DataLength = '+str(self.cDataLength) + "|" +'CustomerID = '+ str(self.cCustomerID) + "|" +'CurrentCashBalance = '+ str(self.cCurrentCashBalance) + "|" + 'PendingWithdrawalRequest ='+str(self.cPendingWithdrawalRequest) + "|" + 'NonCashLimit ='+str(self.cNonCashLimit) + "|" + 'CashBpl = '+str(self.cCashBpl)
                    + "|" +'CashMTM = '+ str(self.cCashMTM) + "|" + 'LimitAgainstShares = '+str(self.cLimitAgainstShares) + "|" + 'CashPreviousSettlementExposure = '+str(self.cCashPreviousSettlementExposure) + "|" +'IntradayMarginCash = '+ str(self.cIntradayMarginCash) + "|" +'FnoMTM = '+ str(self.cFnoMTM) + "|" +'FnoPremium = '+ str(self.cFnoPremium)
                    + "|" + 'FnoBpl = '+str(self.cFnoBpl) + "|" + 'IntradayMarginFno = '+str(self.cIntradayMarginFno) + "|" +'IntradayMarginComm = '+ str(self.cIntradayMarginComm))

class CommodityLimitReportItem():
    def __init__(self,transCode):
        self._DataLength=0
        self._CustomerID=None
        self._CCB=0
        self._WithDrawn=0
        self._NCL=0
        self._MarginforComm=0
        self._MMTMLoss=0
        self._Bpl=0
        self._HoldFunds=0
        self._NseWithdrawlBal=0
        self._PremiumForCurrency=0
        self._Reserved=None

    @property
    def cDataLength(self):return self._DataLength
    @cDataLength.setter
    def Prop01DataLength(self,val):self._DataLength=val

    @property
    def cCustomerID(self):return self._CustomerID
    @cCustomerID.setter
    def Prop02CustomerID(self,val):self._CustomerID=val+'\0'*(10-len(val))

    @property
    def cCCB(self):return self._CCB
    @cCCB.setter
    def Prop03CCB(self,val):self._CCB=val

    @property
    def cWithDrawn(self):return self._WithDrawn
    @cWithDrawn.setter
    def Prop04WithDrawn(self,val):self._WithDrawn=val

    @property
    def cNCL(self):return self._NCL
    @cNCL.setter
    def Prop05NCL(self,val):self._NCL=val

    @property
    def cMarginforComm(self):return self._MarginforComm
    @cMarginforComm.setter
    def Prop06MarginforComm(self,val):self._MarginforComm=val

    @property
    def cMMTMLoss(self):return self._MMTMLoss
    @cMMTMLoss.setter
    def Prop07MMTMLoss(self,val):self._MMTMLoss=val

    @property
    def cBpl(self):return self._Bpl
    @cBpl.setter
    def Prop08Bpl(self,val):self._Bpl=val

    @property
    def cHoldFunds(self):return self._HoldFunds
    @cHoldFunds.setter
    def Prop09HoldFunds(self,val):self._HoldFunds=val

    @property
    def cNseWithdrawlBal(self):return self._NseWithdrawlBal
    @cNseWithdrawlBal.setter
    def Prop10NseWithdrawlBal(self,val):self._NseWithdrawlBal=val

    @property
    def cPremiumForCurrency(self):return self._PremiumForCurrency
    @cPremiumForCurrency.setter
    def Prop11PremiumForCurrency(self,val):self._PremiumForCurrency=val

    @property
    def cReserved(self):return self._Reserved
    @cReserved.setter
    def Prop12Reserved(self,val):self._Reserved=val+'\0'*(100-len(val))

    def ByteToStruct(self,val):
        self.Prop01DataLenght=struct.unpack('I',val[10:14])
        self.Prop02CustomerID=struct.pack("B"*len(val[14:24]),*val[14:24]).decode('utf8')
        self.Prop03CCB=struct.unpack('I',val[24:28])
        self.Prop04WithDrawn=struct.unpack('I',val[28:32])
        self.Prop05NCL=struct.unpack('i',val[32:36])
        self.Prop06MarginforComm=struct.unpack('i',val[36:40])
        self.Prop07MMTMLoss=struct.unpack('i',val[40:44])
        self.Prop08Bpl=struct.unpack('i',val[44:48])
        self.Prop09HoldFunds=struct.unpack('I',val[48:52])
        self.Prop10NseWithdrawlBal=struct.unpack('I',val[52:56])
        self.Prop11PremiumForCurrency=struct.unpack('I',val[56:60])
        self.Prop12Reserved=struct.pack("B"*len(val[60:160]),*val[60:160]).decode('utf8')

    def ToString(self):
        return ('DataLength = '+str(self.cDataLength) + "|" +'CustomerID = '+ str(self.cCustomerID) + "|" +'CCB = '+ str(self.cCCB) + "|" + 'WithDrawn = '+str(self.cWithDrawn) + "|" +'NCL = '+ str(self.cNCL) + "|" +'MarginforComm = '+ str(self.cMarginforComm) + "|" +'MMTMLoss = '+ str(self.cMMTMLoss) + "|" +'Bpl = '+ str(self.cBpl) + "|" + 'HoldFunds = '+str(self.cHoldFunds)
                    + "|" + 'NseWithdrawlBal = '+str(self.cNseWithdrawlBal) + "|" + 'PremiumForCurrency = '+str(self.cPremiumForCurrency) + "|" + 'Reserved = '+str(self.cReserved))

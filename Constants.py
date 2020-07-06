import enum

class constants:
    Seperator = '|'
    SendTrail = 5
    MaxThreadWaitTime = 50
    TrailCountMain = 3		#No of times to try send data Main
    BytesOut = 0

    LogSeparator = "@"

    TAPHeaderSize = 22
    MinPacketSize = 60
    MinBcastpacket = 50



    SignOff = 190#185
    Contract = 28
    LegInfo = 80

    TapIp=None
    TapPort=8000
    LoginId=None
    MemberPassword=None
    TradingPassword=None
    MsgHeaderSize = 6
    LoginRequestSize = 196
    LoginResponseSize = 433
    LogOffRequestSize = 136
    #public static int OrderRequestSize = 357
    OrderItemSize = 227
    FeedRequestSize = 120
    ScripMasterRequest = 108
    ReportRequestSize = 181
    MarketDepthRequestSize = 121
    CommodityMasterSize = 235
    CurrencycripMasterSize = 329
    CashcripMasterSize = 184
    OrderRequestSize = 357
    DerivativeMasterItemSize = 217

    NFExCode = "NF"
    NCExcode = "NC"
    BCExcode = "BC"
    NXExcode = "NX"
    MXExcode = "MX"
    RNExCode = "RN"
    RMExcode = "RM"


    def __init__(self,TapIp=None,TapPort=0,LoginId=None,MemberPassword=None,TradingPassword=None):
        self._TapIp=TapIp
        self._TapPort=TapPort
        self._LoginId=LoginId
        self._MemberPassword=MemberPassword
        self._TradingPassword=TradingPassword

    @property
    def TapIp(self):return self._TapIp
    @property
    def TapPort(self):return self._TapPort
    @property
    def LoginId(self):return self._LoginId
    @property
    def MemberPassword(self):return self._MemberPassword
    @property
    def TradingPassword(self):return self._TradingPassword

    @TapIp.setter
    def TapIp(self,value):self._TapIp=value
    @TapPort.setter
    def TapPort(self,value):self._TapPort=value
    @LoginId.setter
    def LoginId(self,value):self._LoginId=value
    @MemberPassword.setter
    def MemberPassword(self,value):self._MemberPassword=value
    @TradingPassword.setter
    def TradingPassword(self,value):self._TradingPassword=value



    class TranCode(enum.IntEnum):
        LoginRequest = 1
        LogOffRequest = 2
        ScripMasterRequest = 21
        Invitation = 15000
        OrderRequest = 11
        FeedRequest = 22
        DepthRequest = 24
        SysInfoRequest = 1600
        SysInfoResponse = 1601
        PriceConfirmation = 2012

        #region New Order
        NewOrderRequest = 2000
        NewOrderConfirmation = 2073
        OrderFreeze = 2170
        NewOrderRejected = 2231
        #endregion

        #region Spread Order
        SpreadOrderRequest = 2100
        SpreadOrderRequestedResponse = 2101
        SpreadOrderConfirmationResponse = 2124
        SpreadOrderErrorResponse = 2154
        SpreadOrderConfirmCancellationResponse = 2130
        SpreadOrderModRequest = 2118
        SpreadOrderModAck = 2119
        SpreadOrderModConfirmResponse = 2136
        SpreadOrderModRejected = 2133
        SpreadOrderCancelRejected = 2127
        SpreadOrderCancelAck = 2107
        SpreadOrderCancelConfirmation = 2132
        #endregion

        #region Modify Order
        ModifyOrderRequest = 2040
        ModifyOrderAck = 2041
        ModifyOrderRejected = 2042
        ModifyOrderConfirmation = 2074
        #endregion

        #region Cancel Order
        CancelOrderRequest = 2070
        CancelOrderAck = 2071
        CancelOrderRejected = 2072
        CancelOrderConfirmation = 2075
        #endregion

        ExchPortfolioReq = 1775
        ExchportfolioResponse = 1776

        StopLossTriggered = 2212
        TradeConfirmation = 2222
        TradeError = 2223
        TradeCancellationRequest = 5440
        TradeCancellationRejected = 5441
        TradeModificationRequest = 5445

        MarketOpenMessage = 6511
        MarketCloseMessage = 6521
        MarketPreOpenShutDownMsg = 6531
        NormalMarketPreOpenEnd = 6571

        DeltaDownloadReq = 7000
        DeltaDownloadHeader = 7011   # Message Download Starts
        DeltaDownloadRecord = 7021   # Message Download Data Received
        DeltaDownloadTrailer = 7031  # Message Download End

        LocalDBUpdRequest = 7300
        LocalDBUpdData = 7304     # Local DB Data Received
        LocalDBUpdHeader = 7307    # Local DB Download Starts
        LocalDBUpdTrailer = 7308   # Local DB Download End

        SecurityStatus = 7320
        SysInfoPartialResponse = 7321

        BatchOrderCancel = 9002
        CtrlMsgToTrader = 5295
        TradeModifyConfirm = 2287
        TradeModifyReject = 2288
        TradeCancelConfirm = 2282
        TradeCancellationReject = 2286

        ExerPositionRequest = 4000
        ExcerPositionAck = 4001
        ExcerPoistionConfirm = 4002
        ExcerciseModification = 4005
        ExcerciseModificationConfirm = 4007
        ExerciseCancellationReq = 4008
        ExerciseCancelConfirm = 4010

        IndexMapTable = 7326



        #region 2L and 3L Orders
        OrderEntryRequest2L = 2102
        OrderEntryRequest3L = 2104
        OrderEntryAck2L = 2103
        OrderEntryAcl3L = 2105
        OrderConfirmation2L = 2125
        OrderConfirmation3L = 2126
        OrderError2L = 2155
        OrderError3L = 2156
        OrderCancelConfirm2L = 2131
        OrderCancelConfirm3L = 2132
        #endregion

        #region BroadCastTranscode

        BCastMessage = 6501
        BCastSecurityMstchg = 7305
        BCastParticipantMstChg = 7306
        BCastSecurityStatusChg = 7320
        BCastSecurityStatusChgPreOpen = 7210
        BCastTurnoverExceeded = 9010
        BCastBrokerReactivated = 9011
        BCastAuctionInqOut = 6582
        BCastAuctionStatusChg = 6581
        BCastOpenMsg = 6511
        BCastCloseMsg = 6521
        BCastPreOpenShutDownMsg = 6531
        BCastNormalMktPreopenEnded = 6571
        BCastTickerandMktIndex = 7202
        BcastMBOMBPUpdate = 7200
        BCastOnlyMBP = 7208
        BCastMWPoundRobin = 7201
        SecurityOpenPrice = 6013
        BCastCktCheck = 6541
        BCastIndices = 7207
        BCastIndustryIndices = 7203
        BCastBuyBack = 7211

        #endregion

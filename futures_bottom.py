from util import *
#url_base='http://192.168.104.132:8301'
url_base='http://192.168.105.155:8445'

## 下单
def placeOrder(data):
    url=url_base+'/bec/api/future/order/place?account='+str(data[0])
    datajson={}
    datajson["contractId"] = data[1]         ## 合约id
    datajson["marginRate"] = data[2]         ## 保证金率，全仓传0
    datajson["marginType"] = data[3]         ## 全仓逐仓类型，1全仓 2逐仓
    datajson["orderType"] = data[4]          ## 下单类型 1限价 3市价
    datajson["positionEffect"] = data[5]     ## 1开仓，2平仓
    datajson["price"] = data[6]              ## 下单价格
    datajson["quantity"] = data[7]           ## 下单数量
    datajson["side"] = data[8]               ## 买卖方向 1买，-1卖
    resp=httpPost(url,datajson)
    return resp

## 批量下单
def batchPlaceOrder(account,data):
    url=url_base+'/bec/api/future/order/place/batch?account='+str(account)
    datajson=data  ## 数据为下单数据的列表
    resp=httpPost(url,datajson)
    return resp

## 撤单
def cancelOrder(data):
    url=url_base+'/bec/api/future/order/cancel?account='+str(data[0])
    datajson={}
    datajson["contractId"] = data[1]           ## 合约id
    datajson["originalOrderId"] = data[2] ## uuid
    resp=httpPost(url,datajson)
    return resp

## 批量撤单
def batchCancelOrder(account,data):
    url=url_base+'/bec/api/future/order/cancel/batch?account='+str(account)
    datajson=data  ## 数据为撤单数据的列表
    resp=httpPost(url,datajson)
    return resp

## 一键撤单
def onekeyOrder(account,contractId):
    url=url_base+'/bec/api/future/order/cancel/onekey?account='+str(account)
    datajson=contractId
    resp=httpPost(url,datajson)
    return resp

## 调整保证金
def adjustMargin(data):
    url=url_base+'/bec/api/future/order/margin/adjust?account='+str(data[0])
    datajson={}
    datajson["contractId"] = data[1]           ## 合约id
    datajson["margin"] = data[2]                   ## 调整金额，可以正负，不能为0
    resp=httpPost(url,datajson)
    return resp

## 调整保证金率
def adjustMarginrate(data):
    url=url_base+'/bec/api/future/order/marginrate/adjust?account='+str(data[0])
    datajson={}
    datajson["contractId"] = data[1]           ## 合约id
    datajson["initMarginRate"] = data[2]   ## 保证金率，当全仓时传0
    datajson["marginType"] = data[3]           ## 全仓逐仓类型，1全仓 2逐仓
    resp=httpPost(url,datajson)
    return resp


## 资金红充蓝补
def adjustAsset(data):
    url=url_base+'/bec/api/future/asset/adjust?account='+str(data[0])
    datajson={}
    datajson["currencyId"] = data[1]           ## 合约id
    datajson["quantity"] = data[2]               ## 数量
    datajson["updateType"] = data[3]           ## 类型 1加钱 -1扣钱
    resp=httpPost(url,datajson)
    return resp

## 获取期货资产
def getAsset(account):
    url=url_base+'/bec/query/future/asset/get?account='+str(account)
    resp=httpGet(url)
    return resp


    # "currencyId": 2,
    # "totalBalance": "90.003696389131812342",
    # "available": "89.999386089131812342",
    # "frozenForTrade": "0.0000103",
    # "initMargin": "0.0043",
    # "frozenInitMargin": "0.00001",
    # "closeProfitLoss": "0.004464389131812342",
    # "realAvailable": null,
    # "fdProfitLoss": null,
    # "unavailableMargin": null,
    # "allFdProfitLossAll": null

## 获取当前委托
def getActive(account,contractid):
    url=url_base+'/bec/query/future/order/active/get?account='+str(account)+'&contractId='+str(contractid)
    resp=httpGet(url)
    return resp

    # "applId": 2,
    # "contractId": 1,
    # "accountId": 666666,
    # "clOrderId": "df978401-a1aa-42a2-98d9-588c2a0af550",
    # "side": 1,
    # "orderPrice": "1",
    # "orderQty": "1",
    # "orderId": "11597730694871455",
    # "orderTime": 1597802567648598,
    # "orderStatus": 2,
    # "matchQty": "0",
    # "matchAmt": "0",
    # "cancelQty": "0",
    # "matchTime": 0,
    # "orderType": 1,
    # "timeInForce": 0,
    # "feeRate": "0.0003",
    # "markPrice": null,
    # "avgPrice": "0",
    # "positionEffect": 1,
    # "marginType": 1,
    # "initMarginRate": "0.01",
    # "fcOrderId": "",
    # "contractUnit": "0.001",
    # "stopPrice": "0",
    # "orderSubType": 0,
    # "stopCondition": 0,
    # "minimalQuantity": null,
    # "deltaPrice": "0",
    # "frozenPrice": "1"

##
def getPosi(account):
    url=url_base+'/bec/query/future/posi/get?account='+str(account)
    resp=httpGet(url)
    return resp

    # "contractId": 1,
    # "posiQty": "1",
    # "openAmt": "0.43",
    # "initMargin": "0.0043",
    # "posiStatus": 0,
    # "marginType": 1,
    # "closeProfitLoss": "0",
    # "unrealizedProfitLoss": null,
    # "returnRate": null,
    # "forcedPrice": null,
    # "openPrice": null,
    # "tagPrice": null,
    # "initMarginRate": "0.01",
    # "contractUnit": null,
    # "contractSide": null,
    # "maintainMarginRate": "0.002",
    # "frozenCloseQty": "0",
    # "frozenOpenQty": "1",
    # "extraMargin": "0",
    # "billingCoinId": null

#获取指数、标记价格
def getQuot(contractId):
    url=url_base+'/bec/query/future/quot/get?account='+str(contractId)
    resp=httpGet(url)
    return resp

    # "messageType": 4,
    # "applId": 2,
    # "contractId": 1,
    # "symbol": "ETHUSDTsustainability",
    # "tradeDate": 20200819,
    # "time": 1597804126713787,
    # "lastPrice": "430",
    # "matchQty": "0",
    # "numTrades": 0,
    # "openPrice": "0",
    # "priceHigh": "0",
    # "priceLow": "0",
    # "historyPriceHigh": "447.52",
    # "historyPriceLow": "85.88",
    # "totalTurnover": "0",
    # "totalVolume": "0",
    # "totalBidVol": "178253709",
    # "totalAskVol": "177258706",
    # "prevPrice": "430",
    # "clearPrice": "420.80974971",
    # "prevClearPrice": "0",
    # "indexPrice": "420.80974971",
    # "deliveryPrice": "0",
    # "posiVol": "594264",
    # "fundingRate": "0",
    # "predictionFundingRate": "-0.0005",
    # "premiumIndex": "-0.997623629203721759",
    # "predictionPremiumIndex": "-0.211216591715302898",
    # "fairBasis": "0",
    # "priceChangeRadio": "0",
    # "priceChange": "-0.34",
    # "window24hPriceChangeRadio": null,
    # "window24hPriceChange": null,
    # "window24hTotalVolume": null,
    # "window24hTotalTurnover": null,
    # "lastUpdateId": 0,
    # "contractStatus": 2


# 查询数据
# 查询最新一条委托
def selectActive(account,n=0):
    tbname='core_order_future_'+str(account)[-1]
    sql='SELECT * FROM '+ tbname +' WHERE user_id='+str(account)+' ORDER BY uuid DESC '
    if n==1:
        sql=sql+'LIMIT 0,1 '
    result=operSql(sql,n)
    return result

# 查询一条委托条件为 uuid
def selectActiveByuuid(account,uuid):
    tbname='core_order_future_'+str(account)[-1]
    sql=('SELECT * FROM %s WHERE uuid=%s ' %(tbname,uuid))
    result = operSql(sql,1)
    return result



# 查询最新成交
def selectMatch(account,n=0):
    sql='SELECT * FROM core_match_future WHERE bid_user_id = '+str(account)+' or ask_user_id = '+str(account)+' ORDER BY match_time DESC '
    if n==1:
        sql=sql+'LIMIT 0,1 '
    result=operSql(sql,n)
    return result



# 查询持仓数据
def selectPosi(account,contract_id=0):
    place=''
    if contract_id!=0:
        place = ' AND contract_id=' + str(contract_id)
    sql='SELECT * FROM core_posi WHERE user_id = '+str(account)+'%s ORDER BY contract_id DESC ' %(place)
    result=operSql(sql,contract_id)
    return result

# 查询用户资产
def selectAccout(account,currency_id=2):
    sql='SELECT * FROM core_account_future WHERE user_id = '+str(account)+' AND currency_id='+str(currency_id)
    result=operSql(sql,currency_id)
    return result

# 获取所有合约
def selectContract(contract_id=0):
    place=''
    if contract_id!=0:
        place = ' WHERE contract_id = '+str(contract_id)
    sql='SELECT * FROM core_contract_future %s ORDER BY contract_id DESC ' %(place)
    result=operSql(sql,contract_id)
    return result

# 获取保证金
def selectMargin(variety_id,contract_id=0,user_id=0):
    sql='SELECT * FROM core_margin WHERE variety_id='+str(variety_id)+' AND contract_id='+str(contract_id)+' AND user_id='+str(user_id)+' ORDER BY posi_qty DESC '
    result=operSql(sql,contract_id)
    return result
##

def omnipotent(sql,standard,fname,dtype,msg):
    #print(sql)
    Actual = operSql(sql, 1)[fname]

    ActualToStandard(Actual,standard,dtype,fname,msg)


def ActualToStandard(Actual,standard,dtype,fname,msg):

    if Actual == None:
        Actual=0
    if dtype=='int':
        if int(Actual) != int(standard):
            print(fname,Actual,standard)
            msg[fname] = False
    elif dtype=='float':
        if round(float(Actual),8) != round(float(standard),8):
            print(fname,Actual, standard)
            msg[fname] = False
    elif dtype=='str':
        if str(Actual) != str(standard):
            print(fname,Actual, standard)
            msg[fname] = False




##  校验
def assetOmnipotent(user_id,msg):
    # core_contract_future获取
    contracts = selectContract()

    order_frozen_money_M=0
    # core_posi数据核对（基于core_match_future和core_order_future）
    for c in contracts:
        # 获取合约id
        contract_id = c['contract_id']
        contract_unit = c['contract_unit']
        # 查询core_posi表数据核对
        posi = selectPosi(user_id,contract_id)
        if posi ==None:
            continue

        open_amt = float(posi['open_amt'])   #开仓冻结保证金
        long_qty = int(posi['long_qty'])     #多头持仓量
        short_qty = int(posi['short_qty'])   #空头持仓量
        frozen_init_margin = posi['frozen_init_margin']   # 委托冻结保证金
        frozen_long_qty = int(posi['frozen_long_qty'])    # 多头委托冻结量
        frozen_short_qty = int(posi['frozen_short_qty'])  # 空头委托冻结量
        frozen_close_qty = int(posi['frozen_close_qty'])  # 平仓委托冻结量
        init_rate = float(posi['init_rate'])  #初始保证金率

        # 核对long_qty多头开仓量、short_qty空头持仓量
        posiQtySql = ("SELECT "
                   "((CASE WHEN m.bid IS NULL  THEN 0 ELSE m.bid END) - (CASE WHEN m.ask IS NULL  THEN 0 ELSE m.ask END)) qty "
                   "FROM "
                   "(SELECT "
                   "(SELECT SUM(match_qty) "
                   "FROM core_match_future "
                   "WHERE bid_user_id =  %s  AND contract_id = %s ) AS bid, "
                   "( SELECT SUM(match_qty) "
                   "FROM core_match_future "
                   "WHERE ask_user_id =  %s  AND contract_id =  %s ) as ask "
                   "FROM DUAL) m ;" % (user_id,contract_id,user_id,contract_id))
        posiQty = int( operSql(posiQtySql,1)['qty'])
        if posiQty == None :
            if long_qty!=0:
                msg['long_qty']= False
            if short_qty!=0:
                msg['short_qty'] = False
        elif posiQty>=0:
            if long_qty!= posiQty:
                msg['long_qty']= False
            if short_qty!=0:
                msg['short_qty'] = False
        else:
            if long_qty!= 0:
                msg['long_qty']= False
            if short_qty!=abs(posiQty):
                msg['short_qty'] = False
        # 核对open_amt 开仓冻结保证金数据
        # 获取core_match_future数据（这个地方的核算逻辑有问题）
        if posiQty == 0:
            if open_amt != 0:
                msg['open_amt'] = False
        else:
            matchSqlPlace = 'bid_user_id' if posiQty>0 else 'ask_user_id'
            matchSql = ('SELECT match_price,match_qty,match_amt FROM core_match_future WHERE '+ matchSqlPlace + '=%s  AND contract_id = %s ORDER BY update_time DESC ' %(user_id,contract_id))
            matchs = operSql(matchSql)
            open_amt_M = 0
            posiQty_L = posiQty
            for m in matchs:
                if m['match_qty'] > abs(posiQty_L):
                    open_amt_M += m['match_price']*posiQty_L
                    break
                else:
                    open_amt_M += float(m['match_amt'])
                    posiQty_L -= m['match_qty']
            ActualToStandard(open_amt,open_amt_M,'float','open_amt',msg)

        # 核对 frozen_init_margin委托冻结保证金
        orderTableName='core_order_future_'+ str(user_id)[-1]
        frozenInitMarginSql=('SELECT SUM(price*(quantity-filled_quantity)*%s*margin_rate) frozen_init_margin FROM %s ' \
                             'WHERE user_id=%s AND contract_id=%s AND order_status in (2,3)' %( contract_unit,orderTableName,user_id,contract_id) )
        omnipotent(frozenInitMarginSql, frozen_init_margin, 'frozen_init_margin', 'float', msg)
        # 核对 frozen_long_qty委托多头开仓数量
        frozenLongQtySql = ('SELECT SUM(quantity-filled_quantity) frozen_long_qty FROM %s ' \
                            'WHERE user_id=%s AND contract_id=%s AND order_status in (2,3) AND side=1 AND position_effect=1' %(orderTableName,user_id,contract_id))
        omnipotent(frozenLongQtySql,frozen_long_qty,'frozen_long_qty','int',msg)
        # 核对 frozen_short_qty委托多头开仓数量
        frozenShortQtySql = ('SELECT SUM(quantity-filled_quantity) frozen_short_qty FROM %s ' \
                            'WHERE user_id=%s AND contract_id=%s AND order_status in (2,3) AND side=-1 AND position_effect=1' %(orderTableName,user_id,contract_id))
        omnipotent(frozenShortQtySql,frozen_short_qty,'frozen_short_qty','int',msg)
        # 核对 frozen_close_qty委托平仓数量
        frozenCloseQtySql = ('SELECT SUM(quantity-filled_quantity) frozen_close_qty FROM %s ' \
                            'WHERE user_id=%s AND contract_id=%s AND order_status in (2,3) AND side=-1 AND position_effect=2' %(orderTableName,user_id,contract_id))
        omnipotent(frozenCloseQtySql, frozen_close_qty, 'frozen_close_qty', 'int', msg)

        orderFrozenMoneySql = (
                    'SELECT SUM(price*(quantity-filled_quantity)*maker_fee_ratio*%s) order_frozen_money FROM %s ' \
                    'WHERE user_id=%s  AND order_status in (2,3)  AND contract_id=%s AND position_effect=1' % (contract_unit,orderTableName, user_id,contract_id))
        middle = operSql(orderFrozenMoneySql,1)['order_frozen_money']
        #print(middle)
        order_frozen_money_M+= (middle if middle!=None else 0)



    ## core_account_future 对账
    posis = selectPosi(user_id)
    account = selectAccout(user_id)
    if account ==None:
        return msg
    #print(account)
    total_money = account['total_money']
    order_frozen_money = account['order_frozen_money'] #委托冻结手续费
    close_profit_loss = account['close_profit_loss'] #平仓盈亏
    cross_posi_amt = account['cross_posi_amt']  #全仓持仓金额
    cross_posi_margin = account['cross_posi_margin'] #全仓已占用保证金
    cross_frozen_posi_margin = account['cross_frozen_posi_margin'] #全仓已冻结保证金
    isolated_posi_amt = account['isolated_posi_amt'] #逐仓持仓金额
    isolated_posi_margin = account['isolated_posi_margin'] #逐仓已占用保证金
    isolated_frozen_posi_margin = account['isolated_frozen_posi_margin']  #逐仓已冻结保证金
    # 核对 total_money total_money
    totalMoneySql = ('SELECT '
                     '((SELECT' \
                      '((CASE WHEN m.a IS NULL  THEN 0 ELSE m.a END) - (CASE WHEN m.s IS NULL  THEN 0 ELSE m.s END )) transfer ' \
                      'FROM' \
                      '(SELECT ' \
                      '(SELECT  SUM(quantity) FROM core_transfer  WHERE user_id=%s AND from_appl_id=5 AND to_appl_id=2 AND currency_id=2) a, ' \
                      '(SELECT  SUM(quantity) FROM core_transfer  WHERE user_id=%s AND from_appl_id=2 AND to_appl_id=5 AND currency_id=2) s FROM DUAL )m)-' \
                      '(SELECT' \
                      '((CASE WHEN m.bid IS NULL  THEN 0 ELSE m.bid END) + (CASE WHEN m.ask IS NULL  THEN 0 ELSE m.ask END )+ ( CASE WHEN m.del IS NULL THEN 0 ELSE m.del END ) ) fee ' \
                      'FROM' \
                      '(SELECT (SELECT SUM(bid_fee) FROM core_match_future WHERE bid_user_id=%s) AS bid, (SELECT SUM(ask_fee) FROM core_match_future WHERE ask_user_id=%s) as ask, ' \
                      '(SELECT SUM(delivery_fee) FROM core_delivery WHERE user_id=%s) del FROM DUAL) m)) total_money ' \
                      'FROM DUAL;' %(user_id,user_id,user_id,user_id,user_id) )
    omnipotent(totalMoneySql, total_money, 'total_money', 'float', msg)

    # 核对 order_frozen_money委托冻结手续费
    ActualToStandard(order_frozen_money_M,order_frozen_money,'order_frozen_money', 'float', msg)

    # 核对 close_profit_loss平仓盈亏
    closeProfitLossSql = ('SELECT '
                          '(( CASE WHEN m.bid IS NULL THEN 0 ELSE m.bid END ) + ( CASE WHEN m.ask IS NULL THEN 0 ELSE m.ask END ) ) close_profit_loss '
                          'FROM '
                          '( SELECT '
                          '(SELECT SUM( bid_pnl ) FROM core_match_future WHERE bid_user_id = %s ) AS bid, '
                          '( SELECT SUM( ask_pnl ) FROM core_match_future WHERE ask_user_id = %s ) AS ask  '
                          'FROM DUAL ) m;' %(user_id,user_id))
    omnipotent(closeProfitLossSql, close_profit_loss, 'close_profit_loss', 'float', msg)

    # 核对 cross_posi_amt全仓持仓金额
    crossPosiAmtSql = ('SELECT SUM(open_amt) cross_posi_amt FROM core_posi WHERE user_id=%s AND margin_type=1' %(user_id))
    omnipotent(crossPosiAmtSql, cross_posi_amt, 'cross_posi_amt', 'float', msg)

    # 核对 cross_posi_margin全仓已占用保证金
    crossPosiMarginSql = ('SELECT SUM(init_margin+extra_margin) cross_posi_margin FROM core_posi WHERE user_id=%s AND margin_type=1' %(user_id))
    omnipotent(crossPosiMarginSql, cross_posi_margin, 'cross_posi_margin', 'float', msg)

    # 核对 cross_frozen_posi_margin全仓已冻结保证金
    crossFrozenPosiMarginSql = ('SELECT SUM(frozen_init_margin + frozen_extra_margin) cross_frozen_posi_margin FROM core_posi WHERE user_id=%s AND margin_type=1' %(user_id))
    omnipotent(crossFrozenPosiMarginSql, cross_frozen_posi_margin, 'cross_frozen_posi_margin', 'float', msg)

    # 核对 isolated_posi_amt逐仓持仓金额
    isolatedPosiAmtSql = ('SELECT SUM(open_amt) isolated_posi_amt  FROM core_posi WHERE user_id=%s AND margin_type=2' %(user_id))
    omnipotent(isolatedPosiAmtSql, isolated_posi_amt, 'isolated_posi_amt', 'float', msg)

    # 核对 isolated_posi_margin逐仓已占用保证金
    isolatedPosiMarginSql = ('SELECT SUM(init_margin+extra_margin) isolated_posi_margin FROM core_posi WHERE user_id=%s AND margin_type=2' %(user_id))
    print(isolatedPosiMarginSql)
    omnipotent(isolatedPosiMarginSql, isolated_posi_margin, 'isolated_posi_margin', 'float', msg)

    # 核对 isolated_frozen_posi_margin逐仓已冻结保证金
    isolatedFrozenPosiMarginSql = ('SELECT SUM(frozen_init_margin + frozen_extra_margin) isolated_frozen_posi_margin FROM core_posi WHERE user_id=%s AND margin_type=2' %(user_id))
    omnipotent(isolatedFrozenPosiMarginSql, isolated_frozen_posi_margin, 'isolated_frozen_posi_margin', 'float', msg)

    print(msg)
    return msg






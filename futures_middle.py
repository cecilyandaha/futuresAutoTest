import time

from futures_bottom import *
from util import *





## 委托测试接口
    # data[1]  contractId 合约id
    # data[2]  marginRate 保证金率，全仓传0
    # data[3]  marginType 全仓逐仓类型，1全仓 2逐仓
    # data[4]  orderType  下单类型 1限价 3市价
    # data[5]  positionEffect 1开仓，2平仓
    # data[6]  price 下单价格
    # data[7]  quantity 下单数量
    # data[8]  side 买卖方向 1买，-1卖

def activeOrderInterface(data,result):
    msg ={}
    respData={}
    #onekeyOrder(data[0],data[1])
    # 下单
    resp1 = placeOrder(data)
    orderjson = json.loads(resp1.text)
    if resp1.status_code!=200 :
        msg['下单']= False
        respData={'uuid':resp1.text['uuid']}

    else:
        resp2 = placeOrder(data)
        textjson = json.loads(resp2.text)

        # 下单成功后核对数据
        if resp2.status_code != 200 :
            msg['获取委托'] = False
        else:
            resp3= getActive(data[0],data[1])
            redisjson = json.loads(resp3.text)
            redisOrder=redisjson[0]
            mysqlOrder = selectActive(data[0], 1)
            contract = selectContract(data[1])
            if redisOrder['accountId'] != data[0] or mysqlOrder['user_id'] != data[0]:
                msg['accountId'] = False
            if redisOrder['contractId'] != data[1]or mysqlOrder['contract_id'] != data[1]:
                msg['contractId'] = False
            if data[3]==1:
                if float(redisOrder['initMarginRate']) != float(mysqlOrder['margin_rate']) :
                    msg['margin_rate'] = False
            else:
                if float(redisOrder['initMarginRate']) != float(mysqlOrder['margin_rate']) or float(redisOrder['initMarginRate']!=data[2])  :
                    msg['margin_rate'] = False
            if redisOrder['marginType'] != data[3] and mysqlOrder['margin_type'] != data[3]:
                msg['marginType'] = False
            if redisOrder['orderType'] != data[4] and mysqlOrder['order_type'] != data[4]:
                msg['orderType'] = False
            if redisOrder['positionEffect'] != data[5] and mysqlOrder['position_effect'] != data[5]:
                msg['positionEffect'] = False
            if redisOrder['orderPrice'] != data[6] and mysqlOrder['price'] != data[6]:
                msg['price'] = False
            if redisOrder['orderPrice'] != redisOrder['frozenPrice']:
                msg['orderPrice'] = False
            if redisOrder['orderQty'] != data[7] and mysqlOrder['quantity'] != data[7]:
                msg['quantity'] = False
            if redisOrder['side'] != data[8] and mysqlOrder['side'] != data[8]:
                msg['side'] = False
            if redisOrder['clOrderId'] != mysqlOrder['client_order_id'] :
                msg['client_order_id'] = False
            if redisOrder['orderId'] != mysqlOrder['uuid']:
                msg['uuid'] = False
            if redisOrder['orderTime'] != mysqlOrder['timestamp']:
                msg['timestamp'] = False
            if float(redisOrder['feeRate']) != float(contract['maker_fee_ratio']):
                msg['feeRate'] = False
            if float(redisOrder['contractUnit']) != float(contract['contract_unit']):
                msg['feeRate'] = False
            if float(redisOrder['orderStatus']) != 2:
                msg['orderStatus'] = False
    assetOmnipotent(data[0],msg)
    result['msg'] = msg
    return result,respData

        # "matchQty": "0",
        # "matchAmt": "0",
        # "cancelQty": "0",
        # "matchTime": 0,
        # "timeInForce": 0,
        # "markPrice": null,
        # "avgPrice": "0",
        # "fcOrderId": "",
        # "stopPrice": "0",
        # "orderSubType": 0,
        # "stopCondition": 0,
        # "minimalQuantity": null,
        # "deltaPrice": "0",
        # "frozenPrice": "1"


# 资金划转测试接口
def transferAssetInterface(data,result):
    ##划转
    msg={}
    resp = adjustAsset(data)
    if resp.status_code!=200 :
        msg['划转':False]
    assetOmnipotent(data[0],msg)
    result['msg'] = msg
    return result

# 撤单
# data [0] user_id,[1] contractId,[2] originalOrderId(uuid)
def cancelOrderInterface(data,result):
    # 撤单
    msg={}
    # 查询订单
    resp = cancelOrder(data)
    if resp.status_code!=200:
        msg['撤单':False]
    order2 = selectActiveByuuid(data[2])
    # 查询该订单数据 order_status 、quantity = canceled_quantity+filled_quantity、
    if order2['order_status'] !=5 or order2['order_status'] !=6:
        msg['order_status'] = False
    if int(order2['canceled_quantity'] + order2['filled_quantity']) != int(order2['quantity']):
        msg['order_status'] = False
    assetOmnipotent(data[0],msg)
    result['msg'] = msg
    return result

#  一键撤单

# 成交（先撤单，保证成交数据与原始数据一致）
def matchInterface(datalist,result):
    #撤单
    for data in datalist:
        # 依次撤单
        onekeyOrder(data[0],data[1])


    #用户下单
    for data in datalist:
        # 依次下单
        placeOrder(data)

    for data in datalist:
        #核对对应账户的成交的数据,对应order表数据的核对，match表对应数据的核对

        # 校验数据
        assetOmnipotent(data[0], datalist['msg'])
    return result

# 调整保证金率 
def adjustMarginRateInterfa(data,result):
    pass

    #确认是有持仓的而且已知持仓的方向

    #如果没有持仓下单造持仓

    #判定有持仓后 获取是全仓还是逐仓

    #如果是全仓 那进行全仓调整为逐仓的切换






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

def activeOrder(data,expect=0):
    result = True
    msg =''
    onekeyOrder(data[0],data[1])
    # 下单
    resp1 = placeOrder(data)
    orderjson = json.loads(resp1.text)
    if resp1.status_code!=200 or orderjson['code']!=0:
        msg='下单失败'
        result=False
    else:
        resp2 = placeOrder(data)
        textjson = json.loads(resp2.text)

        # 下单成功后核对数据
        if resp2.status_code != 200 or textjson['code'] != 0:
            msg='获取委托接口数据失败'
            result = False
        else:
            resp3= getActive(data[0],data[1])
            redisjson = json.loads(resp3.text)
            redisOrder=redisjson[0]
            mysqlOrder = selectActive(data[0], 1)
            contract = selectContract(data[1])
            if redisOrder['accountId'] != data[0] or mysqlOrder['user_id'] != data[0]:
                msg += 'accountId '
                result = False
            if redisOrder['contractId'] != data[1]or mysqlOrder['contract_id'] != data[1]:
                msg += 'contractId '
                result = False
            if data[3]==1:
                if float(redisOrder['initMarginRate']) != float(mysqlOrder['margin_rate']) :
                    msg += 'margin_rate '
                    result = False
            else:
                if float(redisOrder['initMarginRate']) != float(mysqlOrder['margin_rate']) or float(redisOrder['initMarginRate']!=data[2])  :
                    msg += 'margin_rate '
                    result = False
            if redisOrder['marginType'] != data[3] and mysqlOrder['margin_type'] != data[3]:
                msg += 'marginType '
                result = False
            if redisOrder['orderType'] != data[4] and mysqlOrder['order_type'] != data[4]:
                msg += 'orderType '
                result = False
            if redisOrder['positionEffect'] != data[5] and mysqlOrder['position_effect'] != data[5]:
                msg += 'positionEffect '
                result = False
            if redisOrder['orderPrice'] != data[6] and mysqlOrder['price'] != data[6]:
                msg += 'price '
                result = False
            if redisOrder['orderPrice'] != redisOrder['frozenPrice']:
                msg += 'orderPrice '
                result = False
            if redisOrder['orderQty'] != data[7] and mysqlOrder['quantity'] != data[7]:
                msg += 'quantity '
                result = False
            if redisOrder['side'] != data[8] and mysqlOrder['side'] != data[8]:
                msg += 'side '
                result = False
            if redisOrder['clOrderId'] != mysqlOrder['client_order_id'] :
                msg += 'client_order_id '
                result = False
            if redisOrder['orderId'] != mysqlOrder['uuid']:
                msg += 'uuid '
                result = False
            if redisOrder['orderTime'] != mysqlOrder['timestamp']:
                msg += 'timestamp '
                result = False
            if float(redisOrder['feeRate']) != float(contract['maker_fee_ratio']):
                msg += 'feeRate '
                result = False
            if float(redisOrder['contractUnit']) != float(contract['contract_unit']):
                msg += 'feeRate '
                result = False
    print(msg,result)
    return {'result':result,'msg':msg}

        # "orderStatus": 2,
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


#activeOrder([666666,1,0,1,1,1,1,1,1])





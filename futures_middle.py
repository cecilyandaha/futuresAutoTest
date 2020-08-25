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
    resp2 = placeOrder(data)
    if resp2.status_code!=200 :
        msg['下单']= False

    else:
        textjson = json.loads(resp2.text)
        respData = {'uuid': textjson['msg']}

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
        msg['划转']=False
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
        msg['撤单']=False
    time.sleep(2)
    order2 = selectActiveByuuid(data[2])
    # 查询该订单数据 order_status 、quantity = canceled_quantity+filled_quantity、
    if order2['order_status'] !=5 and order2['order_status'] !=6:
        msg['order_status'] = False
    if int(order2['canceled_quantity'] + order2['filled_quantity']) != int(order2['quantity']):
        msg['order_status'] = False
    assetOmnipotent(data[0],msg)
    result['msg'] = msg
    return result

# 一键撤单


# 整个合约撤单

# 成交（先撤单，保证成交数据与原始数据一致）
#orders={'bid':[bid_user_id,contractId,marginRate,marginType,orderType,positionEffect,price,quantity,side,bid_order_id],
#        'ask':[ask_user_id,contractId,marginRate,marginType,orderType,positionEffect,price,quantity,side,ask_order_id]}
# flag : 为1 表示orders[1]为bid，为0表示orders[0]为bid
def matchInterface(orders,flag,result):
    msg={}
    # #撤单
    # for data in [bid, ask]:
    #     resp = onekeyOrder(bid[0], bid[1])
    #     if resp.status_code != 200:
    #         # 这个写撤单失败的话直接结束流程以及给出错误提示
    #         pass
    #     data =   resp.text
    #用户下单
    if flag==0:
        bid = orders[0]
        ask = orders[1]
        bid[10] = 'taker_fee_ratio'
        ask[10] = 'maker_fee_ratio'
    if flag==1:
        bid = orders[1]
        ask = orders[0]
        bid[10] = 'maker_fee_ratio'
        ask[10] = 'taker_fee_ratio'
    for data in orders:
        # 依次下单
        resp = placeOrder(data)
        if resp.status_code!=200:
            #这个写下单失败的话直接结束流程以及给出错误提示
            pass
        else:
            textjson = json.loads(resp.text)
            respData = {'uuid': textjson['msg']}
            data.append(respData)
    #获取合约参数
    contract = selectContract(bid[1])
    #核对成交数据
    time.sleep(2)
    match = selectMatch(data[0][0])
    ActualToStandard(match['contract_id'],bid[1],'int','contract_id',msg)
    ActualToStandard(match['bid_user_id'], bid[0], 'int', 'bid_user_id', msg)
    ActualToStandard(match['ask_user_id'], ask[0], 'int', 'ask_user_id', msg)
    ActualToStandard(match['match_price'], min(bid[6],ask[6]), 'float', 'match_price', msg)
    ActualToStandard(match['match_qty'], min(bid[7],ask[7]), 'float', 'match_price', msg)
    ActualToStandard(match['bid_order_id'], bid[9], 'str', 'match_price', msg)
    ActualToStandard(match['ask_order_id'], ask[9], 'str', 'match_price', msg)
    ActualToStandard(match['match_amt'], min(bid[7],ask[7])*min(bid[6],ask[6])*contract['contract_unit'], 'float', 'match_amt', msg)
    ActualToStandard(match['bid_fee'], min(bid[7], ask[7]) * min(bid[6], ask[6]) * contract['contract_unit']*contract[bid[10]], 'float','bid_fee', msg)
    ActualToStandard(match['ask_fee'],min(bid[7], ask[7]) * min(bid[6], ask[6]) * contract['contract_unit'] * contract[ask[10]], 'float','ask_fee', msg)
    ActualToStandard(match['is_taker'], 1 if flag==0 else -1, 'int', 'is_taker', msg)
    ActualToStandard(match['bid_position_effect'], bid[5], 'int', 'bid_position_effect', msg)
    ActualToStandard(match['ask_position_effect'], ask[5], 'int', 'ask_position_effect', msg)
    ActualToStandard(match['bid_margin_type'], bid[3], 'int', 'bid_margin_type', msg)
    ActualToStandard(match['ask_margin_type'], ask[3], 'int', 'ask_margin_type', msg)
    ActualToStandard(match['bid_init_rate'], bid[4], 'float', 'bid_init_rate', msg)
    ActualToStandard(match['ask_init_rate'], ask[4], 'float', 'ask_init_rate', msg)
    # ActualToStandard(match['bid_match_type'], 0, 'int', 'bid_match_type', msg)
    # ActualToStandard(match['ask_match_type'], 0, 'int', 'ask_match_type', msg)

    assetOmnipotent(data[0], msg)
    return result
# CREATE TABLE `core_match_future` (
#   `appl_id` tinyint(2) NOT NULL COMMENT '应用标识',
#   `match_time` bigint(20) NOT NULL COMMENT '成交时间',
#   `exec_id` varchar(36) NOT NULL DEFAULT '' COMMENT '成交编号',
#   `bid_pnl_type` tinyint(2) DEFAULT NULL COMMENT '买方盈亏类型：0正常成交1正常平仓2强平3强减',
#   `ask_pnl_type` tinyint(2) DEFAULT NULL COMMENT '卖方盈亏类型：0正常成交1正常平仓2强平3强减',
#   `bid_pnl` decimal(36,18) DEFAULT NULL COMMENT '买方平仓盈亏',
#   `ask_pnl` decimal(36,18) DEFAULT NULL COMMENT '卖方平仓盈亏',
#   `bid_confiscated_amt` decimal(36,18) DEFAULT NULL COMMENT '买强平罚没金额',
#   `ask_confiscated_amt` decimal(36,18) DEFAULT NULL COMMENT '卖强平罚没金额

# 调整保证金率 
def adjustMarginRateInterfa(data,result):
    pass

    #确认是有持仓的而且已知持仓的方向

    #如果没有持仓下单造持仓

    #判定有持仓后 获取是全仓还是逐仓

    #如果是全仓 那进行全仓调整为逐仓的切换






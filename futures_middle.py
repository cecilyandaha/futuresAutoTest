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
    print(resp1.status_code)
    if resp1.status_code!=200 :
        msg['下单']= False

    else:
        resp2 = placeOrder(data)
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
def matchInterface(bid,ask,result):
    msg={}
    #撤单
    for data in [bid, ask]:
        resp = onekeyOrder(bid[0], bid[1])
        if resp.status_code != 200:
            # 这个写撤单失败的话直接结束流程以及给出错误提示
            pass
    #用户下单
    for data in [bid,ask]:
        # 依次下单
        resp = placeOrder(data)
        if resp.status_code!=200:
            #这个写下单失败的话直接结束流程以及给出错误提示
            pass
    #核对成交数据
    match = selectMatch(data[0][0])
    contract_id =1



    assetOmnipotent(data[0], msg)
    return result
# CREATE TABLE `core_match_future` (
#   `appl_id` tinyint(2) NOT NULL COMMENT '应用标识',
#   `match_time` bigint(20) NOT NULL COMMENT '成交时间',
#   `contract_id` int(11) NOT NULL DEFAULT '0' COMMENT '交易对ID、合约号',
#   `exec_id` varchar(36) NOT NULL DEFAULT '' COMMENT '成交编号',
#   `bid_user_id` int(11) NOT NULL DEFAULT '0' COMMENT '买方账号ID',
#   `ask_user_id` int(11) NOT NULL DEFAULT '0' COMMENT '卖方账号ID',
#   `bid_order_id` varchar(36) NOT NULL DEFAULT '' COMMENT '买方委托号',
#   `ask_order_id` varchar(36) NOT NULL DEFAULT '' COMMENT '卖方委托号',
#   `match_price` decimal(36,18) DEFAULT NULL COMMENT '成交价',
#   `match_qty` decimal(36,18) DEFAULT NULL COMMENT '成交数量',
#   `match_amt` decimal(36,18) DEFAULT NULL COMMENT '成交金额',
#   `bid_fee` decimal(36,18) DEFAULT NULL COMMENT '买方手续费',
#   `ask_fee` decimal(36,18) DEFAULT NULL COMMENT '卖方手续费',
#   `is_taker` tinyint(2) DEFAULT NULL COMMENT 'Taker方向',
#   `update_time` bigint(20) DEFAULT NULL COMMENT '最近更新时间',
#   `bid_position_effect` tinyint(2) DEFAULT NULL COMMENT '买方开平标志',
#   `ask_position_effect` tinyint(2) DEFAULT NULL COMMENT '卖方开平标志',
#   `bid_margin_type` tinyint(2) DEFAULT NULL COMMENT '买方保证金类型',
#   `ask_margin_type` tinyint(2) DEFAULT NULL COMMENT '卖方保证金类型',
#   `bid_init_rate` decimal(36,18) DEFAULT NULL COMMENT '买方初始保证金率',
#   `ask_init_rate` decimal(36,18) DEFAULT NULL COMMENT '卖方初始保证金率',
#   `bid_match_type` tinyint(2) DEFAULT NULL COMMENT '买方成交类型：0普通成交1强平成交2强减成交（破产方）3强减成交（盈利方）',
#   `ask_match_type` tinyint(2) DEFAULT NULL COMMENT '卖方成交类型：0普通成交1强平成交2强减成交（破产方）3强减成交（盈利方）',
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






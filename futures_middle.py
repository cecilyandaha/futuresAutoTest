import time
from decimal import Decimal

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
    msg = {'用户':data[0]}
    respData={}
    #onekeyOrder(data[0],data[1])
    # 下单
    resp1 = placeOrder(data)
    if resp1['code']!=200 :
        msg['下单']= resp1['text']['msg']

    else:
        respData = {'uuid': resp1['text']['msg']}
        resp3 = getActive(data[0], data[1])

        # 下单成功后核对数据
        if resp3['code']!= 200 :
            msg['获取委托'] = False
        else:
            redisjson = resp3['text']
            redisOrder=redisjson[0]
            mysqlOrder = selectActive(data[0], 1)
            contract = selectContract(data[1])
            if redisOrder['accountId'] != data[0] or mysqlOrder['user_id'] != data[0]:
                msg['accountId'] = False
            if redisOrder['contractId'] != data[1] or mysqlOrder['contract_id'] != data[1]:
                msg['contractId'] = False
            if data[3]==1:
                ActualToStandard(redisOrder['initMarginRate'], mysqlOrder['margin_rate'], 'float', 'margin_rate', msg)
            else:
                ActualToStandard(redisOrder['initMarginRate'], mysqlOrder['margin_rate'], 'float', 'margin_rate', msg)
                ActualToStandard(redisOrder['initMarginRate'], data[2], 'float', 'margin_rate', msg)
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
    result['respData']=respData
    return result

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
    msg = {'用户': data[0]}
    resp = adjustAsset(data)
    if resp['code']!=200 :
        msg['划转']=resp['text']['msg']
    assetOmnipotent(data[0],msg)
    result['msg'] = msg
    return result

# 撤单
# data [0] user_id,[1] contractId,[2] originalOrderId(uuid)
def cancelOrderInterface(data,result):
    # 撤单
    msg = {'用户': data[0]}
    # 查询订单
    resp = cancelOrder(data)
    if resp['code']!=200:
        msg['撤单']=resp['text']['msg']
    time.sleep(2)
    order2 = selectActiveByuuid(data[0],data[2])
    # 查询该订单数据 order_status 、quantity = canceled_quantity+filled_quantity、
    if order2['order_status'] !=5 and order2['order_status'] !=6:
        msg['order_status'] = False
    if int(order2['canceled_quantity'] + order2['filled_quantity']) != int(order2['quantity']):
        msg['order_status'] = False
    assetOmnipotent(data[0],msg)
    result['msg'] = msg
    return result

# 一键撤单
def onekeyOrderInterface(account,contractId,result):
    msg = {'用户':account}
    resp = onekeyOrder(account,contractId)
    # print(resp.status_code)
    # print(resp.text)
    if resp['code']!=200:
        msg['撤单'] = resp['text']['msg']
    else:
        resp = getActive(account,contractId)
        if resp['text']!=[]:
            msg['撤单'] = False
        assetOmnipotent(account, msg)
    result['msg'] = msg
    return result


# 整个合约撤单
def cancelAllOrderInterface(contractId,result):
    msg={}
    # 查询所有有过该合约持仓的用户
    users = selectPosiUsers(contractId)
    for user in users:
        resp = onekeyOrder(user['user_id'],contractId)
        if resp['code']!=200:
            msg['用户'+str(user['user_id']+'撤单')]=resp['text']['msg']
        assetOmnipotent(user['user_id'], msg)
    result['msg'] = msg
    return result


# 成交（先撤单，保证成交数据与原始数据一致）
#orders=[[bid_user_id,contractId,marginRate,marginType,orderType,positionEffect,price,quantity,side,bid_order_id],
#        [ask_user_id,contractId,marginRate,marginType,orderType,positionEffect,price,quantity,side,ask_order_id]]
# flag : 为-1 表示orders[0]为买方，为1表示orders[0]为卖方
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
    if flag==-1:
        bid = orders[0]
        ask = orders[1]
        bid.append('maker_fee_ratio')
        ask.append('taker_fee_ratio')
    if flag==1:
        bid = orders[1]
        ask = orders[0]
        bid.append('taker_fee_ratio')
        ask.append('maker_fee_ratio')
    for data in orders:
        # 依次下单
        resp = placeOrder(data)
        # print(resp)
        if resp['code']!=200:
            msg['用户'+str(data[0])+'下单']=resp['text']['msg']
            data.append(0)
        else:
            data.append(resp['text']['msg'])
    #获取合约参数
    contract = selectContract(bid[1])
    #核对成交数据
    time.sleep(2)
    match = selectMatch(bid[0],1)
    ActualToStandard(match['contract_id'],bid[1],'int','contract_id',msg)
    ActualToStandard(match['bid_user_id'], bid[0], 'int', 'bid_user_id', msg)
    ActualToStandard(match['ask_user_id'], ask[0], 'int', 'ask_user_id', msg)
    ActualToStandard(match['match_price'], min(bid[6],ask[6]), 'float', 'match_price', msg)
    ActualToStandard(match['match_qty'], min(bid[7],ask[7]), 'float', 'match_qty', msg)
    ActualToStandard(match['bid_order_id'], bid[10], 'str', 'bid_order_id', msg)
    ActualToStandard(match['ask_order_id'], ask[10], 'str', 'ask_order_id', msg)
    ActualToStandard(match['match_amt'], min(bid[7],ask[7])*min(bid[6],ask[6])*contract['contract_unit'], 'float', 'match_amt', msg)
    ActualToStandard(match['bid_fee'], min(bid[7], ask[7]) * min(bid[6], ask[6]) * contract['contract_unit']*contract[bid[9]], 'float','bid_fee', msg)
    ActualToStandard(match['ask_fee'],min(bid[7], ask[7]) * min(bid[6], ask[6]) * contract['contract_unit'] * contract[ask[9]], 'float','ask_fee', msg)
    ActualToStandard(match['is_taker'], flag, 'int', 'is_taker', msg)
    ActualToStandard(match['bid_position_effect'], bid[5], 'int', 'bid_position_effect', msg)
    ActualToStandard(match['ask_position_effect'], ask[5], 'int', 'ask_position_effect', msg)
    ActualToStandard(match['bid_margin_type'], bid[3], 'int', 'bid_margin_type', msg)
    ActualToStandard(match['ask_margin_type'], ask[3], 'int', 'ask_margin_type', msg)
    ## 逐仓的时候进行了核对 全仓时没有核对
    if bid[3]==2:
        ActualToStandard(match['bid_init_rate'], bid[4], 'float', 'bid_init_rate', msg)
    if ask[3]==2:
        ActualToStandard(match['bid_init_rate'], bid[4], 'float', 'bid_init_rate', msg)
    # ActualToStandard(match['bid_match_type'], 0, 'int', 'bid_match_type', msg)
    # ActualToStandard(match['ask_match_type'], 0, 'int', 'ask_match_type', msg)
    msg['用户'] = ask[0]
    assetOmnipotent(ask[0], msg)
    msg['用户'] = bid[0]
    assetOmnipotent(bid[0], msg)
    result['msg'] = msg
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
#     account=data[0]                      用户id
#     datajson["contractId"] = data[1]     合约id
#     datajson["initMarginRate"] = data[2] 保证金率，当全仓时传0
#     datajson["marginType"] = data[3]     全仓逐仓类型，1全仓 2逐仓
def adjustMarginRateInterface(data,result):
    msg = {'用户':data[0]}
    #调整保证金
    resp = adjustMarginrate(data)
    if resp['code']!=200:
        msg['调整保证金率']=resp['text']['msg']
    #获取持仓数据核对
    posi = selectPosi(data[0], data[1])
    if data[3] ==1:
        ActualToStandard(posi['margin_type'], data[3], 'int', 'marginType', msg)
    elif data[3] ==2:
        ActualToStandard(posi['init_rate'], data[2], 'float', 'initMarginRate', msg)
        ActualToStandard(posi['margin_type'], data[3], 'int', 'marginType', msg)
    assetOmnipotent(data[0], msg)
    result['msg'] = msg
    return result

# 调整保证金
#     account = data[0]
#     datajson["contractId"] = data[1]    ## 合约id
#     datajson["margin"] = data[2]        ## 调整金额，可以正负，不能为0
def adjustMarginInterface(data,result):
    msg = {'用户':data[0]}
    #获取持仓数据
    posi1 = selectPosi(data[0], data[1])
    #调整保证金
    resp = adjustMargin(data)
    if resp['code']!=200:
        msg['调整保证金']=resp['text']['msg']
    #获取持仓数据核对 init_margin不变 ，extra_margin2=extra_margin1+data[2]
    posi2 = selectPosi(data[0], data[1])
    ActualToStandard(posi2['extra_margin'], posi1['extra_margin']+data[2], 'int', 'marginType', msg)
    assetOmnipotent(data[0], msg)
    result['msg'] = msg
    return result

# 持仓数据获取
def getPosiInterface(account,contractId):
    posi = selectPosi(account,contractId)
    posi['init_margin'] = float(posi['init_margin'])
    posi['extra_margin'] = float(posi['extra_margin'])
    posi['init_rate'] = float(posi['init_rate'])
    posi['warning_rate'] = float(posi['warning_rate'])
    posi['maintain_rate'] = float(posi['maintain_rate'])
    posi['open_amt'] = float(posi['open_amt'])
    posi['long_qty'] = int(posi['long_qty'])
    posi['short_qty'] = int(posi['short_qty'])
    posi['frozen_long_qty'] = int(posi['frozen_long_qty'])
    posi['frozen_short_qty'] = int(posi['frozen_short_qty'])
    posi['frozen_short_qty'] = int(posi['frozen_close_qty'])
    # print(posi)
    return posi

# 检查合约持仓是否处于强平状态
def isFlatInterface(account,contract_id):
    posi = selectPosi(account,contract_id)

    return posi['posi_status']

# 强平价格验证流程
def forceFlatPriceInterface(accountId,result):
    msg={}
    flPrices=[]
    # 获取基础数据posi、account、指数、标记价格
    account = selectAccout(accountId)
    prices = getAllPrice()
    posi = selectPosi(accountId)
    contracts = selectContract()

    #通过公式计算出强平价格
    #逐仓强平价格 = 合约持仓均价-合约方向*(逐仓开仓保证金+逐仓额外保证金-逐仓持仓维持保证金)/（合约张数*合约单位）
    #全仓强平价格 = 合约持仓均价-合约方向*(账户余额-逐仓冻结保证金-逐仓占用保证金-冻结手续费+全仓浮动盈亏（除本合约以外）-全仓持仓维持保证金-全仓委托维持保证金)/（合约张数*合约单位）
    # 计算所有合约的浮动盈亏
    # 计算所有合约的维保

    for p in posi:
        contract = selectContract(p['contract_id'])
        flPrice=0
        # 如果该合约有持仓就进行计算
        if (p['long_qty']+p['short_qty'])!=0:
            # 该合约为逐仓
            if p['margin_type'] == 2:
                flPrice = p['open_amt'] / (p['long_qty'] + p['short_qty'])/contract['contract_unit'] - (
                            p['init_margin'] + p['extra_margin'] - p['maintain_rate'] * p['open_amt']) / (
                                      p['long_qty'] - p['short_qty']) / contract['contract_unit']
            # 该合约为全仓
            elif p['margin_type'] == 1:
                #计算浮动盈亏和委托维保
                float_profit_loss = 0 #浮动盈亏
                posi_maintain_margin = 0 #持仓维保
                active_maintain_margin = 0 #委托维保
                # 一次遍历每个合约
                for pos in posi:
                    # 如果是全仓合约
                    if pos['margin_type'] == 1:
                        conc = selectContract(pos['contract_id'])
                        # 如果有持仓计算浮动盈亏
                        if (pos['long_qty'] + pos['short_qty']) != 0 :
                            posi_maintain_margin+=p['maintain_rate'] * p['open_amt']
                            if pos['contract_id']!=p['contract_id']:
                                float_profit_loss += (pos['open_amt'] / (pos['long_qty'] + pos['short_qty']) / conc[
                                    'contract_unit'] \
                                                      - Decimal.from_float(prices[pos['contract_id']]['clearPrice'])) \
                                                     * conc['contract_unit'] * (pos['long_qty'] - pos['short_qty'])

                        # 如果有委托计算委托维保
                        if (pos['frozen_long_qty'] + pos['frozen_short_qty']) != 0:
                            actives = selectActives(accountId,pos['contract_id'])
                            for active in actives:
                                active_maintain_margin+=(active['quantity']-active['filled_quantity'])*active['price']* conc['contract_unit']*pos['maintain_rate']
                flPrice = p['open_amt'] / (p['long_qty'] + p['short_qty'])/contract['contract_unit'] \
                          - (account['total_money'] + account['close_profit_loss']
                             - account['isolated_frozen_posi_margin'] - account['isolated_posi_margin']
                             - account['order_frozen_money'] + float_profit_loss-active_maintain_margin- posi_maintain_margin)\
                             /(p['long_qty'] - p['short_qty']) / contract['contract_unit']
        flPrices.append({'contract_id':p['contract_id'],'flPrice':float(flPrice),'side': ( 1 if p['long_qty']!=0 else -1)
                            ,'variety':contract['variety_id'],'clearPrice':prices[p['contract_id']]['clearPrice']})
    result['flPrices']=flPrices
    return result

## 强平验证流程
def foreFlatInterface(accountId,flPrices,result):
    msg={}
    #强平验证流程
    for f in flPrices:
        #指数推送到接近强平价格但不触发强平，做边界值校验
        #判断方向
        ctrprice=0
        if f['side'] == 1:
            #做多持仓调整指数价格为flPrice+0.001
            ctrprice = round(f['flPrice'] + 0.001, 4)
        if f['side'] == -1:
            #做空持仓调整指数价格为flPrice-0.001
            ctrprice = round(f['flPrice'] - 0.001, 4)
        for i in range(3):
            controlIndexPrice(f['variety'], ctrprice)
            time.sleep(3)
            if ctrprice == getPrice(f['contract_id'])['clearPrice']:
                break
            elif i == 2:
                msg['指数设置到强平边界值'+str(f['contract_id'])]=False
                result['msg'] = msg
                return result
        if isFlatInterface(accountId,f['contract_id'])!=0:
            msg['强平边界值验证']=False
            result['msg'] = msg
            return result
        #指数推送到强平价格
        #判断方向
        ctrprice=0
        if f['side'] == 1:
            #做多持仓调整指数价格为flPrice+0.001
            ctrprice = round(f['flPrice'] - 0.00001, 6)
        if f['side'] == -1:
            #做空持仓调整指数价格为flPrice-0.001
            ctrprice = round(f['flPrice'] + 0.00001, 6)
        for i in range(3):
            controlIndexPrice(f['variety'], ctrprice)
            time.sleep()
            if ctrprice == getPrice(f['contract_id'])['clearPrice']:
                break
            elif i == 2:
                msg['指数设置到强平价格'+str(f['contract_id'])]=False
                result['msg'] = msg
                return result
        if isFlatInterface(accountId,f['contract_id'])!=1:
            msg['强平验证']=False
            result['msg'] = msg
            return result
        for i in range(3):
            controlIndexPrice(f['variety'], f['clearPrice'])
            time.sleep()
            if f['clearPrice'] == getPrice(f['contract_id'])['clearPrice']:
                break
            elif i == 2:
                msg['指数从强平设置回原值'+str(f['contract_id'])]=False
                result['msg'] = msg
                return result
    return result





#指数推送到强平价格，读取core_












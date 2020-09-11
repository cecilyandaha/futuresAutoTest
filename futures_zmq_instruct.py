import json

import zmq


def getBigNumber(number):
    return str(int(number * 1000000000000000000))

def to_decimal(f, p = 6):
    i = round(f * pow(10, p))                 #pow(10,i)的意思就是10的i次幂，round() 方法返回浮点数x的四舍五入值
    return str(round(i * pow(10, 18 - p)))



#参数更新推送
def paramRefresh5009():
    datajson={}
    datajson['message_type'] = 5009
    datajson['appl_id'] = 2
    return datajson

def paramRefresh5018():
    datajson={}
    datajson['message_type'] = 5018
    datajson['appl_id'] = 2
    return datajson

#罚没账户参数更新
def core_super_userRefresh():
    datajson={}
    datajson['message_type'] = 5009
    datajson['appl_id'] = 2
    datajson['load_type'] = 2
    return datajson

#保证金修改指令
def core_marginRefresh():
    datajson={}
    datajson['message_type'] = 5012
    datajson['appl_id'] = 2
    datajson['account_id'] = 0
    datajson['variety_id'] = 12
    datajson['contract_id'] = 0
    return datajson

if __name__ == '__main__':
    TRADE_SERVER_URL = 'tcp://192.168.1.211:20060'
    #TRADE_client_URL = 'tcp://192.168.1.150:20050'
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect(TRADE_SERVER_URL)
    datajson = core_marginRefresh()
    str_json = json.dumps(datajson).encode('utf-8')
    print(str_json)
    socket.send(str_json)
    ret = socket.recv()
    print(ret)


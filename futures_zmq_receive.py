#-*-coding:utf-8-*- 3
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE,b'')
#socket.connect("tcp://192.168.1.211:20064")
socket.connect("tcp://192.168.1.211:20051")

while True:
    json = eval(socket.recv())
    if json['message_type']==7 and json['contract_id']==94 :
        print ('k线%s' %(json))
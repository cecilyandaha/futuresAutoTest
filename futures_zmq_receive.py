#-*-coding:utf-8-*- 3
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE,b'')
socket.connect("tcp://192.168.1.211:20061")

while True:
    json = eval(socket.recv())
    if json['message_type']==4:
        print (json['index_price'])
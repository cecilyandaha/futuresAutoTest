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
    if json['message_type'] not in [4,7,13]:
           print (json)
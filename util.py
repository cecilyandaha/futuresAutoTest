import configparser
import random
#import numpy as np
import time

import requests
import json
#np.set_printoptions(suppress=True)
import pymysql

header1={'Content-Type':'application/json'}

#数据放大10的18倍
def big18():
    pass

#http get请求
def httpGet(url,header=None):
    if header==None:
        header=header1
    resp=requests.get(url=url,headers=header)
    if resp.status_code==200:
        if resp.text['code'] != 0 :
            resp.status_code == 400
    time.sleep(1)
    return resp

#http post请求
def httpPost(url,data,header=None):
    if header==None:
        header=header1
    resp=requests.post(url=url,data=json.dumps(data), headers=header)
    if resp.status_code==200:
        if resp.text['code'] != 0 :
            resp.status_code == 400
    time.sleep(1)
    return resp

#操作数据库
def operSql(sql,n=0):
    config = configparser.ConfigParser()
    config.read("conf.ini")
    host = config['Mysql']['host']
    username = config['Mysql']['username']
    psw = config['Mysql']['psw']
    dbname = config['Mysql']['dbname']
    port = int(config['Mysql']['port'])
    # 打开数据库连接
    db = pymysql.connect(host, username, psw, dbname,port)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据.
    if n==0:
        results = cursor.fetchall()
        rs=[]
        for r in results:
            rs.append(r)
    else:
        rs = cursor.fetchone()
    # 关闭数据库连接
    db.close()
    return rs




# for i in range(10):
#     print( str(random.random()*10**18))
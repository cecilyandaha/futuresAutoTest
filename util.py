import configparser
import random
#import numpy as np
import time
import redis

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
    resdata={'code':resp.status_code,'text':json.loads(resp.text)}
    return resdata

#http post请求
def httpPost(url,data,header=None):
    if header==None:
        header=header1
    resp=requests.post(url=url,data=json.dumps(data), headers=header)
    resdata={}
    if resp.status_code==200:
        resdata['code'] = 200
        if json.loads(resp.text)['code'] != 0 :
            resdata['code']=400
    else:
        resdata['code']=400
    text = json.loads(resp.text)
    resdata['text'] = text
    time.sleep(2)
    return resdata

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


# 操作redis
def operateRedis(operate,key,value=0,db=0,):
    config = configparser.ConfigParser()
    config.read("conf.ini")
    host = config['Redis']['host']
    port = int(config['Redis']['port'])
    password = config['Redis']['password']
    r = redis.Redis(host=host, port=port, password=password,db=db)
    if operate=='get':
        backdata = r.get(key)
        return backdata
    elif operate=='set':
        r.set(key, value)
        return True
    return None



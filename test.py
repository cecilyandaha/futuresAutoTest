

import time


# 定义装饰器
def time_calc(func):
    def wrapper(id,*args, **kargs):
        print(id)
        start_time = time.time()
        f = func(id,*args,**kargs)
        exec_time = time.time() - start_time
        return f
    return wrapper

# 使用装饰器
@time_calc
def add(id,a, b):
    return a + b

@time_calc
def sub(id,a, b):
    return a - b

#print(add(666666,1,2))
# posiQty=-1
# aaa='bid_user_id' if posiQty<0 else 'ask_user_id'
# print(aaa)
a=[2,2,2]
b=[5,5,5]
for i in [a,b]:
    i.append(1)
print(a)
print(b)
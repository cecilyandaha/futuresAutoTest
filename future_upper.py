from futures_middle import  *

#result = matchInterface([[666666,2,0,1,1,1,11650,1,1],[666667,2,0,1,1,1,11650,1,-1]],-1,{'测试项':'成交'})
# print(result)

# result = activeOrderInterface([668802,2,0.1,2,1,1,11600,1,1],{'测试项':'逐仓做多委托1'})
# print(result)
# result = activeOrderInterface([668802,2,0.1,2,1,1,11600,1,1],{'测试项':'逐仓做多委托2'})
# print(result)

# result = onekeyOrderInterface(668802,1,{'测试项':'一键撤单'})
result = cancelAllOrderInterface(1,{'测试项':'一键撤单'})
print(result)
#result = matchInterface([[668802,1,0.1,2,1,1,400,1,1],[668803,1,0.1,2,1,1,400,1,-1]],-1,{'测试项':'全仓持仓成交'})
#print(result)
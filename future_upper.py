from futures_middle import *

# # 红冲蓝补
# # 蓝补
# result = transferAssetInterface([668802,2,200000,1],{'测试项':'蓝补资金'})
# print(result)
# # 红冲
# result = transferAssetInterface([668803,2,99000,-1],{'测试项':'红冲资金'})
# print(result)
#
# # 限价委托多次下单：委托流程5
# result = activeOrderInterface([668802,1,0,1,1,1,100,1,1],{'测试项':'限价全仓做多委托1'})
# print(result)
# result = activeOrderInterface([668802,1,0,1,1,1,110,1,1],{'测试项':'限价全仓做多委托2'})
# print(result)
#
# # 限价委托多次下单：委托流程6
# result = activeOrderInterface([668802,1,0,1,1,1,800,1,-1],{'测试项':'限价全仓做空委托1'})
# print(result)
# result = activeOrderInterface([668802,1,0,1,1,1,800,1,-1],{'测试项':'限价全仓做空委托2'})
# print(result)
#
# # 限价委托多次下单：委托流程7
# result = activeOrderInterface([668802,2,0.4,2,1,1,11600,1,1],{'测试项':'逐仓做多委托1'})
# print(result)
# result = activeOrderInterface([668802,2,0.4,2,1,1,11600,1,1],{'测试项':'逐仓做多委托2'})
# print(result)
#
# # 限价委托多次下单：委托流程8
# result = activeOrderInterface([668802,2,0.4,2,1,1,11900,1,-1],{'测试项':'逐仓做空委托1'})
# print(result)
# result = activeOrderInterface([668802,2,0.4,2,1,1,11900,1,-1],{'测试项':'逐仓做空委托2'})
# print(result)
#
# # 无委托限价下单：委托流程1
# result = onekeyOrderInterface(668802,0,{'测试项':'一键撤单'})
# print(result)
# result = activeOrderInterface([668802,1,0,1,1,1,200,1,1],{'测试项':'全仓做多委托'})
# print(result)
#
# # 无委托限价下单：委托流程2
# result = onekeyOrderInterface(668802,0,{'测试项':'一键撤单'})
# print(result)
# result = activeOrderInterface([668802,1,0,1,1,1,800,1,-1],{'测试项':'全仓做空委托'})
# print(result)
#
# # 无委托限价下单：委托流程3
# result = onekeyOrderInterface(668802,0,{'测试项':'一键撤单'})
# print(result)
# result = activeOrderInterface([668802,2,0.4,2,1,1,11500,1,1],{'测试项':'逐仓做多委托'})
# print(result)
#
# # 无委托限价下单：委托流程2
# result = onekeyOrderInterface(668802,0,{'测试项':'一键撤单'})
# print(result)
# result = activeOrderInterface([668802,2,0.4,2,1,1,11900,1,-1],{'测试项':'逐仓做空委托'})
# print(result)
#
# # ~~~~~~~~~~~~~~~~~~~~~~
# result = onekeyOrderInterface(668802,0,{'测试项':'一键撤单'})
# print(result)
# # ~~~~~~~~~~~~~~~~~~~~~~
#
# # 单笔撤单流程
# result = activeOrderInterface([668802,1,0,1,1,1,200,1,1],{'测试项':'全仓做多委托'})
# print(result)
# print(result[1]["uuid"])
# result = cancelOrderInterface([668802,1,result[1]["uuid"]],{'测试项':'单笔撤单-全仓做多'})
# print(result)
#
# result = activeOrderInterface([668802,2,0.4,2,1,1,11900,1,-1],{'测试项':'逐仓做空委托'})
# print(result)
# print(result[1]["uuid"])
# result = cancelOrderInterface([668802,1,result[1]["uuid"]],{'测试项':'单笔撤单-逐仓做空'})
# print(result)
#
# # 一键撤单流程
# result = activeOrderInterface([668803,1,0,1,1,1,100,1000,1],{'测试项':'全仓做多委托1'})
# print(result)




#result = activeOrderInterface([668803,2,0,1,1,1,11500,10,1],{'测试项':'全仓做多委托2'})
# print(result)
# result = activeOrderInterface([668802,1,0,1,1,1,800,1,-1],{'测试项':'全仓做空委托'})
# print(result)
# result = activeOrderInterface([668802,2,0.4,2,1,1,11600,1,1],{'测试项':'逐仓做多委托'})
# print(result)
# result = activeOrderInterface([668802,2,0.4,2,1,1,11900,1,-1],{'测试项':'逐仓做空委托'})
# print(result)
# result = onekeyOrderInterface(668802,0,{'测试项':'一键撤单'})
# print(result)
#
# # 无委托持仓：全仓单笔成交
# result = matchInterface([[668802,1,0,1,1,1,400,1,1],[668803,1,0,1,1,1,400,4,-1]],-1,{'测试项':'全仓持仓成交'})
# print(result)
#
# # 无委托持仓：全仓多笔成交
# result = matchInterface([[668802,1,0,1,1,1,400,1,1],[668803,1,0,1,1,1,400,1,-1]],-1,{'测试项':'全仓持仓成交1'})
# print(result)
# result = matchInterface([[668802,1,0,1,1,1,401,2,-1],[668803,1,0,1,1,1,401,2,1]],1,{'测试项':'全仓持仓成交2'})
# print(result)
#
# # 无委托持仓：逐仓单笔成交
# result = matchInterface([[668802,1,0.1,2,1,1,400,1,1],[668803,1,0.1,2,1,1,400,1,-1]],-1,{'测试项':'逐仓持仓成交'})
# print(result)
#
# # 无委托持仓：逐仓多笔成交
# result = matchInterface([[668802,2,0.4,2,1,1,11600,1,1],[668803,2,0.4,2,1,1,11600,1,-1]],-1,{'测试项':'逐仓持仓成交1'})
# print(result)
# result = matchInterface([[668802,2,0.4,2,1,1,11601,12,-1],[668803,2,0.4,2,1,1,11601,12,1]],1,{'测试项':'逐仓持仓成交2'})
# print(result)
#
# # 无委托持仓：全仓逐仓混合成交
# result = matchInterface([[668802,1,0,1,1,1,400,1,1],[668803,1,0,1,1,1,400,1,-1]],-1,{'测试项':'全仓持仓成交'})
# print(result)
# result = matchInterface([[668802,2,0.4,2,1,1,11600,1,1],[668803,2,0.4,2,1,1,11600,1,-1]],-1,{'测试项':'逐仓持仓成交'})
# print(result)
#
# # 逐仓调整保证金
# result = matchInterface([[668802,2,0.4,2,1,1,11600,1,1],[668803,2,0.4,2,1,1,11600,1,-1]],-1,{'测试项':'逐仓持仓成交'})
# print(result)
# # 增加逐仓保证金  [668802,1,30]
# result = adjustMarginInterface([668802,2,30],{'测试项':'增加逐仓保证金'})
# print(result)
# # 减少逐仓保证金  [668802,1,-10]
# result = adjustMarginInterface([668802,2,-20],{'测试项':'减少逐仓保证金'})
# print(result)
#
# # 调整保证金率：流程1  全仓切换至10倍逐仓
# result = matchInterface([[668802,2,0.4,2,1,1,11600,1,1],[668803,2,0.4,2,1,1,11600,1,-1]],-1,{'测试项':'逐仓持仓成交'})
# print(result)
# # 全仓切换至10倍逐仓  [668802,2,0.1,2]
# result = adjustMarginRateInterface([668802,2,0.1,2],{'测试项':'全仓切换至10倍逐仓'})
# print(result)
# # 持仓数据获取
# result = getPosiInterface(668802,2)
# print(result)
#
# # 调整保证金率：流程2  逐仓切换至全仓
# result = matchInterface([[668802,2,0.4,2,1,1,11600,1,1],[668803,2,0.4,2,1,1,11600,1,-1]],-1,{'测试项':'逐仓持仓成交'})
# print(result)
# # 逐仓切换至全仓  [668802,1,0,1]
# result = adjustMarginRateInterface([668802,1,0,1],{'测试项':'逐仓切换至全仓'})
# print(result)
# # 持仓数据获取
# result = getPosiInterface(668802,2)
# print(result)
#
# # 调整保证金率：流程3  逐仓10倍切换至逐仓20倍
# result = matchInterface([[668802,2,0.1,2,1,1,11600,1,1],[668803,2,0.1,2,1,1,11600,1,-1]],-1,{'测试项':'逐仓持仓成交'})
# print(result)
# # 逐仓10倍切换至逐仓20倍  [668802,2,0.05,2]
# result = adjustMarginRateInterface([668802,2,0.05,2],{'测试项':'逐仓10倍切换至逐仓20倍'})
# print(result)
# # 持仓数据获取
# result = getPosiInterface(668802,2)
# print(result)
#
# # 平仓委托流程1：全仓限价做多平仓委托
# result = cancelAllOrderInterface(1,{'测试项':'整个合约撤单'})
# print(result)
# result = matchInterface([[668802,1,0,1,1,1,400,1,1],[668803,1,0,1,1,1,400,1,-1]],-1,{'测试项':'全仓持仓成交'})
# print(result)
# result = activeOrderInterface([668802,1,0,1,1,2,405,1,-1],{'测试项':'A限价做多平仓委托'})
# print(result)
#
# # 平仓委托流程2：全仓限价做空平仓委托
# result = cancelAllOrderInterface(1,{'测试项':'整个合约撤单'})
# print(result)
# result = matchInterface([[668802,1,0,1,1,1,400,1,1],[668803,1,0,1,1,1,400,1,-1]],-1,{'测试项':'全仓持仓成交'})
# print(result)
# result = activeOrderInterface([668803,1,0,1,1,2,200,1,1],{'测试项':'B限价做空平仓委托'})
# print(result)
#
# # 平仓委托流程3：逐仓限价做多平仓委托
# result = cancelAllOrderInterface(1,{'测试项':'整个合约撤单'})
# print(result)
# result = matchInterface([[668802,2,0.1,2,1,1,11600,1,1],[668803,2,0.1,2,1,1,11600,1,-1]],-1,{'测试项':'逐仓持仓成交'})
# print(result)
# result = activeOrderInterface([668802,2,0.1,2,1,2,11605,1,-1],{'测试项':'A限价做多平仓委托'})
# print(result)
#
# # 平仓委托流程4：逐仓限价做空平仓委托
# result = cancelAllOrderInterface(1,{'测试项':'整个合约撤单'})
# print(result)
# result = matchInterface([[668802,2,0.1,2,1,1,11600,1,1],[668803,2,0.1,2,1,1,11600,1,-1]],-1,{'测试项':'逐仓持仓成交'})
# print(result)
# result = activeOrderInterface([668803,2,0.1,2,1,2,11605,1,1],{'测试项':'B限价做空平仓委托'})
# print(result)
#
# # 平仓成交流程1：全仓限价平仓
# result = cancelAllOrderInterface(1,{'测试项':'整个合约撤单'})
# print(result)
# result = matchInterface([[668802,1,0,1,1,1,400,1,1],[668803,1,0,1,1,1,400,1,-1]],-1,{'测试项':'全仓持仓成交'})
# print(result)
# result = matchInterface([[668802,1,0,1,1,2,401,1,-1],[668803,1,0,1,1,2,401,1,1]],1,{'测试项':'全仓限价平仓'})
# print(result)
#
# # 平仓成交流程2：逐仓限价平仓
# result = cancelAllOrderInterface(1,{'测试项':'整个合约撤单'})
# print(result)
# result = matchInterface([[668802,2,0.4,2,1,1,11600,2,1],[668803,2,0.4,2,1,1,11600,2,-1]],-1,{'测试项':'逐仓持仓成交'})
# print(result)
# result = matchInterface([[668802,2,0.4,2,1,1,11601,1,-1],[668803,2,0.4,2,1,1,11601,1,1]],1,{'测试项':'逐仓限价平仓'})
# print(result)
#
# # 平仓成交流程3：全仓市价平仓
# result = cancelAllOrderInterface(1,{'测试项':'整个合约撤单'})
# print(result)
# result = matchInterface([[668802,1,0,1,1,1,400,1,1],[668803,1,0,1,1,1,400,1,-1]],-1,{'测试项':'全仓持仓成交'})
# print(result)
# result = matchInterface([[668802,1,0,1,1,2,401,1,-1],[668803,1,0,1,3,2,401,1,1]],1,{'测试项':'全仓市价平仓'})
# print(result)
#
# # 平仓成交流程3：逐仓市价平仓
# result = cancelAllOrderInterface(1,{'测试项':'整个合约撤单'})
# print(result)
#result = matchInterface([[668802,2,0.4,2,1,1,11600,1,-1],[668803,2,0.4,2,1,1,11600,1,1]],1,{'测试项':'逐仓持仓成交'})
#print(result)
#result = matchInterface([[668802,2,0.4,2,1,2,11601,1,-1],[668803,2,0.4,2,3,2,11601,1,1]],1,{'测试项':'逐仓市价平仓'})
# print(result)
#
# # # ************************************************************************************************
result = forceFlatPriceInterface(668803,{'测试项':'获取用户强平价格'})
print(result)
print(result['flPrices'])

result = foreFlatInterface(668803,result['flPrices'],{'测试项':'强平验证'})
print(result)

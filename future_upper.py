from futures_middle import  *


#做多委托
result = activeOrderInterface([666666,1,0,1,1,1,1,1,1],{'测试项':'做多委托'})
print(result)
#做空委托
result = activeOrderInterface([666666,1,0,1,1,1,500,1,-1],{'测试项':'做空委托'})
print(result)
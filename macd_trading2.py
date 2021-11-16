import time
import datetime
import pandas as pd
from pandas.core.tools.datetimes import to_datetime
import initData
import api
import judgeTrade
import function

binance = api.binance
dfInfo = pd.DataFrame(initData.data)
dfList = []

#dfList에 값 넣기
for i in range(0, 5):    
    dfList.append(api.get_ohlcv(dfInfo.symbol[i], dfInfo.period[i]))
    function.MACD(dfList[i])

#dfInfo 출력
for i in range(len(dfInfo)):
    print(
    "SYMBOL:" + dfInfo.symbol[i], 
    "PERIOD:" + dfInfo.period[i], 
    "TYPE:" + str(dfInfo.loc[i,'type']), 
    "AMOUNT:" + str(dfInfo.amount[i]), 
    "FLAG:" + str(dfInfo.flag[i]))

op_mode = True

#레버리지설정
for i in range(len(dfInfo)):
    binance.set_leverage(leverage = dfInfo.leverage[i], symbol = dfInfo.symbol[i]) 

while True:
    try:
        now = datetime.datetime.now()
        
        for i in range(0, 5):
            dfList[i] = function.MACD_2(dfInfo, dfList[i], i)    
            time.sleep(0.2)
        
        balance = binance.fetch_balance(params = {"type":"future"})
        usdt = balance['total']['USDT'] 
        coin = binance.fetch_ticker(symbol = 'BTC/USDT')
        cur_price = coin['last']

        if op_mode and (dfInfo.soldtime[0] <= 0):
            judgeTrade.judge(dfList[0], 0, usdt, dfInfo)
            time.sleep(0.1)

        if op_mode and (dfInfo.soldtime[4] <= 0):
            judgeTrade.judge(dfList[4], 4, usdt, dfInfo)
            time.sleep(0.1)

        function.printData(dfList, dfInfo, now, cur_price)
                    
        for i in range(len(dfInfo)) :
            if (dfInfo.soldtime[i] > 0):
                dfInfo.loc[i,'soldtime'] -= 1
                if (i == 1) and ((now.hour == 0) or (now.hour == 8) or (now.hour == 16)) and (now.minute == 59):
                    dfInfo.loc[i,'soldtime'] = 0

        time.sleep(2.3)

    except:
        print("except")
        time.sleep(10)
        continue





import math
import ta
import api

#AMOUNT 계산
def cal_amount(usdt_balance, cur_price, portion,leverage):
    usdt_trade = usdt_balance * portion * leverage
    amount = math.floor((usdt_trade *1000) / cur_price )/1000 #  0.001이하 버림 계산 가우스 함수 floor
    return amount

#AMOUNT_2 계산
def cal_amount_2(usdt_balance, cur_price, portion,leverage):
    usdt_trade = usdt_balance * portion * leverage
    amount = math.floor((usdt_trade * 10 ) / cur_price )/10  #1이하 버림 계산 가우스 함수 floor
    return amount

#MACD 계산
def MACD(df):
    df['histo'] = ta.trend.macd_diff(df.close)
    df['histodf'] = df['histo'] - df['histo'].shift(1)
    meanhisto = df['histodf'].std()
    df['histodfr'] = df['histodf'] / meanhisto *10
    df['rsi'] = ta.momentum.rsi(df.close, window=14)
    df['rsidf'] = df['rsi'] - df['rsi'].shift(1)

#MACD2 계산
def MACD_2(dfInfo, df, i):
    limitCount = 1
    dfLimit1 = api.get_ohlcv(dfInfo.symbol[i], dfInfo.period[i], limitCount)

    if df.index[-1] == dfLimit1.index[-1]:
        df.close[-1] = dfLimit1.close[-1]
    elif df.index[-1] != dfLimit1.index[-1]:
        df = df.append(dfLimit1)

    MACD(df)
    return df

#데이터 출력
def printData(dfList, dfInfo, now, cur_price):
    printData = ""
    for i in range(len(dfList)):
        printData +=  "\n" + str(i) + " HISTO_DFR:" + str(round(dfList[i].histodfr[-1], 3))
        printData += " COUNTER:" + str(dfInfo.counter[i])
        printData += " SOLDTIME:" + str(dfInfo.soldtime[i])

    print(now, "CUR_PRICE:" + str(cur_price), printData)
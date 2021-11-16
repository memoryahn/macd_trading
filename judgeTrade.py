import api
import function

binance = api.binance

def judge(df,  i, usdt, dfInfo):
    coin = binance.fetch_ticker(symbol=dfInfo.symbol[i])
    cur_price = coin['last']
  
    if df['histodfr'][-1] > 2 and (dfInfo['type'][i] == 0):
        dfInfo.loc[i,'counter'] += 1

        if dfInfo.loc[i,'counter'] >= dfInfo['maxcount'][i] :

            amount = function.cal_amount(usdt, cur_price, dfInfo.portion[i], dfInfo.leverage[i])
            if dfInfo['symbol'][i] == 'BNB/USDT' :
                amount = function.cal_amount_2(usdt, cur_price, dfInfo.portion[i], dfInfo.leverage[i])

            if dfInfo.loc[i,'flag'] == 0 :
                print("buy_position", dfInfo['symbol'][i], amount, dfInfo)
                #buy_position(binance, dfs['symbol'][i], amount, dfs)
            elif dfInfo.loc[i,'flag'] == -1 :
                print("sell_position", dfInfo['symbol'][i], amount, dfInfo)
                #sell_position(binance, dfs['symbol'][i], amount, dfs)

            dfInfo.loc[i,'counter'] = 0
            dfInfo.loc[i,'type'] = 1
            dfInfo.loc[i,'soldtime'] = dfInfo['maxsoldtime'][i]
            dfInfo.loc[i,'amount'] = amount

            print(dfInfo.symbol[i],dfInfo.period[i],' buy! ' , amount, cur_price)

    elif df['histodfr'][-1] < 2 and (dfInfo['type'][i] == 0):

        if dfInfo.loc[i,'counter'] >0 :
            dfInfo.loc[i,'counter'] -= 1

    elif df['histodfr'][-1] < -2 and (dfInfo['type'][i] == 1):
        dfInfo.loc[i,'counter'] -= 1 
        
        if dfInfo.loc[i,'counter'] <= -(dfInfo['maxcount'][i]) :
            amount = dfInfo.loc[i,'amount']
        
            if dfInfo.loc[i,'amount']==0 :
                amount = function.cal_amount(usdt, cur_price, dfInfo.portion[i], dfInfo.leverage[i])
        
                if dfInfo['symbol'][i] == 'BNB/USDT' :
                    amount = function.cal_amount_2(usdt, cur_price, dfInfo.portion[i], dfInfo.leverage[i])

            if dfInfo.loc[i,'flag'] == 0 :
                print("sell_position", dfInfo['symbol'][i], amount)
                #sell_position(binance, dfs['symbol'][i], amount, dfs)
            elif dfInfo.loc[i,'flag'] == -1 :
                print("buy_position", dfInfo['symbol'][i], amount)
                #buy_position(binance, dfs['symbol'][i], amount, dfs)           

            dfInfo.loc[i,'counter'] = 0
            dfInfo.loc[i,'type'] = 0
            dfInfo.loc[i,'amount'] = 0
            dfInfo.loc[i,'soldtime'] = (dfInfo['maxsoldtime'][i] * 1.5)

            print(
                "SELL SYMBOL:" + dfInfo.symbol[i],
                "PERIOD:" + dfInfo.period[i], 
                "AMOUNT:" + str(amount), 
                "CUR_PRICE:" + str(cur_price))

    elif df['histodfr'][-1] > -2 and (dfInfo['type'][i] == 1):
        if dfInfo.loc[i,'counter'] < 0 :
            dfInfo.loc[i,'counter'] += 1
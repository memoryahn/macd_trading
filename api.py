import ccxt 
import pandas as pd
import os

api_key = os.environ('BINANCE_API_KEY')
secret = os.environ('BINANCE_SECRET')

# binance 객체 생성
binance = ccxt.binance (
    config = 
    {
    'apiKey'            : api_key,
    'secret'            : secret,
    'enableRateLimit'   : True,
    'options'           : {'defaultType': 'future'}   
    }
)

# ohlcv 데이터 받아오기
def get_ohlcv(ticker,timef, limitCount = 1000):

    coin1m = binance.fetch_ohlcv (
        symbol = ticker, 
        timeframe = timef, 
        since = None,         
        limit = limitCount
        )

    df = pd.DataFrame(coin1m, columns = ['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace = True)
    return df

# BUY ORDER
def buy_position(exchange, symbol, amount):
    exchange.create_market_buy_order(symbol= symbol, amount= amount)

# SELL ORDER
def sell_position(exchange, symbol, amount):
    exchange.create_market_sell_order(symbol= symbol, amount= amount)
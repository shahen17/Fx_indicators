#Importing necessary modules-------------
import MetaTrader5 as mt5
import mt5 as mt5
import pandas as pd
import numpy as np
import talib


#IM USING MT5 AS THE DATA SOURCE..
#INITALISING MT5

if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

            #MT5 LOGIN/SERVER/PASSWORD
authorized=mt5.login(login= , server="", password="")

pair = "EURUSD"
time_frame = mt5.TIMEFRAME_H1

#INDICATOR _1
# SMIPLE MOVING AVERAGE


def simple_moving_average(pair, time_frame):
    price = mt5.copy_rates_from(pair, time_frame, 0, 100)
    close_p = [x.close for x in price]
    sma = talib.SMA(close_p, timeperiod=5)
    return sma
#INDICATOR _2
#SIMPLE MOVING AVERAGE CROSSOVER (5 OVER 10)

def simple_moving_average_crossover(pair, time_frame):
    price = mt5.copy_rates_from(pair, time_frame, 0, 100)
    close_p = [x.close for x in price]
    sma_5 = talib.SMA(close_p, timeperiod=5)
    sma_10 = talib.SMA(close_p, timeperiod=10)
    if sma_5[-1] > sma_5[-2] and sma_5[-2] <= sma_10:
        return True
    else:
        return False


#INDICATOR _3
#BOLLINGER BANDS
def bollinger_bands(pair, time_frame):
    periods = 15
    deviation = 2
    data = mt5.copy_rates_from_pos(pair, time_frame, 0, periods)
    df = pd.DataFrame(data)
    df.rename(
        columns={
            "time": "timestamp",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "tick_volume": "Volume",
        },
        inplace=True,
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df.set_index("timestamp", inplace=True)
    rolling_mean = df["Close"].rolling(window=periods).mean()
    rolling_std = df["Close"].rolling(window=periods).std()
    df["upper_band"] = rolling_mean + (rolling_std * deviation)
    df["lower_band"] = rolling_mean - (rolling_std * deviation)
    df["middle_band"] = rolling_mean


    return df["upper_band"].iloc[-1]
    return df["middle_band"].iloc[-1]
    return df["lower_band"].iloc[-1]

#INDICATOR _4
#RELATIVE STRENGTH INDEX
def relative_strength_index(pair, time_frame):
    period = 10
    data = mt5.copy_rates_from_pos(pair, time_frame, 0, 1000)
    close_p = [bar[4] for bar in data]
    rsi = talib.RSI(close_p, timeperiod=period)
    return rsi

#INDICATOR _5
#Money Flow Index
def money_flow_index(pair, time_frame):
    period = 10
    data = mt5.copy_rates_from_pos(pair, time_frame, 0, 200)
    high = [bar[2] for bar in data]
    low = [bar[3] for bar in data]
    close = [bar[4] for bar in data]
    volume = [bar[5] for bar in data]
    mfi = talib.MFI(high, low, close, volume, timeperiod=period)
    return mfi




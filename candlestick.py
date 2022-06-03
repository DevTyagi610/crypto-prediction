#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import numpy as np
from binance import Client, ThreadedWebsocketManager , ThreadedDepthCacheManager
get_ipython().run_line_magic('matplotlib', 'inline')
import mplfinance as mpf
import pandas_ta as ta
from scipy.stats import linregress


# In[13]:


api_key = "grbtS6aVaMLGqlKjNcRSYSCV6uwuyKEn3zynoSHNFjIodJilIyCI7YD0gbIpUtJI"
secret_key = "bBru8FTk2LL8jv3AfvYLQQ4kof0ZzMjZKKu1nsSn98hi0bNDw6TxR0yksWFk0rpP"


# In[14]:


client = Client(api_key , secret_key)


# In[15]:


tickers=client.get_all_tickers()
tickers[0]["price"]


# In[16]:


df = pd.DataFrame(tickers)
df


# In[17]:


historical_data = client.get_historical_klines("MANAUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan 2021")


# In[18]:


history_df = pd.DataFrame(historical_data)
history_df.columns=["Open Time" , "Open" , "High" , "Low" , "Close" , "Volume" , "Close Time" , "Quote Asset Vol" , "No. of Trades" , "TB Base Vol" , "TB Quote Vol" , "Ignore"]
history_df["Open Time"] = pd.to_datetime(history_df["Open Time"]/1000 , unit = "s")
history_df["Close Time"] = pd.to_datetime(history_df["Close Time"]/1000 , unit = "s")
num = ["Open", "High", "Low", "Close","Volume"]
history_df[num] = history_df[num].apply(pd.to_numeric, axis=1)
history_df.head()


# In[23]:


history_df = history_df[["Open Time", "Open", "High", "Low", "Close","Volume"]]
indexZeroes = history_df[history_df["Volume"]==0].index
history_df.drop(indexZeroes , inplace= True)
#history_df = history_df.set_index("Open Time")
#history_df.loc[(history_df["Volume"]==0)]
history_df.head()


# In[31]:


history_df["ATR"] = history_df.ta.atr(length = 20)
history_df["RSI"] = history_df.ta.rsi()
history_df["Average"] = history_df.ta.midprice(length = 1)
history_df['MA40'] = history_df.ta.sma(length=40) #very sensitive to price movements
history_df['MA80'] = history_df.ta.sma(length=80)
history_df['MA160'] = history_df.ta.sma(length=160) # least sensitive 
history_df.tail(5)


# In[34]:


def get_slope(array):
    y = np.array(array)
    x = np.arange(len(y))
    slope, intercept, r_value, p_value, std_err = linregress(x,y)
    return slope

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
backrollingN = 6
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
history_df['slopeMA40'] = history_df['MA40'].rolling(window=backrollingN).apply(get_slope, raw=True)
history_df['slopeMA80'] = history_df['MA80'].rolling(window=backrollingN).apply(get_slope, raw=True)
history_df['slopeMA160'] = history_df['MA160'].rolling(window=backrollingN).apply(get_slope, raw=True)
history_df['AverageSlope'] = history_df['Average'].rolling(window=backrollingN).apply(get_slope, raw=True)
history_df['RSISlope'] = history_df['RSI'].rolling(window=backrollingN).apply(get_slope, raw=True)
history_df.tail(5)


# TARGET CATEGORIES

# In[39]:


pipdiff = 500*1e-5 #for TP
SLTPRatio = 2 #pipdiff/Ratio gives SL

def mytarget(barsupfront, df1):
    length = len(df1)
    high = list(df1['High'])
    low = list(df1['Low'])
    close = list(df1['Close'])
    open = list(df1['Open'])
    trendcat = [None] * length
    
    for line in range (0,length-barsupfront-2):
        valueOpenLow = 0
        valueOpenHigh = 0
        for i in range(1,barsupfront+2):
            value1 = open[line+1]-low[line+i]
            value2 = open[line+1]-high[line+i]
            valueOpenLow = max(value1, valueOpenLow)
            valueOpenHigh = min(value2, valueOpenHigh)

            if ( (valueOpenLow >= pipdiff) and (-valueOpenHigh <= (pipdiff/SLTPRatio)) ):
                trendcat[line] = 1 #-1 downtrend
                break
            elif ( (valueOpenLow <= (pipdiff/SLTPRatio)) and (-valueOpenHigh >= pipdiff) ):
                trendcat[line] = 2 # uptrend
                break
            else:
                trendcat[line] = 0 # no clear trend
            
    return trendcat


# In[42]:


history_df['mytarget'] = mytarget(16, history_df)
history_df


# DOJI PATTERN

# In[1]:


def doji(df) :
    df1 = pd.DataFrame(columns=['Open','Close','High','Low'])
    df1['Open'] = df['Open'].astype(float)
    df1['Close'] = df['Close'].astype(float)
    df1['High'] = df['High'].astype(float)
    df1['Low'] = df['Low'].astype(float)
    if 20 * abs((df1["Open"] - df1["Close"])) <= df1["High"] - df1["Low"] :
        df1["DOJI"] = True
    else :
        df1["DOJI"] = False
    return df1


# In[2]:


doji(history_df)


# In[ ]:


#mpf.plot(history_df.tail(20),type="candle" , mav=(5) , style="yahoo")


# In[ ]:





# In[ ]:





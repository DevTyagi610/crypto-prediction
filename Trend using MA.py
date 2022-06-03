#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from binance import Client, ThreadedWebsocketManager , ThreadedDepthCacheManager
import pandas_ta as ta


# In[2]:


api_key = "grbtS6aVaMLGqlKjNcRSYSCV6uwuyKEn3zynoSHNFjIodJilIyCI7YD0gbIpUtJI"
secret_key = "bBru8FTk2LL8jv3AfvYLQQ4kof0ZzMjZKKu1nsSn98hi0bNDw6TxR0yksWFk0rpP"


# In[3]:


client = Client(api_key , secret_key)


# In[4]:


tickers=client.get_all_tickers()
tickers[0]["price"]
df = pd.DataFrame(tickers)
df


# In[5]:


historical_data = client.get_historical_klines("MANAUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan 2021")


# In[6]:


history_df = pd.DataFrame(historical_data)
history_df.columns=["Open Time" , "Open" , "High" , "Low" , "Close" , "Volume" , "Close Time" , "Quote Asset Vol" , "No. of Trades" , "TB Base Vol" , "TB Quote Vol" , "Ignore"]
history_df["Open Time"] = pd.to_datetime(history_df["Open Time"]/1000 , unit = "s")
history_df["Close Time"] = pd.to_datetime(history_df["Close Time"]/1000 , unit = "s")
num = ["Open", "High", "Low", "Close","Volume"]
history_df[num] = history_df[num].apply(pd.to_numeric, axis=1)
history_df.head()


# In[7]:


history_df = history_df[["Open Time", "Open", "High", "Low", "Close","Volume"]]
indexZeroes = history_df[history_df["Volume"]==0].index
history_df.drop(indexZeroes , inplace= True)
history_df.head()


# In[8]:


import pandas_ta as pa
history_df["MA20"] = pa.ema(history_df.Close, length=20)
history_df["MA30"] = pa.ema(history_df.Close, length=30)
history_df["MA60"] = pa.ema(history_df.Close, length=60)
history_df.tail(10)


# In[9]:


def mysig(x):
    if x.MA20<x.MA30<x.MA60:
        return -1
    elif x.MA20>x.MA30>x.MA60:
        return +1
    else:
        return 0


# In[17]:


history_df["signal"] = history_df.apply(mysig, axis=1)
history_df.tail()


# In[18]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
dfpl = history_df[:518]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close']),
                go.Scatter(x=dfpl.index, y=dfpl.MA20, line=dict(color='orange', width=1), name="MA Fast"),
                go.Scatter(x=dfpl.index, y=dfpl.MA30, line=dict(color='blue', width=1), name="MA Medium"),
                go.Scatter(x=dfpl.index, y=dfpl.MA60, line=dict(color='black', width=1), name="MA Slow")])

fig.show()


# In[12]:


def trend_alert(df): 
    dfstream = pd.DataFrame(columns=['Open','Close','High','Low'])
    dfstream['Open'] = df['Open'].astype(float)
    dfstream['Close'] = df['Close'].astype(float)
    dfstream['High'] = df['High'].astype(float)
    dfstream['Low'] = df['Low'].astype(float)

    dfstream['MA20'] = dfstream['Open'].rolling(window=20).mean()
    dfstream['MA30'] = dfstream['Open'].rolling(window=30).mean()
    dfstream['MA60'] = dfstream['Open'].rolling(window=60).mean()

    dfstream["signal"] = dfstream.apply(mysig, axis=1)
    dfstream_last_60_vals = dfstream.tail(60) 

    if dfstream_last_60_vals.iloc[59]['signal']==1 and dfstream_last_60_vals.iloc[58]['signal']!=1:
        msg = str("the signal is buying, the Trend is Uptrend")
    elif dfstream_last_60_vals.iloc[59]['signal']==1 and dfstream_last_60_vals.iloc[58]['signal']==1:
        msg = str("the signal is buying, the Trend is Uptrend")    
    elif dfstream_last_60_vals.iloc[59]['signal']==-1 and dfstream_last_60_vals.iloc[58]['signal']==1:
        msg = str("The Trend is changing from Uptrend to Downtrend")     
    elif dfstream_last_60_vals.iloc[59]['signal']==1 and dfstream_last_60_vals.iloc[58]['signal']==-1:
        msg = str("The Trend is changing from Downtrend to Uptrend")
    elif dfstream_last_60_vals.iloc[59]['signal']==-1 and dfstream_last_60_vals.iloc[58]['signal']==-1:
        msg = str("the signal is selling, the Trend is Downtrend")   
    elif dfstream_last_60_vals.iloc[59]['signal']==-1 and dfstream_last_60_vals.iloc[58]['signal']==-1:
        msg = str("the signal is selling, the Trend is Downtrend")   
    else :
        msg = str("No significant trend")
    return msg


# In[21]:


trend_alert(history_df[:518])


# In[14]:


def doji(df) :
    df1 = pd.DataFrame(columns=['Open','Close','High','Low'])
    df1['Open'] = df['Open']
    df1['Close'] = df['Close']
    df1['High'] = df['High']
    df1['Low'] = df['Low']
    df1["DOJI"] = 20 * abs((df1["Open"] - df1["Close"])) <= df1["High"] - df1["Low"]
    return df1


# In[15]:


newdf = doji(history_df)
newdf.loc[newdf["DOJI"] == True]


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[2]:


import talib


# In[3]:


import pandas as pd
from binance import Client, ThreadedWebsocketManager , ThreadedDepthCacheManager
import pandas_ta as ta


# In[4]:


api_key = "grbtS6aVaMLGqlKjNcRSYSCV6uwuyKEn3zynoSHNFjIodJilIyCI7YD0gbIpUtJI"
secret_key = "bBru8FTk2LL8jv3AfvYLQQ4kof0ZzMjZKKu1nsSn98hi0bNDw6TxR0yksWFk0rpP"


# In[5]:


client = Client(api_key , secret_key)


# In[6]:


tickers=client.get_all_tickers()
tickers[0]["price"]
df = pd.DataFrame(tickers)
df


# In[7]:


historical_data = client.get_historical_klines("MANAUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan 2021")


# In[8]:


history_df = pd.DataFrame(historical_data)
history_df.columns=["Open Time" , "Open" , "High" , "Low" , "Close" , "Volume" , "Close Time" , "Quote Asset Vol" , "No. of Trades" , "TB Base Vol" , "TB Quote Vol" , "Ignore"]
history_df["Open Time"] = pd.to_datetime(history_df["Open Time"]/1000 , unit = "s")
history_df["Close Time"] = pd.to_datetime(history_df["Close Time"]/1000 , unit = "s")
num = ["Open", "High", "Low", "Close","Volume"]
history_df[num] = history_df[num].apply(pd.to_numeric, axis=1)
history_df.head()


# In[9]:


history_df = history_df[["Open Time", "Open", "High", "Low", "Close","Volume"]]
indexZeroes = history_df[history_df["Volume"]==0].index
history_df.drop(indexZeroes , inplace= True)
history_df.head()


# In[14]:


morning_star = talib.CDLMORNINGSTAR(history_df['Open'], history_df['High'], history_df['Low'], history_df['Close'])
engulfing = talib.CDLENGULFING(history_df['Open'], history_df['High'], history_df['Low'], history_df['Close'])
doji = talib.CDLDOJI(history_df['Open'], history_df['High'], history_df['Low'], history_df['Close'])

history_df['Morning Star'] = morning_star
history_df['Engulfing'] = engulfing
history_df["doji"] = doji

doji_days = history_df[history_df['doji'] != 0]

print(doji_days)


# In[17]:


import streamlit as st


# In[ ]:





# In[ ]:





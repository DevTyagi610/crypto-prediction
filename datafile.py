#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from binance import Client, ThreadedWebsocketManager , ThreadedDepthCacheManager
import pandas_ta as ta
import streamlit as st


# In[11]:


import pickle


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


# In[13]:


file="data.pkl"
fileobj = open(file, "wb")
pickle.dump(history_df , fileobj)
fileobj.close()


# In[14]:


file = "data.pkl"
fileobj = open(file, "rb")
df = pickle.load(fileobj)
print(df)


# In[ ]:





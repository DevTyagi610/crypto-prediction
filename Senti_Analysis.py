#!/usr/bin/env python
# coding: utf-8

# GENERAL LIBS USED FOR DATA

# In[1]:


import pandas as pd
import numpy as np
import re
import csv
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
from datetime import datetime
from datetime import date
from datetime import timedelta


# TWITTER API IMPORTS

# In[2]:


import tweepy
from tweepy import Stream
from tweepy import OAuthHandler


# LIBS FOR SENTIMENT ANALYSIS

# In[3]:


import flair
from flair.models import TextClassifier
from flair.data import Sentence


# TWITTER API KEYS

# In[4]:


api_key = 'fafQEqJniUV4AfBk6OR9PQAXN'   #api key
api_secret = 'lKGGsowdIpvgMFR4GkyO6rE3DbecdWCeOmAwy9COyaNRlcEElo'  #api key secret 
access_token = '1501429494527463427-afHCQnbeUiVndYs0WwtlSVwANaMRA8'    #access token
access_secret = 'oHgBxvJnHMjQJBsDrkHQmOXDedHyP7dOTG3EZrIbmlhqH'  #access secret


# In[5]:


auth = tweepy.OAuthHandler(api_key , api_secret)
auth.set_access_token(access_token , access_secret)
api = tweepy.API(auth , wait_on_rate_limit = True)
day = date.today() - timedelta(hours = 12)
print(day)
tweets = tweepy.Cursor(api.search_tweets, q = "#bitcoin -filter:retweets" , lang="en", tweet_mode="extended").items(1000)
all_tweets = [tweet.full_text for tweet in tweets]
all_tweets


# DATAFRAME TO STORE TWEETS

# In[6]:


df = pd.DataFrame(all_tweets , columns=["tweets"])
df.drop_duplicates(keep=False, inplace=True)
print(df.shape[0])
df.head()


# CLEANING TWEEETS WITH REGEX

# In[7]:


def CleanTweets(txt) :
    txt = re.sub("#bitcoin" , "bitcoin" , txt)
    txt = re.sub("#Bitcoin" , "bitcoin" , txt)
    txt = re.sub("#BTC" , "bitcoin" , txt)
    txt = re.sub("\\n" , "" , txt)
    txt = re.sub("#[A-Za-z0-9]+" , "" , txt)
    txt = re.sub("@[A-Za-z0-9]+" , "" , txt) 
    txt = re.sub("https?:\/\/S+" , "" , txt)
    return txt


# In[8]:


df["cleaned_tweets"] = df["tweets"].apply(CleanTweets)
df


# SAVING DF IN CSV

# In[9]:


df.to_csv("twitterDB.csv")
df1 = pd.read_csv("twitterDB.csv")
df1.head()


# In[10]:


sia = TextClassifier.load('en-sentiment')

def Sentiment_Flair(txt) :
    sentence = Sentence(txt)
    sia.predict(sentence)
    score = sentence.labels[0]
    if "POSITIVE" in str(score) :
        return "positive"
    elif "NEGATIVE" in str(score) :
        return "negative"
    else :
        return "neutral"

df1["sentiments"] = df1["cleaned_tweets"].apply(lambda x : Sentiment_Flair(x))
df1.head()


# In[11]:


df1["sentiments"].value_counts().plot(kind="bar")
plt.title("Sentiment Analysis Bar Graph")
plt.xlabel("Sentiment")
plt.ylabel("No. of Tweets")
plt.show()


# In[ ]:





# In[ ]:





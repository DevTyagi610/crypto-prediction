#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pickle
import numpy as np


# In[2]:


def load_data() :
    with open("data.pkl" , "rb") as file :
        data = pickle.load(file)
    return data


# In[3]:


df = load_data()
print(df)


# In[4]:


def show_data():
    st.title("Hello, this is DataFrame1")


# In[ ]:





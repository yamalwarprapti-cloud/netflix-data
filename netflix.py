#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import streamlit

# In[3]:


sales=pd.DataFrame({"quantity":[1,2,3,4,5,6],"price":[100,200,300,400,500,600]})#to create a tabuler structure in python


# In[4]:


sales


# In[5]:


netflix=pd.read_csv("netflix.csv")


# In[6]:


netflix


# In[7]:


netflix.shape


# In[8]:


netflix.info()


# In[9]:


netflix.isnull().sum()


# In[10]:


netflix.describe()


# In[11]:


netflix.duplicated().sum()


# In[12]:


netflix.drop_duplicates(inplace=True)


# In[13]:


netflix


# In[14]:


netflix["Watch_Date"]=pd.to_datetime(netflix["Watch_Date"])


# In[15]:


netflix.info()


# In[16]:


netflix["month"]=netflix["Watch_Date"].dt.month_name()


# In[17]:


netflix


# In[25]:


netflix.groupby("month")["Monthly_Revenue"].sum().plot(kind="bar",ylabel="Monthly_Revenue",xlabel="month",title="month wise revenue")


# In[33]:


netflix.groupby("Region")["Rating"].sum().plot(kind="pie",ylabel="rating",xlabel="Region",title="Region Wise Rating",autopct='%1.1f%%')


# In[26]:


netflix.groupby("Device")["Monthly_Revenue"].sum().plot(kind="line",ylabel="Monthly_Revenue",xlabel="Device",title="Device wise revenue")


# In[37]:


netflix["Rating"].value_counts().plot(kind="bar",title="Total Rating")


# In[29]:


netflix.groupby("Region")["Monthly_Revenue"].sum().plot(kind="bar",ylabel="Monthly_Revenue",xlabel="Region",title="Region wise Revenue")


# In[35]:


netflix.groupby("Subscription_Plan")["Watch_Count"].sum().plot(kind="pie",title="subscription plan wise watch count",autopct='%1.1f%%')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





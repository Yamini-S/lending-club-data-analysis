
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
#pip install seaborn 
import seaborn as sns
get_ipython().magic('matplotlib inline')
import math

from datetime import datetime


# In[2]:

print("Start downloading data")

df = pd.read_csv("Data/RejectStatsA.csv",skiprows=1, encoding='utf-8')
#df = pd.read_csv("Data/CombinedCSV_just_plain_combined.csv",skiprows=1)

#if more than 50% values in an observation is NAN drop that observation
half_count = len(df.columns) / 2
df=df.dropna(axis='columns', how='all')
df = df.dropna(thresh=half_count)

print(df.shape)


# In[3]:

print("Clean and Analyse the data by slicing")
print("Cleaning and missing value handling started")
df.ix[:3,:9]


# In[4]:

df["Amount Requested"]=df["Amount Requested"].dropna().astype(int)
df["Application Date"]=df["Application Date"].fillna(method='ffill')
df["Loan Title"]=df["Loan Title"].fillna("Not available")

df=df[pd.notnull(df['Risk_Score'])]

ceil_function= lambda x: math.ceil(x)

df['Risk_Score']=df['Risk_Score'].apply(ceil_function)

df=df[pd.notnull(df['Debt-To-Income Ratio'])]
#Debt-To-Income Ratio was loaded as an object data type instead of float due to the '%' character. Let's strip that out and convert the column type.
df["Debt-To-Income Ratio"] = pd.Series(df["Debt-To-Income Ratio"]).str.replace('%', '').astype(float)

df.ix[:3,:5]


# In[5]:

df=df[pd.notnull(df['Zip Code'])]
df["Zip Code"]=df["Zip Code"].astype(str)

#stripping the last two characters and fetching the first three digits of the zipcode
df["Zip Code"]=df["Zip Code"].map(lambda x: x[:3]).astype(int)

df.ix[:3,5:]


# In[6]:

#replace missing values for addr_state with XX (random characters)
df["State"]=df["State"].fillna("XX")

#replacing missing values with 0
df["Employment Length"].replace('n/a', np.nan,inplace=True)
df["Employment Length"].fillna(value=0,inplace=True)

#convert categorical value into numerical value
df['Employment Length'].replace(to_replace='[^0-9]+', value='', inplace=True, regex=True)
df['Employment Length'] = df['Employment Length'].astype(int)

df["Policy Codee"]=df["Policy Code"].fillna((df['Policy Code'].value_counts().idxmax())).astype(int)

df.ix[:3,5:9]


# In[7]:

print("Cleaning and missing value handling completed")
df.ix[:3,:9]


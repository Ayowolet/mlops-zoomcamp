#!/usr/bin/env python
# coding: utf-8

# In[1]:


#get_ipython().system('pip freeze | grep scikit-learn')


# In[2]:


#get_ipython().system('python -V')


# In[3]:


import pickle
import pandas as pd
import os
import sys


# In[14]:


year = int(sys.argv[1]) # 2023
month = int(sys.argv[2]) # 4

input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'


# In[8]:

MODEL_FILE = os.getenv('MODEL_FILE', 'model.bin')

with open(MODEL_FILE, 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[5]:


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[6]:


df = read_data(input_file)


# In[9]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


# In[12]:


y_pred.std()
print('predicted mean duration:', y_pred.mean())

# In[15]:


df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


# In[18]:


df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['predicted_duration'] = y_pred


# In[20]:
os.makedirs('output', exist_ok=True)

df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)


# In[ ]:





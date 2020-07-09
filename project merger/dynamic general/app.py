#!/usr/bin/env python
# coding: utf-8

# In[71]:


import json
#import random, string
import pandas as pd
#import numpy as np
from collections import defaultdict
#import requests
from functions import *

# Open base
with open('export.json') as json_file:
    data = json.load(json_file)

# Work with XSLX and define variables
xls = pd.ExcelFile('FAQ.xlsx')
df1 = pd.read_excel(xls, "FAQ's")
df = pd.DataFrame()
df['Questions']=list(df1['Question'])
df['Answers']=list(df1['Answer'])
df['Topic']=list(df1['Topic'])
n_items = max(df.count())
qa = df[:n_items]
# get Organization Info
df2 = pd.read_excel(xls, "Introduction")
df2.columns = ['row', 'faq2bot instruction', 'none', 'label', 'value']
orgdict = df2.set_index('label')['value'].to_dict()
questions = list(qa['Questions'])
answers = list(qa['Answers'])

#create from excel
data = create_flows_intents_actions (data, questions, answers)

tg = add_textgen (data)
with open('general nl1.json') as json_file:
    a = json.load(json_file)
b = tg

new = merge_flows (a,b)
new = merge_intents (new,b)
merged = merge_actions (new,b)

merged = create_opening (merged, orgdict['Organization'], orgdict['Chatbot Name'])
unique_topics = sorted(df.Topic.unique())
merged = create_carousel (df, merged, unique_topics)
merged = replace_handoff_email (merged, orgdict['Support Email'])


# In[93]:


with open('merged_projects.json', 'w') as f:
    json.dump(merged, f)

print("conversion done")
#!/usr/bin/env python
# coding: utf-8

# In[94]:


import pandas as pd
import json
from flask import jsonify

print("Preparing Data")
# Work with XSLX and define variables

xls = pd.ExcelFile("FAQ.xlsx")
df1 = pd.read_excel(xls, "FAQ's")
df = pd.DataFrame()
df['Questions']=list(df1['Question'][:10])
df['Answers']=list(df1['Answer'][:10])
df['Topic']=list(df1['Topic'][:10])
n_items = max(df.count())
qa = df[:n_items]

# get Organization Info
df2 = pd.read_excel(xls, "Introduction")
df2.columns = ['row', 'faq2bot instruction', 'none', 'label', 'value']
orgdict = df2.set_index('label')['value'].to_dict()
questions = list(qa['Questions'])
answers = list(qa['Answers'])
topics = list(qa['Topic'])


# In[95]:


for key in orgdict:
    print('orgdict["{}"]'.format(key))

print("Data Prepared")
print("Starting Request")


# In[105]:


print(questions)


# In[ ]:


import requests

url = "https://botcreator.ew.r.appspot.com/"

payload = json.dumps({
    "textgen": "false",
    "language": orgdict["Language"],
    "questions": questions,
    "answers": answers,
    "topics": topics,
    "chatbotName": orgdict["Chatbot Name"],
    "organizationName": orgdict["Organization"],
    "supportEmail": orgdict["Support Email"],
    "handoffType": "ticket"
})


headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

#print(response.text.encode('utf8'))
print("Response received")


# In[108]:


with open("upload_"+str(orgdict["Organization"])+",json", mode='wb') as localfile:     
    localfile.write(response.content)

print("Saved to file")


# In[ ]:





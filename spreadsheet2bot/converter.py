#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import random, string
import pandas as pd
import numpy as np
from collections import defaultdict
import requests


# # Loading data

# In[2]:


with open('export.json') as json_file:
    data = json.load(json_file)


# # Functions

# ## Create Flow Steps

# In[3]:


def createflowsteps (title, actionId, intentId, stepId):#
    return [{'meta': {'audioHashes': []},
   'type': 'INTENT',
   'title': title,
   'contexts': [],
   'actions': [{'actionId': actionId}],
   'children': [],
   'stepId': stepId,
   'intent': {'intentId': intentId}}]
# createflowsteps ('Intent 1','a','i','s') 


# ## Create Flows

# In[4]:


def createflow (title, actionId, flowId, intentId, stepId):
    return {
        'flowId': '4cc34237-cbd9-4e08-8a4e-d1104c34ea5b',
        'disabled': False,
        'group': 'FAQ',
        'metadata': [],
        'steps': createflowsteps (title, actionId, intentId, stepId),
        'title': title}
# createflow ('title', "actionId", "flowId", "intentId", "stepId")


# ## Create Intents

# In[5]:


def createintent (title, brainId, intentId):
    return {
        'brainId': brainId,
        'intentId': intentId,
        'accuracy': 15.38,
        'disableTraining': False,
        'examples': [
            {'entities': [], 'query': title},
            ],
         'title': title}
# createintent ('title', "brains", "intents")


# ## Create Actions

# In[6]:


def createaction (actionId, brainId, answer):
    return {
        'actionId': actionId,
        'brainId': brainId,
        'payload': {'texts': [answer], 'quickReplies': [], 'tags': []},
        'type': 'TEXT'}
# createintent ('title', "brains", "intents")


# ## Text Generation Service

# In[7]:


# TextGen API
def textgen(sentence, lang):
    
    url = "https://textgenapp-259408.appspot.com/textgen"

    payload = {
        'input sentences': [sentence],
        'lang': lang
    }
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.19.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "e6565f73-3b8d-4dff-82c6-8b5ef3c969ec,6118f8fa-8824-419b-8558-5e84893cc8c9",
        'Host': "textgenapp-259408.appspot.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "89",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }
    
    example = str(json.dumps(payload))
    # print(example)
    response = requests.request("POST", url, data=example, headers=headers)
    return(response)
    


# In[8]:


# Get Trainings Data from API in list
def get_td (sentence, lang):
    response = textgen(sentence,lang)
    json_data = json.loads(response.text)
    td = [item[0] for item in json_data]
    return td


# In[9]:


# create training examples
def create_td (list_sentences):
    td = []
    for example in list_sentences:  
         td.append({'entities': [], 'query': example})
    return td


# ## Key Generator

# In[10]:


def keygen():
    k = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    return k


# # Get FAQ's from Spreadsheet
# 

# In[11]:


xls = pd.ExcelFile('FAQ.xlsx')
df1 = pd.read_excel(xls, "FAQ's")
df = pd.DataFrame()
df['Questions']=list(df1['Question'])
df['Answers']=list(df1['Answer'])
n_items = max(df.count())
qa = df[:n_items]


# In[12]:


questions = list(qa['Questions'])
answers = list(qa['Answers'])


# In[13]:


# Optional: Check of answers matches question
#for i in range(len(questions)):
#    print(questions[i])
#    print(answers[i])
#    print()


# In[14]:


keys = ["actionId","intentId", "flowId", "stepId"]
brainId = keygen()

flows = []
intents = []
actions = []
for i in range(len(questions)):
    title = questions[i]
    answer = answers[i]
    dkeys = {}
    for key in keys:
        dkeys[key]=keygen()
    #print(dkeys)
    flows.append (createflow (title, dkeys["actionId"] ,dkeys["flowId"], dkeys["intentId"], dkeys["stepId"]))
    intents.append (createintent (title, brainId, dkeys["intentId"]))
    actions.append (createaction (dkeys["actionId"], brainId, answer) )
    #print()


# In[15]:


data['brains'][0]['flows'] = flows
data['brains'][0]['intents'] = intents
data['brains'][0]['actions'] = actions


# In[16]:



with open('uploadthisfiletoflow.json', 'w') as f:
    json.dump(data, f)


# # Add training examples from TextGen
# 

# In[17]:


with open('uploadthisfiletoflow.json') as json_file:
    tg = json.load(json_file)


# In[18]:


intents = tg['brains'][0]['intents']


# In[19]:


for i in range(len(intents)):
    examples = intents[i]['examples']
    in_tg = examples[0]['query']
    listtd = get_td (in_tg, "nl")
    listtd.append(in_tg)
    examples = create_td (listtd)
    tg['brains'][0]['intents'][i]['examples']=examples

  #  print()
intents = tg['brains'][0]['intents']


# In[20]:


with open('uploadwithexamples.json', 'w') as f:
    json.dump(tg, f)

print("Completed")
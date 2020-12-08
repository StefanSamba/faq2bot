#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import random, string
import pandas as pd
import numpy as np
from collections import defaultdict


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


# ## Key Generator

# In[7]:


def keygen():
    k = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    return k


# # Fill with FAQ
# 

# In[16]:


qa = pd.read_csv('scrapedwebsite.csv', encoding = "utf-8")


# In[19]:


questions = list(qa['Questions'])
answers = list(qa['Answers'])


# In[21]:


# Optional: Check of answers matches question
#for i in range(len(questions)):
#    print(questions[i])
#    print(answers[i])
#    print()


# In[22]:


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


# In[23]:


data['brains'][0]['flows'] = flows
data['brains'][0]['intents'] = intents
data['brains'][0]['actions'] = actions


# In[24]:



with open('uploadthisfiletoflow.json', 'w') as f:
    json.dump(data, f)


# In[ ]:





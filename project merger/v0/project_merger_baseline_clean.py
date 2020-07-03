#!/usr/bin/env python
# coding: utf-8

# In[69]:


import json
with open('projecta.json') as json_file:
    a = json.load(json_file)
with open('projectb.json') as json_file:
    b = json.load(json_file)


# In[71]:


def merge_flows (prjct_base,prjct_head):
    for flow in prjct_head['brains'][0]['flows']:
        prjct_base['brains'][0]['flows'].append(flow)
    return prjct_base


# In[72]:


def merge_intents (prjct_base,prjct_head):
    brainId = prjct_base['brains'][0]['brain']['brainId']
    for intent in prjct_head['brains'][0]['intents']:
        prjct_base['brains'][0]['intents'].append(intent)
    return prjct_base


# In[73]:


def merge_actions (prjct_base,prjct_head):
    brainId = prjct_base['brains'][0]['brain']['brainId']
    for action in prjct_head['brains'][0]['actions']:
        prjct_base['brains'][0]['actions'].append(action)
    return prjct_base


# In[74]:


new = merge_flows (a,b)
new = merge_intents (new,b)
new = merge_actions (new,b)


# In[82]:


with open('merged_projects.json', 'w') as f:
    json.dump(new, f)


# In[ ]:





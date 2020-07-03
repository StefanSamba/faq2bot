from functions import *
import json
import random, string
import pandas as pd
import numpy as np
from collections import defaultdict
import requests

# get FAQs
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
if n_items > 10:
    print("Whoops, more then 10 items, maximum of 10 allowed")
qa = df[:n_items]
# get Organization Info
df2 = pd.read_excel(xls, "Introduction")
df2.columns = ['row', 'faq2bot instruction', 'none', 'label', 'value']
orgdict = df2.set_index('label')['value'].to_dict()
questions = list(qa['Questions'])
answers = list(qa['Answers'])

#create from excel
data = create_flows_intents_actions (data, questions, answers)


with open('general nl.json') as json_file:
    a = json.load(json_file)


print("let's add training examples")
tg = add_textgen (data)# disable without textgen

b = tg# #change to tg / data

merged = merge_flows (a,b)
merged = merge_intents (merged,b)
merged = merge_actions (merged,b)
merged = create_opening (merged, orgdict['Organization'], orgdict['Chatbot Name'])
merged = replace_text_in_reply (merged, '43f36c26-3e9d-412d-8eca-1eb8507a85d0', "Chatbot Name", orgdict['Chatbot Name'])
unique_topics = sorted(df.Topic.unique())
merged = create_carousel (df, merged, unique_topics)
merged = replace_handoff_email (merged, orgdict['Support Email'])

with open('merged_projects.json', 'w') as f:
    json.dump(merged, f)
    print("conversion completed")
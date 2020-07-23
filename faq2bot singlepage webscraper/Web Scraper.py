#!/usr/bin/env python
# coding: utf-8

# In[31]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# insert page to scrape
html = urlopen('https://www.ltp.nl/kandidaten/veelgestelde-vragen/')
bs = BeautifulSoup(html, "html.parser")


# In[26]:


# Create list of answers
listanswers = []
for i in range(len(bs.findAll("div", {"class": "toggle-content"}))):
    listanswers.append(bs.findAll("div", {"class": "toggle-content"})[i].find('p').text)


# In[34]:


# Create list of questions
listquestions = []
for i in range (4,len(bs.findAll("label"))-4):
    listquestions.append(bs.findAll("label")[i].text)


# In[39]:


df = pd.DataFrame()


# In[41]:


df['Questions']=listquestions
df['Answers']=listanswers


# In[43]:


df.to_csv('scrapedwebsite.csv', index=False, encoding='utf-8')


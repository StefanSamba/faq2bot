
import json
import random, string
import pandas as pd
import numpy as np
from collections import defaultdict
import requests


def createflowsteps (title, actionId, intentId, stepId):#
    return [{'meta': {'audioHashes': []},
   'type': 'INTENT',
   'title': title,
   'contexts': [],
   'actions': [{'actionId': actionId}],
   'children': [],
   'stepId': stepId,
   'intent': {'intentId': intentId}}]


def createflow (title, actionId, flowId, intentId, stepId):
    return {
        'flowId': '4cc34237-cbd9-4e08-8a4e-d1104c34ea5b',
        'disabled': False,
        'group': 'FAQ',
        'metadata': [],
        'steps': createflowsteps (title, actionId, intentId, stepId),
        'title': title}


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



def createaction (actionId, brainId, answer):
    return {
        'actionId': actionId,
        'brainId': brainId,
        'payload': {'texts': [answer], 'quickReplies': [], 'tags': []},
        'type': 'TEXT'}


# TextGen API
def textgen(sentence, lang):
    
    url = "https://data-augment.ew.r.appspot.com/augment"
    data={"sequences" :[sentence]}
    headers = {
    'Content-Type': 'application/json',
    'Postman-Token': 'c70dae30-6834-42a4-a1f6-8b998e689591',
    'cache-control': 'no-cache'
    }
    
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    result = json.loads(response.text)

    #format Results
    all_suggestions = result['suggestions']
    max_length = len(all_suggestions)
    if len(all_suggestions) > 10:
        max_length = 10
        
    formatted_result = []
    for i in range(max_length):
        #print(all_suggestions[i])
        text, confidence = all_suggestions[i]['text'],all_suggestions[i]['confidence']
        formatted_result.append([text,confidence])
    #print(formatted_result)
    return(formatted_result)
    
# Get Trainings Data from API in list
def get_td (sentence, lang):
    response = textgen(sentence,lang)
    #json_data = json.loads(response.text)
    td = [item[0] for item in response if item[1] > 0.1]
    return td


# create training examples
def create_td (list_sentences):
    td = []
    for example in list_sentences:  
         td.append({'entities': [], 'query': example})
    return td


def keygen():
    k = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    return k


def create_flows_intents_actions (project, questions, answers):
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
        
    project['brains'][0]['flows'] = flows
    project['brains'][0]['intents'] = intents
    project['brains'][0]['actions'] = actions
    return project


def add_textgen (project, lang):
    intents = project['brains'][0]['intents']
    for i in range(len(intents)):
        examples = intents[i]['examples']
        in_tg = examples[0]['query']
        listtd = get_td (in_tg, lang)
        listtd.append(in_tg)
        examples = create_td (listtd)
        project['brains'][0]['intents'][i]['examples']=examples
    return project

def merge_flows (prjct_base,prjct_head):
    numberPrior = len(prjct_base['brains'][0]['flows'])

    for flow in prjct_head['brains'][0]['flows']:
        prjct_base['brains'][0]['flows'].append(flow)

    numberAfter = len(prjct_base['brains'][0]['flows'])

    print("Length of flows from {}, to {}".format(numberPrior,numberAfter))

    return prjct_base

def merge_intents (prjct_base,prjct_head):
    numberPrior = len(prjct_base['brains'][0]['intents'])
    for intent in prjct_head['brains'][0]['intents']:
        prjct_base['brains'][0]['intents'].append(intent)
    numberAfter = len(prjct_base['brains'][0]['intents'])
    print("Length of intents from {}, to {}".format(numberPrior,numberAfter))

    return prjct_base

def merge_actions (prjct_base,prjct_head):
    numberPrior = len(prjct_base['brains'][0]['actions'])
    for action in prjct_head['brains'][0]['actions']:
        prjct_base['brains'][0]['actions'].append(action)
    numberAfter = len(prjct_base['brains'][0]['actions'])

    print("Length of actions from {}, to {}".format(numberPrior,numberAfter))

    return prjct_base

def merge_integrations (prjct_base,prjct_head):
    existingActions = [integration['actionName'] for integration in prjct_base['integrations']]
    for integration in prjct_head['integrations']:
        if integration['actionName'] not in existingActions:
            prjct_base['integrations'].append(integration)
    return prjct_base

def remove_double_intents (project):
    count = {}
    intents = project['brains'][0]['intents']
    for intent in intents:
        if intent['intentId'] not in count:
            count[(intent["intentId"])] = 1
        elif intent['intentId'] in count:
            count[(intent["intentId"])] += 1
    
    for key in count:
        if count[key]>1:
            #print(key)
            for intent in intents:
                if intent['intentId'] == key:
                    intents.remove(intent)
                    count[key]-=1
                    #print("removed key")
                    break
            #remove intent
            # count -1 
    project['brains'][0]['intents'] = intents
    return project



def find_flow (project, flowname):
    for flow in project['brains'][0]['flows']:
        if flow['title']==flowname:
            return(flow)
    print("No flow found")



def find_action (project,actionId):
    for action in project['brains'][0]['actions']:
        if action['actionId']==actionId:
            return(action)
    print("No action found")
        
def find_integration (project,integrationId):
    for i in range(len(project['integrations'])):
        if project['integrations']['integrationId']==integrationId:
            print("integration index : ",i)
            return project['integrations'][i]

def find_handoff_ids (project, nameofflows):
    action_handoffs = []
    flows = project["brains"][0]['flows']
    for flow in flows:
        if flow['title'] in nameofflows:
            actionId = flow['steps'][-1]['actions'][-1]['actionId']
            action_handoffs.append(actionId)
    return action_handoffs

def add_handoff_event (project, action_handoffs):
    actions = project["brains"][0]['actions']
    for actionId in action_handoffs:
        for i in range(len(actions)):
            if actions[i]["actionId"] == actionId:
                project["brains"][0]['actions'][i]["payload"]["eventName"] = 'Handoff'
                #print(project["brains"][0]['actions'][i])
    return project
        

# fill opening with organization name and chatbot name
def create_opening (project, organizationName, chatbotName, lang):
    openingflow = find_flow (project, "02 Opening")
    firstactionId = openingflow['steps'][0]['actions'][0]['actionId']
    brainId = project['brains'][0]['brain']['brainId']
    
    opening = {'actionId': firstactionId,
     'brainId': brainId,
     'payload': {'texts': ['Welkom bij {}! Ik ben {}, jouw virtuele assistent.'.format((organizationName),chatbotName)],
      'quickReplies': [],
      'tags': []},
     'type': 'TEXT'}

    if lang == "en":
        opening = {'actionId': firstactionId,
        'brainId': brainId,
        'payload': {'texts': ['Welcome to {}! My name is {}, your Virtual Assistant.'.format((organizationName),chatbotName)],
        'quickReplies': [],
        'tags': []},
        'type': 'TEXT'}
    
    actions = project['brains'][0]['actions']
    for i in range(len(actions)):
        if actions[i]['actionId'] == firstactionId:
            print("index of opening actions ",i)
            project['brains'][0]['actions'][i]=opening
            
    return project


def create_card (topic, list_of_questions, imgurl):
    return {'title': 'Swipe en select below <👇>',
      'subtitle': topic,
      'buttons': create_button (list_of_questions),
      'media': create_media ('https://source.unsplash.com/featured/?'+str(topic))}


def create_button (list_of_questions):
    buttons = []
    for question in list_of_questions:
        buttons.append({'label': question, 'type': 'postback', 'value': question})
        if len(buttons)==3:
            continue
    return buttons

def create_media (imgurl):
    return {'type': 'image','url': imgurl}

def create_carousel (project, unique_topics, df):

    menuflow = find_flow (project, "03 Menu")
    carouselactionId = menuflow['steps'][1]['actions'][0]['actionId']
    brainId = project['brains'][0]['brain']['brainId']

    opening_carousel = {'actionId': carouselactionId,
     'brainId': brainId,
     'payload': {'fallback': '',
      'response': {'type': 'carousel',
       'payload': {'cards': []
                  }
                  },
      'tags': []},
     'type': 'CAROUSEL'}
    
    for topic in unique_topics:
        q = list(df.loc[df['Topic'] == topic, 'Questions'])
        card = create_card (topic, q, "imgurl")
        opening_carousel['payload']['response']['payload']['cards'].append(card)
    
    
    
    actions = project['brains'][0]['actions']
    for i in range(len(actions)):
        if actions[i]['actionId'] == carouselactionId:
            print("index of carousel actions ",i)
            project['brains'][0]['actions'][i]=opening_carousel
            
    
    return project
    


# # Replace Handoff email adress


def replace_handoff_email (project, supportemail):
    integration = project['integrations'][3]
    CC = integration['cloudCode']
    CC = CC.replace("Support Email",(supportemail))
    integration['cloudCoude']= CC
    project['integrations'][3]['cloudCode'] = CC
    return project






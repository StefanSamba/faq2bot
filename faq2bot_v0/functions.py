import random, string
import pandas as pd
import json
import requests

def keygen():
    k = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    return k
    
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

# Get Trainings Data from API in list
def get_td (sentence, lang):
    response = textgen(sentence,lang)
    json_data = json.loads(response.text)
    td = [item[0] for item in json_data]
    return td

# create training examples
def create_td (list_sentences):
    td = []
    for example in list_sentences:  
         td.append({'entities': [], 'query': example})
    return td

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

def add_textgen (project):
    intents = project['brains'][0]['intents']
    for i in range(len(intents)):
        examples = intents[i]['examples']
        in_tg = examples[0]['query']
        listtd = get_td (in_tg, "nl")
        listtd.append(in_tg)
        examples = create_td (listtd)
        project['brains'][0]['intents'][i]['examples']=examples
    return project


# merge projects
def merge_flows (prjct_base,prjct_head):
    for flow in prjct_head['brains'][0]['flows']:
        prjct_base['brains'][0]['flows'].append(flow)
    return prjct_base

def merge_intents (prjct_base,prjct_head):
    # brainId = prjct_base['brains'][0]['brain']['brainId']
    for intent in prjct_head['brains'][0]['intents']:
        prjct_base['brains'][0]['intents'].append(intent)
    return prjct_base

def merge_actions (prjct_base,prjct_head):
    # brainId = prjct_base['brains'][0]['brain']['brainId']
    for action in prjct_head['brains'][0]['actions']:
        prjct_base['brains'][0]['actions'].append(action)
    return prjct_base

def find_flow (project, flowname):
    for flow in project['brains'][0]['flows']:
        if flow['title']==flowname:
            return(flow)

def find_action (project,actionId):
    for action in project['brains'][0]['actions']:
        if action['actionId']==actionId:
            return(action)
        
def find_integration (project,integrationId):
    for i in range(len(project['integrations'])):
        if project['integrations']['integrationId']==integrationId:
            print("integration index : ",i)
            return project['integrations'][i]
        
def create_opening (project, organizationName, chatbotName):
    
    opening = {'actionId': '3d721dcc-0978-4604-824b-d6c904fc94a2',
     'brainId': '2233f6d1-2817-4ff2-bca4-e095918e66c8',
     'payload': {'texts': ['Welkom bij {}! Ik ben {}, jouw virtuele assistent.'.format((organizationName),chatbotName)],
      'quickReplies': [],
      'tags': []},
     'type': 'TEXT'}
    
    #print(project['brains'][0]['actions'][13])
    project['brains'][0]['actions'][13]=opening
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

#images only
def create_media (imgurl):
    return {'type': 'image','url': imgurl}

def create_carousel (df, project, unique_topics):
    opening_carousel = {'actionId': 'fa67d2e1-6b4e-42e1-9107-548a47282970',
     'brainId': '2233f6d1-2817-4ff2-bca4-e095918e66c8',
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
    
    project['brains'][0]['actions'][4] = opening_carousel
    return project

def replace_handoff_email (project, supportemail):
    integration = project['integrations'][3]
    CC = integration['cloudCode']
    CC = CC.replace("Support Email",(supportemail))
    integration['cloudCoude']= CC
    project['integrations'][3]['cloudCode'] = CC
    return project

def replace_text_in_reply (project, actionId, replace, replace_with):
    actions = project['brains'][0]['actions']
    for i in range(len(actions)):
        if actions[i]['actionId']==actionId:
            actions[i]['payload']['texts'][0] = actions[i]['payload']['texts'][0].replace(replace, replace_with)
    return project
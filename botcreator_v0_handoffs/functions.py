




# In[3]:


def find_unique_groups (project):
    u_groups = []
    flows = project['brains'][0]['flows']
    for flow in flows:
        if flow['group'] not in u_groups:
            u_groups.append(flow['group'])
   
    return (sorted(u_groups))


# In[4]:


def find_flow(project, flowtitle):
    flows = project['brains'][0]['flows']
    for flow in flows:
        if flow['title'] == flowtitle:
            return(flow)
        
def find_action(project, actionId):
    actions = project['brains'][0]['actions']
    for action in actions:
        if action['actionId'] == actionId:
            return(action)
        


# In[5]:


def tailor_carousel(project, actionId, topics):
    #tailors opening carousel to matching topics
    # inputs= project, actionID of carousel + list of topics
    # c8bf580a-d2cd-4f0f-9921-3f7f71018098
    new_cards = []
    actions = project['brains'][0]['actions']
    for action in actions:
        if action['actionId'] == actionId:
            cards = (action['payload']['response']['payload']['cards'])
            for card in cards:
                if card['title'] in topics:
                    new_cards.append(card)
    for i in range(len(actions)):
        if actions[i]['actionId']==actionId:
            print("Index of Opening carousel in list of Actions:",i)
            project['brains'][0]['actions'][i]['payload']['response']['payload']['cards'] = new_cards
    return(project)


# In[6]:


def disable_flows (project, selectables, selected):
    # Disable flows of non relevant groups
    flows = project['brains'][0]['flows']
    for flow in flows:
        if flow['group'] in selectables and flow['group'] not in selected:
            flow['disabled']=True
            #print("disabling flow : ", flow['title'])
    print("Non relevant flows/groups have been disabled")
    print()
    return project


# In[7]:


def find_action (project,integrationIitle):
    integrations = project['integrations'] 
    for i in range (len(integrations)):
        if integrations[i]['title']==integrationIitle:
            print("Index of",integrationIitle, "is", i)
            #print(integrations[i]['cloudCode'])
            return(i)
        
def replace_cloudcode (project, i, replace, replacewith):
    old_cloudcode = project['integrations'][i]['cloudCode']
    new_cloudcode = old_cloudcode.replace(replace,replacewith)
    project['integrations'][i]['cloudCode']=new_cloudcode
    print(replace,"is replaced with", replacewith, "in action",project['integrations'][i]['title'])
    return project


# In[8]:


def disable_menu(project, selectables, selected):
    # Disable non-relevant menuflows in group "01 Menu's"
    flows = project['brains'][0]['flows']
    for flow in flows:
        if flow['group'] ==  "01 Menu's":
            item = flow['title'].split()[-1] 
            if item in selectables and item not in selected:
                flow['disabled']=True
                print("Disabling menu:", flow['title'])
    print()

    return project


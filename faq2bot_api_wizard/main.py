from flask import Flask, jsonify, request
from functions import *

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])

def index():
    if(request.method == 'POST'):
        api_input = request.get_json()
        textgen = api_input['textgen']
        lang = api_input['language']

        df = pd.DataFrame()
        questions=list(api_input['questions'])
        answers=list(api_input['answers'])
        df['Topic']=list(api_input['topics'])
        df['Questions']=list(api_input['questions'])
        df['Answers']=list(api_input['answers'])
        
        chatbotName = api_input['chatbotName']
        organizationName = api_input['organizationName']
        supportEmail = api_input['supportEmail']
        handoffType = api_input["handoffType"]


        #return metric
        print("start running")
        with open('export.json') as json_file:
            data = json.load(json_file)

        print("Preparing Data")
        # Work with XSLX and define variables
        #n_items = max(df.count())

        print("Data Prepared")

        #create from excel
        data = create_flows_intents_actions (data, questions, answers)

        print("Adding Training Examples")
        
        b = data
        if textgen == 'true':
            b = add_textgen (data, lang)
        
        with open('general_{}.json'.format(lang)) as json_file:
            a = json.load(json_file)


        print("Merging with base")
        new = merge_flows (a,b)
        new = merge_intents (new,b)
        merged = merge_actions (new,b)

        with open('handoff/handoff_{}_{}.json'.format(handoffType,lang)) as json_file:
            handoff = json.load(json_file)        

        print("Merging with Handoff")
        merged = merge_flows (merged,handoff)
        merged = merge_intents (merged,handoff)
        merged = merge_actions (merged,handoff)
        merged = merge_integrations(merged,handoff)
        merged = remove_double_intents (merged)

        # add Feedback event to:
        handoff_en = ["04 Talk to agent", "05 Unknown", "06 Feedback"]
        handoff_nl = ["04 Medewerker spreken", "05 Onbekend", "06 Feedback"]

        if lang == "en":
            action_handoffs = find_handoff_ids (merged, handoff_en)
        if lang =="nl":
            action_handoffs = find_handoff_ids (merged, handoff_nl)

        merged = add_handoff_event (merged, action_handoffs)


        # ADD HANDOFF EVENT TO
        # Feedback Negative, Talk To Agent, Unknown
        #if handoffType == "ticket":
         #   merged = replace_handoff_email (merged, supportEmail)

        print("Tailoring Opening, Menu and Support")
        merged = create_opening (merged, organizationName, chatbotName,lang)
        unique_topics = sorted(df.Topic.unique())
        merged = create_carousel (merged, unique_topics,df)


        #with open('merged_projects.json', 'w') as f:
        #    json.dump(merged, f)

        print("Done")

        return merged
    else:
        return jsonify({"about":"Flow.ai Botgenerator API"})


if __name__ == '__main__':
    app.run(debug=True)
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

        print("Tailoring Opening, Menu and Support")
        merged = create_opening (merged, organizationName, chatbotName,lang)
        unique_topics = sorted(df.Topic.unique())
        merged = create_carousel (merged, unique_topics,df)
        merged = replace_handoff_email (merged, supportEmail)


        #with open('merged_projects.json', 'w') as f:
        #    json.dump(merged, f)

        #print("Done")

        return merged
    else:
        return jsonify({"about":"Flow.ai Botgenerator API"})


if __name__ == '__main__':
    app.run(debug=True)
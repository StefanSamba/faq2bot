from flask import Flask, jsonify, request
from functions import *

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])

def index():
    if(request.method == 'POST'):
        api_input = request.get_json()
        textgen = api_input['textgen']
        lang = api_input['language']
        excel = api_input['excelurl']

        #return metric
        print("start running")
        with open('export.json') as json_file:
            data = json.load(json_file)

        print("Preparing Data")
        # Work with XSLX and define variables
        xls = pd.ExcelFile(excel)
        df1 = pd.read_excel(xls, "FAQ's")
        df = pd.DataFrame()
        df['Questions']=list(df1['Question'])
        df['Answers']=list(df1['Answer'])
        df['Topic']=list(df1['Topic'])
        n_items = max(df.count())
        qa = df[:n_items]

        # get Organization Info
        df2 = pd.read_excel(xls, "Introduction")
        df2.columns = ['row', 'faq2bot instruction', 'none', 'label', 'value']
        orgdict = df2.set_index('label')['value'].to_dict()
        questions = list(qa['Questions'])
        answers = list(qa['Answers'])

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
        merged = create_opening (merged, orgdict['Organization'], orgdict['Chatbot Name'],lang)
        unique_topics = sorted(df.Topic.unique())
        merged = create_carousel (merged, unique_topics,df)
        merged = replace_handoff_email (merged, orgdict['Support Email'])


        with open('merged_projects.json', 'w') as f:
            json.dump(merged, f)

        #print("Done")

        return merged
    else:
        return jsonify({"about":"Flow.ai FAQ2BOT API"})


if __name__ == '__main__':
    app.run(debug=True)
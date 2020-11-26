from flask import Flask, render_template, request, url_for,send_from_directory,redirect, Response
import os
from werkzeug.utils import secure_filename
import pandas as pd
import requests
import json


ALLOWED_EXTENSIONS = {'xlsx'}    
UPLOAD_FOLDER = './uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = './results/'

@app.route("/")
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods = ['POST'])
def upload():
    file=request.files['inputFile']
    filename = secure_filename(file.filename)
    print("filename", filename)    

    # TBD
    if filename != "":
        if not allowed_file(filename):
            return "FileError: Only .CSV"
        elif allowed_file(filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))    
            return redirect(url_for('uploaded_file', filename=filename))
            #return filename


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print('Routed to uploaded file...')

    # change to app.config['RESULT_FOLDER']
    #df = pd.read_csv(
        
    filepath = app.config['UPLOAD_FOLDER']+str(filename)

    print("Preparing Data")
    # Work with XSLX and define variables

    xls = pd.ExcelFile(filepath)

    # check if tab exists or error
    df1 = pd.read_excel(xls, "FAQ's")
    df = pd.DataFrame()
    df['Questions']=list(df1['Question'][:10])
    df['Answers']=list(df1['Answer'][:10])
    df['Topic']=list(df1['Topic'][:10])
    n_items = max(df.count())
    qa = df[:n_items]

# get Organization Info
    df2 = pd.read_excel(xls, "Introduction")
    df2.columns = ['row', 'faq2bot instruction', 'none', 'label', 'value']
    orgdict = df2.set_index('label')['value'].to_dict()
    questions = list(qa['Questions'])
    answers = list(qa['Answers'])
    topics = list(qa['Topic'])

    textgen = "false"
    if orgdict["Data Augmentation"] == "yes":
        textgen = "true"

    for key in orgdict:
        print('orgdict["{}"]'.format(key))

    print("Data Prepared")
    print("Starting Request")

    print(f"questions: {questions}")



    url = "https://botcreator.ew.r.appspot.com/"

    payload = json.dumps({
        "textgen": textgen,
        "language": orgdict["Language"],
        "questions": questions,
        "answers": answers,
        "topics": topics,
        "chatbotName": orgdict["Chatbot Name"],
        "organizationName": orgdict["Organization"],
        "supportEmail": orgdict["Support Email"],
        "handoffType": orgdict["Handoff Type"]
    })

    headers = {
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, data = payload)
    content = json.loads(response.text)
    return Response(json.dumps(content), mimetype='application/json', headers={"Content-disposition":
                 "attachment; faq2bot_upload_to_flowai.json"})



    print("Response received & returning file")


    ## SEND RESULT TO USER
    #content = str(request.form['jsonval'])
    #return Response(content, 
    #        mimetype='application/json',
     #       headers={'Content-Disposition':'attachment;filename=faq2botupload'})
    


if __name__ == '__main__':
    app.run(debug=True)

    
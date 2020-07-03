from flask import Flask, request, jsonify
import json
from functions import find_flow, tailor_carousel, disable_flows, disable_menu, find_action, replace_cloudcode

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def index():
    if(request.method == 'POST'):
        data = request.get_json()
        selectables = ["Account","Bestellen","Betalen","Bezorgen","Garantie","Retourneren","Product", "Service","Contact", "Handoff Livechat", "Handoff Bot only", "Handoff Ticket"]
        topics = data["picked_topics"]
        handoff_type = data["handoff_type"]
        with open('retailbot_handoffs.json') as json_file:
            project = json.load(json_file)
        actionIdOpening = find_flow(project, "Menuopties")['steps'][0]['actions'][0]["actionId"]
        selected = topics
        project = tailor_carousel(project, actionIdOpening, selected)
        project = disable_flows (project, selectables, selected)
        project = disable_menu(project, selectables, selected)
        if handoff_type == "Handoff Ticket":
            support_email = data['support_email']
            i_send_email = find_action (project,"Send Email")
            project = replace_cloudcode(project,i_send_email,'naam@domein.nl',support_email)
        return jsonify(project)
    else:
        return jsonify({"about":"Flow.ai Bot Creator API"})

        
if __name__ == '__main__':
    app.run(debug=True)



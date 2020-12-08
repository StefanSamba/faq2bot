# FAQ2BOT API

Faq2bot is a Python API for generating bots in a Flow.ai format.

## How it works

This service allows you to easily create the first set-up of your AI chatbot by generating a .json file that represents that bot.

The generated .json file consists of 3 components:
1. Base template: This includes general flows like a greeting, menu, and feedback an are stored in `general_en.json` and `general_nl.json`
2. API Input: The input of the API (see below) will tailor the bot to your needs by incorporating questions, answers, topics, and organization data.
3. Handoff Type: The handoff covers 3 possible handoff scenarios `botonly`, `ticket`, and `livechat`. Just like 1. Base Templates, these handoff types are also stored as templates within the `/handoff` folder

The API is publish on Google App Engine
```https://botcreator.ew.r.appspot.com/```


## Usage

Curl
```bash
curl --location --request POST 'https://botcreator.ew.r.appspot.com/' \
--header 'Content-Type: application/json' \
--data-raw '{
        "textgen": "false",
        "language": "en",
        "questions": ["What food can I order?", "Do you deliver?"],
        "answers": ["We'\''ve got a broad variety of dishes.", "We deliver for free to any Flow-designer"],
        "topics": ["Food","Delivery"],
        "chatbotName": "Pablo",
        "organizationName": "Pablo'\''s dishes",
        "supportEmail": "stefan+faq2bot@flow.ai",
        "handoffType": "ticket"
    }'
```

Python

```Python
import requests
import json

url = "https://botcreator.ew.r.appspot.com/"

payload={"textgen" : "true",
         "language": "en",
         "questions": ["how do I order food", "where is the sea?"],
         "answers": ["You can always use Uber Eats", "Roll down the hill and you will find it or get stuck in a local minima."],
         "topics": ["food", "sea"],
         "chatbotName": "Pablo",
         "organizationName": "SambaBV",
         "supportEmail": "support@sambabv.nl",
         "handoffType": "livechat"}

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
content = json.loads(response.text)
print(content)

```
## Variables 

textgen: generates training examples via Flow.ai Data Augmentation API: `true` or `false`

language: set available language of base template `en` or `nl`

questions: list of strings `["how do I order food", "where is the sea?"]`

answers: list of strings `["You can always use Uber Eats", "Roll down the hill and you will find it or get stuck in a local minimum."]`

topics: list of strings `["food","sea"]`

chatbotName: string, name of your chatbot `Pablo`

organizationName: string, name of the organization `"SambaBV`

supportEmail: string, email address to send email handoff tickets to `"support@flow.ai"`

handoffType: string, type of handoff `livechat`, `botonly`, or `ticket`

## Future Work
For the future we can easily scale in 2 ways. The first is to add different languages (e.g. Spanish by adding `general_es` and 3 handoff types in `es`) Perhaps we can even do this with Auto-Translate? Second, we can incorporate different use cases by create different base templates (e.g. a lead generation template).
## License
[Flow.ai](http://flow.ai/)
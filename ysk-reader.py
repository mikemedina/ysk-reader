from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode


username = ''
password = ''

app = Flask(__name__)
ask = Ask(app, "/ysk-reader")

def get_headlines():
    user_pass_dict = {'user': username,
                      'password': password,
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: ' + username})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)

    time.sleep(1)

    url = 'https://reddit.com/r/youshouldknow/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))

    titles = ['You should know ' + unidecode.unidecode(listing['data']['title'])[4:]  # Skip "YSK "
            for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])

    return titles  

@ask.launch
def start_skill():
    return share_headlines()

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = "Here's some useful information: {} ... Cool huh?".format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Alright, bye then!'
    return statement(bye_text)
    
if __name__ == '__main__':
    app.run(debug=True, port=5002)


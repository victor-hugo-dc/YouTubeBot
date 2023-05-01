# import sys
# sys.path.insert(0, 'vendor')

import urllib.request
import json
import requests
import re

PREFIX = '~'

def receive(event, context):
    message = json.loads(event['body'])

    bot_id = message['bot_id']
    response = process(message)
    if response:
        send(response, bot_id)

    return {
        'statusCode': 200,
        'body': 'ok'
    }


def process(message):
    # Prevent self-reply
    if message['sender_type'] == 'bot':
        return None
    
    if message['text'].startswith(PREFIX):
        query = message['text'][len(PREFIX):].strip().replace(" ", "%20")
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
        videos = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        reply = "https://www.youtube.com/watch?v=" + videos[0]
        return reply
    

def send(text, bot_id):
    url = 'https://api.groupme.com/v3/bots/post'

    message = {
        'bot_id': bot_id,
        'text': text,
    }
    r = requests.post(url, json=message)
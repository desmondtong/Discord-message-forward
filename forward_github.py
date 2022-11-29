import json
import threading
import time
import websocket
from discord_webhook import DiscordWebhook

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws) :
    response = ws.recv( )
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print('Heartbeat begin')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")

def extract(event):
    username = event['d']['author']['username']
    content = event['d']['content'].removesuffix('@deleted-role @deleted-role')
    if event['d']['attachments'] != []:
        attachments = event['d']['attachments'][0]['url']
    else:
        attachments = ''
    message = f"{username}: \n{content} \n{attachments}"
    return message

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

#discord authorization ID
token = ''
payload = {
    'op': 2,
    'd': {
        'token': token,
        'properties': {
            '$os': 'windows',
            '$browser': 'chrome',
            '$device': 'pc'
        }
    }
}
send_json_request(ws, payload)

while True:
        event = recieve_json_response(ws)
        
        try:
            if event['d']['channel_id'] == '' and event['d']['guild_id'] == '':
                message = extract(event)
                print(message)
                
                webhook = DiscordWebhook(url='', content = message)
                response = webhook.execute()

            elif event['d']['channel_id'] == '' and event['d']['guild_id'] == '':
                message = extract(event)
                print(message)
                
                webhook = DiscordWebhook(url='', content = message)
                response = webhook.execute()                
            
            elif event['d']['channel_id'] == '' and event['d']['guild_id'] == '':
                message = extract(event)
                print(message)
                
                webhook = DiscordWebhook(url='', content = message)
                response = webhook.execute()

            else:
                pass
        except:
            pass

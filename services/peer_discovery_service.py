import os.path, sys
import json
import requests
import eventlet
from config import port

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def check_live_status(ip):
    endpoint = 'http://' + ip + ':' + port + '/status'
    try:
        with eventlet.Timeout(10):
            response = requests.get(endpoint)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def get_active_peers():
    with open('resources/peers.json') as data:
        peers = json.load(data)

    peerList = {}
    for ip, status in peers.items():
        if check_live_status(ip):
            peerList[ip] = "Active"

    with open('resources/peers.json') as data:
        peers = json.load(data)

    with open('resources/peers.json', mode = 'w') as file:
        for peer in peerList:
            peers[peer] = "Active"
        file.write(json.dumps(peers))
    return peerList

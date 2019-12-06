import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import json
import requests
from config import MY_IP, port

def sync_peer_data(remote_ip):
    #Merge remote peer data into local
    endpoint = 'http://' + remote_ip + ':5000' + '/peers_json'
    try:
        resp = requests.get(endpoint)
        remote_peer_list = {}
        if resp.status_code == 200:
            remote_peer_list = json.loads(resp.text)
    except:
        return {"failed" : "remote_ip_dead"}

    for ip, status in remote_peer_list.items():
        if ip != MY_IP:
            updateEndpoint = 'http://' + MY_IP + ':5000' + '/peers/' + ip + '/' + status
            updateStatus = requests.post(updateEndpoint)

    endpoint = 'http://' + MY_IP + ':5000' + '/peers_json'
    resp = requests.get(endpoint)
    remote_peer_list = {}

    if resp.status_code == 200:
        remote_peer_list = json.loads(resp.text)

    for ip, status in remote_peer_list.items():
        if ip != remote_ip:
            updateEndpoint = 'http://' + remote_ip + ':5000' + '/peers/' + ip + '/' + status
            updateStatus = requests.post(updateEndpoint)

    return {"success" : "Synced"}

def get_peer_data():
    with open('resources/peers.json') as data:
        peers = json.load(data)

    return peers

def send_peer_data(ip, status):
    with open('resources/peers.json') as data:
        peers = json.load(data)

    with open('resources/peers.json', mode = 'w') as file:
        peers[ip] = status
        file.write(json.dumps(peers))

    return {'success' : '200'}

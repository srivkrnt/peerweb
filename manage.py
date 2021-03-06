from flask import Flask, render_template, send_file
import flask
import json
from services.peer_discovery_service import get_active_peers
from services.peer_sync_service import send_peer_data, get_peer_data, sync_peer_data
from services.file_service import get_file_list, file_exist
from flask import request, jsonify
from config import MY_IP, port
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('about.html')

@app.route('/files')
def files():
    fileList = get_file_list()
    return render_template('download.html', fileList = fileList, MY_IP = MY_IP , port=port)

@app.route('/files/get/<file_name>')
def return_file(file_name):
    if file_exist(file_name):
        return send_file('./resources/files/' + file_name)
    else:
        return render_template('error.html')

@app.route('/404')
def error():
    return render_template('error.html')

@app.route('/peers')
def all_peers():
    peerData = get_peer_data()
    peers = [peer for peer,status in peerData.items()]
    status = [status for peer, status in peerData.items()]
    return render_template('peers.html', synced = -1, peers = peers, status = status, port = port)

@app.route('/peers_json')
def all_peers_json():
    peerData = get_peer_data()
    return jsonify(peerData)

@app.route('/peers/active')
def discover_peers():
    return jsonify(get_active_peers())

@app.route('/peers/<ip>/<status>', methods = ['POST'])
def update_peer_list(ip, status):
     send_peer_data(ip, status)
     return jsonify({'success' : 'IP added'})

@app.route('/peers/sync/<ip>')
def sync_peer_list(ip):
    peerData = get_peer_data()
    peers = [peer for peer,status in peerData.items()]
    status = [status for peer, status in peerData.items()]
    synced = sync_peer_data(ip)
    if synced == True:
        synced = 1
    else:
        synced = 2
    return render_template('peers.html', port = port, synced = synced, peers = peers, status = status)

@app.route('/status')
def status():
    return render_template('status.html')

if __name__ == "__main__":
    app.run(host = '0.0.0.0')

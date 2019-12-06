from flask import Flask, render_template
import flask
import json
from services.peer_discovery_service import get_active_peers
from services.peer_sync_service import send_peer_data, get_peer_data, sync_peer_data
from flask import request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('about.html')

@app.route('/peers')
def all_peers():
    peerData = get_peer_data()
    peers = [peer for peer,status in peerData.items()]
    status = [status for peer, status in peerData.items()]
    return render_template('peers.html', peers = peers, status = status)

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
    return jsonify(sync_peer_data(ip))

@app.route('/status')
def status():
    return render_template('status.html')

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0')

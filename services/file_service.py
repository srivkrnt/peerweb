import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import requests
from config import port

def send_file(ip, sourceFileName):
    sourceFileLocation = './resources/files/' + sourceFileName
    files = {'file' : open(sourceFileLocation, 'rb')}
    try:
        endpoint = 'http://' + ip + ':' + port
        resp = requests.post(endpoint, files = files)
        print(resp.text)
        return {"success" : "200"}
    except Exception as e:
        print(e)
        return {"failed" : "400"}

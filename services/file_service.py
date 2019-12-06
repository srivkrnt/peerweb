import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import requests
import json
import os
from config import port

def generate_file_metadata():
    with open('resources/files/metadata.json') as data:
        fileList = json.load(data)
    files = [f for f in os.listdir('./resources/files')]

    tempFileList = {"files" : []}

    for file in fileList["files"]:
        if file in files:
            tempFileList["files"].append(file)

    for file in files:
        if file != "metadata.json" and file not in tempFileList["files"]:
            tempFileList["files"].append(file)

    with open('resources/files/metadata.json', mode = 'w') as file:
        file.write(json.dumps(tempFileList))

def file_exist(file_name):
    generate_file_metadata()
    with open('resources/files/metadata.json') as data:
        fileList = json.load(data)
    return file_name in fileList["files"]

def get_file_list():
    generate_file_metadata()
    with open('resources/files/metadata.json') as data:
        fileList = json.load(data)
    return fileList["files"]

from flask import Flask, request
from flask_cors import CORS
import sendMSG
import configparser
import sys
import os
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

contactConfig = configparser.RawConfigParser()

greetingServer = Flask(__name__)
CORS(greetingServer)
providers = {"att" : "@mms.att.net", "tmobile":"@tmomail.net", "verizon": "@vzwpix.com", "email":""}

@greetingServer.route("/")
def rootFile():
    contactConfig.read("carWatcher.cfg")
    return contactConfig.get("DATA","ID")

@greetingServer.route("/add")
def addNumber():
    if(request.args.get('number') == None):
        return "errnonumber"
    numbPassed = request.args.get('number')
    emailPassed = request.args.get('email')
    endPassed = ""
    for i in range(len(numbPassed)):
        if(ord(numbPassed[i]) >= 48 and ord(numbPassed[i]) <= 58):
            endPassed += numbPassed[i]
    if(emailPassed == None or emailPassed not in providers):
        return "bademail"
    providerEmail = providers[emailPassed]
    contactConfig.read("carWatcher.cfg")
    if(len(contactConfig.get("DATA","EMAILS")) > 0):
        contactConfig.set("DATA","EMAILS",contactConfig.get("DATA","EMAILS") +","+ (endPassed+providerEmail))       
    else:
        contactConfig.set("DATA","EMAILS",contactConfig.get("DATA","EMAILS") + (endPassed+providerEmail))       

    with open("carWatcher.cfg", "w") as configfile:
        contactConfig.write(configfile)
    return "success"


def returnHTMLCode(fileName):
    filepath = sys.path[0] + '/'+fileName
    exists = os.path.isfile(filepath)
    if exists:
        # Store configuration file values
        f = open(filepath, 'r')
        fileConts = f.read()
        f.close()
        return fileConts
    else:
        return "<h1>404 file not found!</h1>"
        

@greetingServer.route('/index.html')
def index():
    return returnHTMLCode("index.html")

@greetingServer.route('/css/<string:filename>')
def show_css(filename):
    filepath = sys.path[0] + '/css/'+filename
    exists = os.path.isfile(filepath)
    if exists:
        # Store configuration file values
        f = open(filepath, 'r')
        fileConts = f.read()
        f.close()
        return fileConts
    else:
        return "<h1>404 file not found!</h1>"
        
@greetingServer.route('/js/<string:filename>')
def show_js(filename):
    filepath = sys.path[0] + '/js/'+filename
    exists = os.path.isfile(filepath)
    if exists:
        # Store configuration file values
        f = open(filepath, 'r')
        fileConts = f.read()
        f.close()
        return fileConts
    else:
        return "<h1>404 file not found!</h1>"

'''
if __name__ == "__main__":
    greetingServer.run(host='localhost', port=80)
'''
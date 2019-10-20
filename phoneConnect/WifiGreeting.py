from flask import Flask, request
from flask_cors import CORS
import sendMSG
import configparser

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


'''
if __name__ == "__main__":
    greetingServer.run(host='localhost', port=80)
'''
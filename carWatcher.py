# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)

sys.path.append('./sendText')
sys.path.append('./site')
sys.path.append('./vision')
sys.path.append('./phoneConnect')
sys.path.append('./captive')
sys.path.append('./heatSensor')

from random import randrange
import configparser
from threading import Thread
import time
import tempWarner as temperatureSensor
import DiffPerson as camera
import sendText as sendEmail
import wifiSetup


global average
tempCheckDelay = 60
pictureDelay = 60


def testTemperature():
    while True:
        if temperatureSensor.isHot():
            if camera.different(average):
                config = configparser.RawConfigParser()
                config.read('phoneConnect/carWatcher.cfg')
                camera.savePicture()
                sendEmail.sendText(config.get("DATA","EMAILS").split(','))
        time.sleep(tempCheckDelay)

def takePictures():
    time.sleep(pictureDelay)
    if average == None:
        average = camera.average() #ideally we would average over time, not just over a few seconds
        
def websiteWatcher():
    print("running")
    import WifiGreeting
    WifiGreeting.greetingServer.run(host='localhost', port=179)

def startNgrok():
    wifiSetup.create()


"""
config = configparser.RawConfigParser()
config.read('phoneConnect/carWatcher.cfg')




id = config.get("DATA","ID")
if id=="":
    id = str(randrange(99999999))
    config.set("DATA","ID",id)
    with open('phoneConnect/carWatcher.cfg',"w") as configfile:
        config.write(configfile)
    
emails = config.get("DATA","EMAILS")
subjects = emails.split(",")

    

config.read('phoneConnect/carWatcher.cfg')
emails = config.get("DATA","EMAILS")
subjects = emails.split(",")
"""


average = camera.average()


tempThread = Thread(target = testTemperature)
#cameraThread = Thread(target = takePictures)
websiteThread = Thread(target = websiteWatcher)
ngrokThread = Thread(target = startNgrok)

tempThread.setDaemon(True)
#cameraThread.setDaemon(True)
websiteThread.setDaemon(True)
ngrokThread.setDaemon(True)

tempThread.start()
#cameraThread.start()
websiteThread.start()
ngrokThread.start()

while True:
    pass

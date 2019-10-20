# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('/path/to/application/app/folder')


from random import randrange
import configparser
from threading import Thread
import time
import temperatureSensor
import camera
import sendEmail
import wifiSetup



tempCheckDelay = 60
pictureDelay = 3600


def testTemperature():
	while True:
		if temperatureSensor.isHot():
			if camera.different(average):
				config = configparser.RawConfigParser()
				config.read('carWatcher.cfg')
				camera.savePicture()
				sendEmail.sendText(config.get("DATA","EMAILS").split(','))
		time.sleep(tempCheckDelay)

def takePictures():
	time.sleep(pictureDelay)
	if average == None:
		global average = camera.average() #ideally we would average over time, not just over a few seconds
		
def websiteWatcher():
	import WifiGreeting

config = configparser.RawConfigParser()
config.read('carWatcher.cfg')




id = config.get("DATA","ID")
if id=="":
	id = str(randrange(99999999))
	config.set("DATA","ID",id)
	with open('carWatcher.cfg',"w") as configfile:
		config.write(configfile)
	
emails = config.get("DATA","EMAILS")#how do config files look??
subjects = emails.split(",")

#if len(subjects) == 0:
#	wifiSetup.create(id)
	

config.read('carWatcher.cfg')
emails = config.get("DATA","EMAILS")
subjects = emails.split(",")



tempThread = Thread(target = testTemperature)
cameraThread = Thread(target = takePictures)
websiteThread = Thread(target = websiteWatcher)

tempThread.setDaemon(True)
cameraThread.setDaemon(True)
websiteThread.setDaemon(True)

tempThread.start()
tempThread.start()
cameraThread.start()

while True:
	pass

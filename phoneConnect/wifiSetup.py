import os
import sys
from pyngrok import ngrok
import configparser
import RPi.GPIO as GPIO


def create():
    contactConfig = configparser.RawConfigParser()
    contactConfig.read("phoneConnect/carWatcher.cfg")
    URL = ngrok.connect()
    urlID = URL.split("//")[1].split(".")[0]
    print(urlID)
    contactConfig.set("DATA","ID",urlID)       

    with open("carWatcher.cfg", "w") as configfile:
        contactConfig.write(configfile)
    
    while True:
        1 == 1
#create()


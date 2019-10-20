from PyAccessPoint import pyaccesspoint
import atexit

access_point = None

def create(networkName):
	access_point = pyaccesspoint.AccessPoint(ssid=networkName, ip="192.168.0.10")
	access_point.start()
	

@atexit.register
def exit():
	access_point.stop()
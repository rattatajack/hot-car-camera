import sys
import Adafruit_DHT as ad
import time

    




def isHot():
    lowerLimit = 80

    maxedOutTimes = 0
    timeDelay = 1
    timesToCheck = 20

    timesToWarn = 5
    for i in range(timesToCheck):
        
        h, t = ad.read_retry(11,4)
        faren = t * (9/5) + 32
        if(faren >= lowerLimit):
            maxedOutTimes+= 1
        else:
            maxedOutTimes -= 1
            maxedOutTimes = max(maxedOutTimes, 0)
        print(faren, "maxedOutTimes:", maxedOutTimes)
        if(maxedOutTimes >= timesToWarn):
            return True
        time.sleep(timeDelay)
    return False
    
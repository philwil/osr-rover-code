import time
#from Display import display
#from Updater import updater
#import Feature
import os
import threading
import socket

'''
Monitor water level every 10 seconds
If greater than xxx turn on pump for yyy
if not switched less than zzz turn off pump in xxx

Also monitor switch.
If switch changed to 0 set switched turn on pump for xxx secs 
log pump on time to sql
log event in sql
send mail when done
'''

switch = 1
lastSwitch = 0
lastdata = 0
level=6
pumpTime=0
maxPumpTime=10
switchPumpTime=2
maxLevel= 5
pump = "off"

class Pump:
    ' Pump Class '

    def __init__(self, maxTime, switchTime, state):
        self.time = 0
        self.maxTime = maxTime
        self.switchTime = switchTime
        self.state = state

class Level:
    ' Water Level Class'

    def __init__(self, maxLevel, pump, timeout=0.01, retries=3):
	self.maxLevel = maxLevel
	#self._port = comport
	self.pump = pump
        print pump
        self.timeout = timeout;
        self._trystimeout = retries
        self._crc = 0;

    def testLevel(self, level):
        #global level
        #global maxLevel
        #global pump
        #global pumpTime
        #global maxPumpTime
        print ">>testLevel"
        if(level > self.maxLevel) :
            print ">>turn on pump"
            self.pump.state = "on"
            self.pump.time = self.pump.maxTime

        if(level > 0):
            level = level -1;
        print ">>testLevel done"
        return 1


def testLevel():
    global level
    global maxLevel
    global pump
    global pumpTime
    global maxPumpTime
    print "testLevel"
    if(level > maxLevel) :
        print "turn on pump"
        pump = "on"
        pumpTime = maxPumpTime

    if(level > 0):
        level = level -1;
    print "testLevel done"
    return 1

def testSwitch():
    global switch
    global lastSwitch
    global pump
    global pumpTime
    global switchPumpTime
    print "testSwitch"
    if(switch > lastSwitch):
        print "testSWitch 1"
        if(switch == 0):
            if(pump == "off") :
                print "switch on pump"
                pump = "on"
                pumpTime = switchPumpTime
    else:
        print "testSWitch 2"
    lastSwitch = switch
    print "testSWitch done"
    return 1
                
def testPump():
    global pump
    global pumpTime
    print "testPump"
    if(pump == "on"):
        pumpTime = pumpTime -1
    if(pumpTime <= 0):
        pump = "off"
        print "turn off pump"
        raise 0
    return 1
    
def closedown():
    pump = "off"
    print "close down"
        
def main():
	myPump = Pump(10, 2, "off")
	myLevel = Level(6, myPump)
	#myScreenUpdater.createServer()
	#screenSock = myScreenUpdater.server
	#dataListThread = threading.Thread
	#screenSock.setblocking(0)
	lastdata = -1
        #testLevel()
        #testSwitch()
        #testPump()

        
	while True:
            try:
                testLevel()
                testSwitch()
                testPump()
            except:
                print "breaking loop"
		break
        closedown()
        
        myLevel.testLevel(8)
        myLevel.testLevel(4)
        
if __name__ == '__main__':
	main()

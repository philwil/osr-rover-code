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


# this is a test command class
# "set_switch 1 on"

class CommandList:
    ' a dedicated list of commands'
    def __init__(self, name):
        self.name = name
        self.list = []
        self.id = 0
    
class Command:
    ' Command class to process a command line '
    id = 0
    #list = []
    def __init__(self, cl, key, desc, action, env=""):
        self.key = key
        self.desc = desc
        self.action = action
        self.id = cl.id
        self.cl = cl
        self.env = env
        cl.id += 1
        cl.list.append(self)
        
    def runCommand(self, command):
        wds = command.split()
        print wds
        for c in self.cl.list:
            if c.key == wds[0]:
                print "Command match " + c.key + " -->" + command
                if c.action :
                    c.action(self, c, command)
                    return 0

    def CmdHelp(self, cmd, cmdstring):
        for c in self.cl.list:
            print "Command key " + c.key + " desc .." + c.desc

def CmdSwitch(xxx, cmd, cmdstring):
    print "Switch " + cmd.key + " desc" + cmd.desc
    

class Switch:
    ' Switch Class '
    switchId = 0
    list = []
    def __init__(self, pump, state, gpio=0):
        self.state = state
        self.pump = pump
        self.pumpTime = 2
        self.gpio = gpio
        #global switchId
        self.id = Switch.switchId
        Switch.switchId += 1
        Switch.list.append(self)
        
    def setState(self, state):
        self.state = state
        print ">>switch state " + state

    def testSwitch(self, state):
        #global switch
        #global lastSwitch
        #global pump
        #global pumpTime
        #global switchPumpTime
        print "testSwitch" + state
        if(state != self.state):
            print "testSWitch change from " + self.state + " to " + state
            self.state = state
            if( state == "on"):
                print ">>switch new state on pump " + self.pump.getState()
                if(self.pump.getState() == "off") :
                    print ">>switch on pump"
                    self.pump.setState("on")
                    self.pump.setTime (self.pumpTime)
            else:
                print ">>switch off pump"
                self.pump.setState("off")
                self.pump.setTime (0)

                
        else:
            print "testSwitch no change " + state

        print "testSWitch done"
        return 1

        
class Pump:
    ' Pump Class '

    def __init__(self, maxTime, switchTime, state):
        self.time = 0
        self.maxTime = maxTime
        self.switchTime = switchTime
        self.state = state
        
    def setState(self, state):
        self.state = state
        print ">>pump state " + state

    def getState(self):
        return self.state

    def setTime(self, ptime):
        self.ptime = ptime
        print ">>pump time " + str(ptime)
        
        
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
        self.level =  level
        if(level > self.maxLevel) :
            self.pump.setState("on")
            self.pump.setTime (self.pump.maxTime)

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
	mySwitch = Switch(myPump, "off")
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
                time.sleep(0.1)
                
            except:
                print "breaking loop"
		break
        closedown()
        
        myLevel.testLevel(8)
        myLevel.testLevel(4)
        myPump.setState("off")

        mySwitch.testSwitch("on")
        mySwitch.testSwitch("off")
        #mySwitches.append(mySwitch)
        foo = Switch(myPump, "on")
        foo = Switch(myPump, "on")
        
        #print mySwitches
        for switch in Switch.list:
            print switch.id

        Xl1 = CommandList("list1")
        Xl2 = CommandList("list2")
        x=Command(Xl1, "help", " this is the help", Command.CmdHelp)
        Command(Xl1, "set_switch", "set_switch on / off ", CmdSwitch)
        x.runCommand("help xl1 this is what I need")            
        # we can copy the class


        
        x2=Command(Xl2,"help", " xC this is the help", Command.CmdHelp)
        Command(Xl2,"get_switch", " xC get_switch on / off ", CmdSwitch)
        x2.runCommand("help this is what I need from xl2")
        x.runCommand("help this is what I need from xl1")
        
if __name__ == '__main__':
	main()

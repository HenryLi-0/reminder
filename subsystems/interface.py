'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time, random, ast
from subsystems.render import *
from subsystems.fancy import *
from subsystems.simplefancy import *
from subsystems.visuals import *
from subsystems.counter import Counter
from subsystems.point import *
from subsystems.bay import *

class Interface:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.prevmx = 0
        self.prevmy = 0
        self.mPressed = False
        self.mRising = False
        self.fps = 0
        self.ticks = 0
        self.c = Counter()
        '''Interactable Visual Objects'''
        '''
        Code:
        a - example A
        b - example B
        '''
        self.ivos = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes
            -997 : [" ", DummyVisualObject("dummy", (0,0))], # used by keybinds
            -996 : [" ", DummyVisualObject("dummy", (0,0))], # used by scrolling

        }
        '''Control'''
        self.interacting = -999
        self.previousInteracting = -999
        self.stringKeyQueue = ""
        self.previousKeyQueue = []
        self.mouseScroll = 0 
        self.consoleAlerts = []
        self.keybindLastUpdate = time.time()
        '''Sliders'''
        self.sliders = []
        self.slidersData = []
        pass

    def mouseInSection(self, section):
        return SECTIONS_DATA[section][0][0] <= self.mx and self.mx <= SECTIONS_DATA[section][1][0] and SECTIONS_DATA[section][0][1] <= self.my and self.my <= SECTIONS_DATA[section][1][1]

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.prevmx = self.mx
        self.prevmy = self.my
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        self.fps = fps
        self.deltaTicks = 1 if self.fps==0 else round(INTERFACE_FPS/self.fps)
        self.ticks += self.deltaTicks
        
        self.mouseInCalanderSection = self.mouseInSection("c")
        self.mouseInPopupSection    = self.mouseInSection("p")
        self.mouseInReminderSection = self.mouseInSection("r")
        self.mouseInDateSection     = self.mouseInSection("d")
        self.mouseInTimerSection    = self.mouseInSection("t")

        '''Keyboard'''
        for key in keyQueue: 
            if not key in self.previousKeyQueue:
                if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                    self.stringKeyQueue+=key
                else:
                    if key=="space":
                        self.stringKeyQueue+=" "
                    if key=="BackSpace":
                        if len(self.stringKeyQueue) > 0:
                            self.stringKeyQueue=self.stringKeyQueue[0:-1]
                    if key=="Return" or key=="Control_L":
                        self.interacting = -998
                        break
        self.previousKeyQueue = keyQueue.copy()
        if (self.interacting == -999 or self.interacting == -997) and (time.time() - self.keybindLastUpdate > 0.2):
            if KB_EXAMPLE(keyQueue):
                '''EXAMPLE KEYBIND: CTRL + SPACE'''
                print("example keybind")

        '''Mouse Scroll'''
        self.mouseScroll = mouseScroll
        if abs(self.mouseScroll) > 0:
            if self.interacting == -999: self.interacting = -996
            if self.interacting == -996:
                print("scrolling!")
        else:
            if self.interacting == -996: self.interacting = -999
        pass

        '''Interacting With...'''
        self.previousInteracting = self.interacting
        if not(self.mPressed):
            self.interacting = -999
        if self.interacting == -999 and self.mPressed and self.mRising:
            processed = False
            for id in self.ivos:
                for section in SECTIONS:
                    if self.ivos[id][0] == section:
                        if self.ivos[id][1].getInteractable(self.mx - SECTIONS_DATA[section][0][0], self.my - SECTIONS_DATA[section][0][1]):
                            self.interacting = id
                            processed = True
                            break
                if processed: break
        if self.interacting != -999:
            section = self.ivos[self.interacting][0]
            self.ivos[self.interacting][1].updatePos(self.mx - SECTIONS_DATA[section][0][0], self.my - SECTIONS_DATA[section][0][1])
            self.ivos[self.interacting][1].keepInFrame(SECTIONS_DATA[section][3][0],SECTIONS_DATA[section][3][1],SECTIONS_DATA[section][4][0],SECTIONS_DATA[section][4][1])
        if (self.mPressed) and (self.previousInteracting == -999) and (self.interacting != -999) and (self.ivos[self.interacting][1].type  == "textbox"): 
            self.stringKeyQueue = self.ivos[self.interacting][1].txt
        if (self.interacting != -999) and (self.ivos[self.interacting][1].type  == "textbox"):
            self.ivos[self.interacting][1].updateText(self.stringKeyQueue)
        if (self.previousInteracting != -999) and (self.previousInteracting != -998):
            if (self.ivos[self.previousInteracting][1].type  == "textbox"):
                if not(self.interacting == -998):
                    self.interacting = self.previousInteracting
                    self.ivos[self.interacting][1].updateText(self.stringKeyQueue)
                else:
                    self.ivos[self.previousInteracting][1].updateText(self.stringKeyQueue)

    def processCalander(self, im):
        '''Calander Area: `(  14,  14) to ( 463, 683)` : size `( 450, 670)`'''
        img = im.copy()
        rmx = self.mx - 14
        rmy = self.my - 14

        for id in self.ivos:
            if self.ivos[id][0] == "c":
                self.ivos[id][1].tick(img, self.interacting==id)

        return img    
    
    def processPopup(self, im):
        '''Popup Area:    `( 240,  14) to ( 463, 213)` : size `( 224, 200)`'''
        img = im.copy()
        rmx = self.mx - 240
        rmy = self.my - 14


        for id in self.ivos:
            if self.ivos[id][0] == "p":
                self.ivos[id][1].tick(img, self.interacting==id)

        return img    

    def processReminder(self, im):
        '''Reminder Area: `( 478,  14) to ( 927, 683)` : size `( 450, 670)`'''
        img = im.copy()
        rmx = self.mx - 478
        rmy = self.my - 14

        for id in self.ivos:
            if self.ivos[id][0] == "r":
                self.ivos[id][1].tick(img, self.interacting==id)

        return img    

    def processDate(self, im):
        '''Date Area:     `( 942,  14) to (1351, 341)` : size `( 410, 328)`'''
        img = im.copy()
        rmx = self.mx - 942
        rmy = self.my - 14

        temp = FORMATING_NOW("%m-%Y")
        placeOver(img, displayText(f"{temp}", "m"), (20,25))


        delta = -(7+int(FORMATING_NOW("%d"))-((int(FORMATING_NOW("%d"))-["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(FORMATING_NOW("%A"))))%7)*86400
        days = [FORMATING_DELTA("%d", delta+i*86400) for i in range(35)]
        months = [FORMATING_DELTA("%m", delta+i*86400) for i in range(35)]
        currentMonth = FORMATING_NOW("%m")
        currentDay = FORMATING_NOW("%d")

        for i in range(7):
            placeOver(img, displayText("SMTWTFS"[i], "m"), (i*55+25, 75))

        for i in range(35):
            placeOver(img, displayText(str(days[i]), "m", colorTXT=((255,255,255,255) if days[i] == currentDay else (175,175,175,255)) if months[i] == currentMonth else (100,100,100,255)), (i%7*55+25, i//7*40+115))

        for id in self.ivos:
            if self.ivos[id][0] == "d":
                self.ivos[id][1].tick(img, self.interacting==id)

        return img    

    def processTimer(self, im):
        '''Timer Area:    `( 942, 356) to (1351, 683)` : size `( 410, 328)`'''
        img = im.copy()
        rmx = self.mx - 942
        rmy = self.my - 356

        placeOver(img, displayText(f"FPS: {self.fps}", "m"), (20,20))
        placeOver(img, displayText(f"Interacting With: {self.interacting}", "m"), (20,55))
        placeOver(img, displayText(f"length of IVO: {len(self.ivos)}", "m"), (20,90))
        placeOver(img, displayText(f"Mouse Pos: ({self.mx}, {self.my})", "m"), (200,20))
        placeOver(img, displayText(f"Mouse Press: {self.mPressed}", "m", colorTXT=(100,255,100,255) if self.mPressed else (255,100,100,255)), (200,55))

        for id in self.ivos:
            if self.ivos[id][0] == "t":
                self.ivos[id][1].tick(img, self.interacting==id)

        return img    

    def saveState(self):
        pass

    def close(self):
        pass

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
        self.temporaryInteracting = -999
        self.stringKeyQueue = ""
        self.previousKeyQueue = []
        self.mouseScroll = 0 
        self.consoleAlerts = []
        self.keybindLastUpdate = time.time()
        '''Sliders'''
        self.sliders = []
        self.slidersData = []
        '''Visuals'''
        self.reminderScrollOffset = 0
        self.reminderTabScrollOffset = 0
        '''Data'''
        self.now = time.time()
        self.reminders = {
            "Reminders": [["hmmmmm",65465465, False],["aaaaa",17179869184, False]],
            "test test": [["yippee",84546512, False],["huh  ",646546545, False]]
        }
        self.selectedRemindersList = list(self.reminders.keys())[0]
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

        self.now = time.time()
        
        self.mouseInCalanderSection = self.mouseInSection("c")
        self.mouseInPopupSection    = self.mouseInSection("p")
        self.mouseInReminderSection = self.mouseInSection("r")
        self.mouseInDateSection     = self.mouseInSection("d")
        self.mouseInTimerSection    = self.mouseInSection("t")

        '''Temporary Interacting'''
        if not(self.temporaryInteracting in self.ivos):
            self.temporaryInteracting = -999
        else:
            if self.temporaryInteracting in self.ivos and self.interacting != self.temporaryInteracting:
                if self.ivos[self.temporaryInteracting][1].name[0] == "A":
                    self.reminders[self.selectedRemindersList][int(self.ivos[self.temporaryInteracting][1].name[1:])][0] = self.ivos[self.temporaryInteracting][1].txt
                if self.ivos[self.temporaryInteracting][1].name[0] == "B":
                    timestamp = self.ivos[self.temporaryInteracting][1].txt
                    try:
                        offset = 0
                        for test in ["am", "AM", "aM", "Am", "pm", "PM", "pM", "Pm"]:
                            if test in timestamp: break
                        if test in ["am", "AM", "aM", "Am"]: offset = 0
                        if test in ["pm", "PM", "pM", "Pm"]: offset = 43200
                        timestamp += " "
                        for char in timestamp:
                            if not(str(char) in "0123456789"): timestamp = timestamp.replace(str(char), " ")
                        while "  " in timestamp: timestamp = timestamp.replace("  ", " ")
                        try: self.reminders[self.selectedRemindersList][int(self.ivos[self.temporaryInteracting][1].name[1:])][1] = (int(round(time.mktime(time.strptime(timestamp, "%m %d %Y %I %M %S ")))+offset))
                        except: self.reminders[self.selectedRemindersList][int(self.ivos[self.temporaryInteracting][1].name[1:])][1] = (int(round(time.mktime(time.strptime(timestamp, "%m %d %Y %I %M ")))+offset))
                    except:
                        pass
                if self.ivos[self.temporaryInteracting][1].name[0] == "C":
                    editing = list(self.reminders.keys())[int(self.ivos[self.temporaryInteracting][1].name[1:])]
                    temp = self.reminders[editing]
                    self.reminders.pop(editing)
                    self.reminders[self.ivos[self.temporaryInteracting][1].txt] = temp
                    self.selectedRemindersList = self.ivos[self.temporaryInteracting][1].txt
                self.ivos.pop(self.temporaryInteracting)
                self.temporaryInteracting = -999  

        '''Keyboard'''
        for key in keyQueue:
            if not key in self.previousKeyQueue:
                if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                    self.stringKeyQueue+=key
                else:
                    if key=="space":    self.stringKeyQueue+=" "
                    if key=="slash":    self.stringKeyQueue+="/"
                    if key=="asterisk": self.stringKeyQueue+="*"
                    if key=="equal":    self.stringKeyQueue+="="
                    if key=="at":       self.stringKeyQueue+="@"
                    if key=="minus":    self.stringKeyQueue+="-"
                    if key=="colon":    self.stringKeyQueue+=":"
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
                '''Scrolling!'''
                if self.mouseInReminderSection:
                    rmx = self.mx - 478
                    rmy = self.my - 14
                    if 58 < rmy and rmy < 640:
                        self.reminderScrollOffset += self.mouseScroll/2
                        self.reminderScrollOffset = max(0, min(self.reminderScrollOffset, (len(self.reminders[self.selectedRemindersList])-1)*73))
                    elif 640 <= rmy:
                        self.reminderTabScrollOffset += self.mouseScroll/2
                        self.reminderTabScrollOffset = max(0, min(self.reminderTabScrollOffset, (len(self.reminders.keys())-1)*100))
        else:
            if self.interacting == -996: self.interacting = -999
        pass

        '''Mouse Pressed Activations'''
        if self.mouseInReminderSection and self.mRising and self.interacting == -999:
            rmx = self.mx - 478
            rmy = self.my - 14
            if 58 <= rmy and rmy <= 640:
                if rmx > 60:
                    if 58 < rmy and rmy < len(self.reminders[self.selectedRemindersList])*73+80-self.reminderScrollOffset and rmy < 640:
                        i = (rmy+self.reminderScrollOffset-80)//73
                        self.interacting = self.c.c()
                        self.temporaryInteracting = self.interacting
                        if (rmy - ((rmy+self.reminderScrollOffset-80)//73+1)*73) <= 22:
                            self.stringKeyQueue = self.reminders[self.selectedRemindersList][i][0]
                            self.ivos[self.interacting] = ["r", EditableTextBoxVisualObject(f"A{i}", (60, i*73+80-self.reminderScrollOffset), self.stringKeyQueue)]
                        else:
                            self.stringKeyQueue = FORMAT_TIME_FANCY(self.reminders[self.selectedRemindersList][i][1])
                            self.ivos[self.interacting] = ["r", EditableTextBoxVisualObject(f"B{i}", (60, i*73+102-self.reminderScrollOffset), self.stringKeyQueue)]
                    elif len(self.reminders[self.selectedRemindersList])*73+80-self.reminderScrollOffset < rmy and rmy < 640:
                        self.reminders[self.selectedRemindersList].append(["New Reminder", (time.time()//86400)*86400 + 86400, False])
                    elif rmy <= 58 or 640 <= rmy:
                        pass
                else:
                    i = (rmy+self.reminderScrollOffset-80)//73
                    if 0 <= i and i <= len(self.reminders[self.selectedRemindersList])-1:
                        self.reminders[self.selectedRemindersList][i][2] = not(self.reminders[self.selectedRemindersList][i][2])
                        self.interacting = -997
            elif 640 < rmy:
                i = (rmx+self.reminderTabScrollOffset-10)//100
                if 0 <= i and i <= len(self.reminders.keys())-1 and list(self.reminders.keys())[i] != self.selectedRemindersList:
                    self.selectedRemindersList = list(self.reminders.keys())[i]
                    self.interacting = -997
                if list(self.reminders.keys())[i] == self.selectedRemindersList:
                    self.interacting = self.c.c()
                    self.temporaryInteracting = self.interacting
                    self.stringKeyQueue = self.selectedRemindersList
                    self.ivos[self.interacting] = ["r", EditableTextBoxVisualObject(f"C{i}", (i*100+10-self.reminderTabScrollOffset, 645), self.stringKeyQueue)]


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

        selectedList = self.reminders[self.selectedRemindersList]

        i=0
        for reminder in selectedList:
            if i*73+60-self.reminderScrollOffset > 640:
                break
            if i*73+60-self.reminderScrollOffset > 0:
                if not(self.ivos[self.temporaryInteracting][1].name[0] == "A" and str(i) == str(self.ivos[self.temporaryInteracting][1].name[1:])):
                    placeOver(img, displayText(reminder[0], "m", colorTXT=(175,175,175,255) if reminder[2] else (0,0,0,255)), (60, i*73+80-self.reminderScrollOffset))
                if not(self.ivos[self.temporaryInteracting][1].name[0] == "B" and str(i) == str(self.ivos[self.temporaryInteracting][1].name[1:])):
                    placeOver(img, displayText(FORMAT_TIME_FANCY(reminder[1]), "m", colorTXT=(175,175,175,255) if reminder[2] else ((150,150,150,255) if reminder[1] >= self.now else (255,100,100,255))), (60, i*73+102-self.reminderScrollOffset))
                if reminder[1] >= self.now and not(reminder[2]):
                    placeOver(img,CHECKLIST_NORMAL_ARRAY, (30, i*73+102-self.reminderScrollOffset), True)
                elif reminder[1] <= self.now and not(reminder[2]):
                    placeOver(img,CHECKLIST_LATE_ARRAY, (30, i*73+102-self.reminderScrollOffset), True)
                elif reminder[2]:
                    placeOver(img,CHECKLIST_COMPLETE_ARRAY, (30, i*73+102-self.reminderScrollOffset), True)
                else:
                    pass
            i+=1

        placeOver(img, generateColorBox((444,55), FILL_COLOR_RGBA), (3,3))
        placeOver(img, generateColorBox((300,2), FRAME_COLOR_RGBA), (76,56))
        placeOver(img, displayText(f"Reminders > {self.selectedRemindersList}: {len(selectedList)}", "m"), (20,20))


        placeOver(img, generateColorBox((444,25), FILL_COLOR_RGBA), (3,642))
        placeOver(img, generateColorBox((300,2), FRAME_COLOR_RGBA), (76,640))
        i=0
        for listname in list(self.reminders.keys()):
            shift = i*100+10-self.reminderTabScrollOffset
            if shift > 450:
                break
            if not(self.ivos[self.temporaryInteracting][1].name[0] == "C" and str(i) == str(self.ivos[self.temporaryInteracting][1].name[1:])):
                if shift > -90:
                    if shift < 0:
                        placeOver(img, getRegion(displayText(listname, "m"), (abs(shift)+3,0), (90,25)), (3,645))
                    elif shift > 360:
                        placeOver(img, getRegion(displayText(listname, "m"), (0,0), (90-(shift-360+4),25)), (shift,645))
                    else:
                        placeOver(img, getRegion(displayText(listname, "m"), (0,0), (90,25)), (shift,645))
            i+=1

        for id in self.ivos:
            if self.ivos[id][0] == "r":
                self.ivos[id][1].tick(img, self.interacting==id)

        return img    

    def processDate(self, im):
        '''Date Area:     `( 942,  14) to (1351, 341)` : size `( 410, 328)`'''
        img = im.copy()
        rmx = self.mx - 942
        rmy = self.my - 14

        temp = FORMAT_NOW("%m-%Y")
        placeOver(img, displayText(f"{temp}", "m"), (20,25))


        delta = -(7+int(FORMAT_NOW("%d"))-((int(FORMAT_NOW("%d"))-["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(FORMAT_NOW("%A"))))%7)*86400
        days = [FORMAT_DELTA("%d", delta+i*86400) for i in range(35)]
        months = [FORMAT_DELTA("%m", delta+i*86400) for i in range(35)]
        currentMonth = FORMAT_NOW("%m")
        currentDay = FORMAT_NOW("%d")

        for i in range(7):
            placeOver(img, displayText("SMTWTFS"[i], "m"), (i*55+25, 75))

        for i in range(35):
            placeOver(img, displayText(str(days[i]), "m", colorTXT=((0,0,0,255) if days[i] == currentDay else (150,150,150,255)) if months[i] == currentMonth else (200,200,200,255)), (i%7*55+25, i//7*40+115))

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
        placeOver(img, displayText(f"Temp Interacting: {self.temporaryInteracting}", "m"), (200,90))

        for id in self.ivos:
            if self.ivos[id][0] == "t":
                self.ivos[id][1].tick(img, self.interacting==id)

        return img    

    def saveState(self):
        pass

    def close(self):
        pass

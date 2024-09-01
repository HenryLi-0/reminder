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

            -99 : ["p", EditableTextBoxVisualObject( "Name", (10,10), "")],
            -98 : ["p", EditableTextBoxVisualObject("Start", (10,50), "")],
            -97 : ["p", EditableTextBoxVisualObject(  "End", (10,90), "")],
            -96 : ["p", TextButtonPushVisualObject( "Save", "Save", (10,150), 3)],
            -95 : ["p", TextButtonPushVisualObject("Cancel", "Cancel", (150,150), 3)],
            -94 : ["p", DummyVisualObject("editing", (0,0))],
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
        self.updateSection = []
        '''Sliders'''
        self.sliders = []
        self.slidersData = []
        '''Visuals'''
        self.reminderScrollOffset = 0
        self.reminderTabScrollOffset = 0
        self.calendarOffset = 0
        self.calendarScale = 1
        temp = time.localtime(time.time())
        self.selectedCalendarIndex = temp.tm_mday + (8-temp.tm_wday)
        self.selectedCalendarDate = (time.mktime(temp) - time.mktime(time.gmtime(0)))//(86400)
        self.editingEvent = False
        '''Data'''
        self.now = time.time()
        self.reminders = {
            "Reminders": [["hmmmmm",65465465, False],["aaaaa",17179869184, False]],
            "test test": [["yippee",84546512, False],["huh  ",646546545, False]]
        }
        self.selectedRemindersList = list(self.reminders.keys())[0]
        self.calendar = [
            ["test event", 1725075043, 1725082243, generatePastelLight()]
        ]
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
                if not self.temporaryInteracting in SYS_IVOS:
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
            if KB_DEL_REMINDER(keyQueue):
                '''DELETE REMINDER BELOW MOUSE: SHIFT + BACKSPACE'''
                if self.mouseInReminderSection and 55 < (self.my-14) and (self.my-14) < 640:
                    if len(self.reminders[self.selectedRemindersList]) > 1:
                        i = ((self.my-14)+self.reminderScrollOffset-80)//73
                        if 0 <= i and i <= len(self.reminders[self.selectedRemindersList])-1:
                            self.keybindLastUpdate = time.time()
                            self.reminders[self.selectedRemindersList].pop(i)
                            self.interacting = -997
            if KB_DEL_LIST(keyQueue):
                '''DELETE CURRENT REMINDERS LIST: ALT + SHIFT + BACKSPACE'''
                if self.mouseInReminderSection and 640 < (self.my-14):
                    if len(self.reminders.keys()) > 1:
                        i = ((self.mx-478)+self.reminderTabScrollOffset-10)//100
                        if 0 <= i and i <= len(self.reminders.keys())-1:
                            self.keybindLastUpdate = time.time()
                            self.reminders.pop(list(self.reminders.keys())[i])
                            self.selectedRemindersList = list(self.reminders.keys())[i-1]
                            self.interacting = -997
            if KB_NEW_REMINDER(keyQueue):
                '''CREATES A NEW REMINDER: ALT + N'''
                if self.mouseInReminderSection and 55 < (self.my-14) and (self.my-14) < 640:
                    self.keybindLastUpdate = time.time()
                    self.reminders[self.selectedRemindersList].append(["New Reminder", (time.time()//86400)*86400 + 86400, False])
                    self.interacting = -997
            if KB_NEW_LIST(keyQueue):
                '''CREATES A NEW LIST: ALT + N'''
                if 640 <= (self.my-14):
                    self.keybindLastUpdate = time.time()
                    self.reminders[f"New List {len(self.reminders.keys())}"] = [["New Reminder", (time.time()//86400)*86400 + 86400, False]]
                    self.interacting = -997
            if KB_ZOOM_IN(keyQueue):
                '''ZOOM IN (CALENDAR): ALT + PLUS'''
                self.keybindLastUpdate = time.time()
                calendarScalePrevious = self.calendarScale
                self.calendarScale = 10**(math.log(self.calendarScale+0.000001,10) - 500/2500)-0.000001
                self.calendarScale = max(0.25, min(self.calendarScale, 1))
                self.calendarOffset -= (self.calendarScale-calendarScalePrevious)*(self.my-50)/25
                self.interacting = -997
            if KB_ZOOM_OUT(keyQueue):
                '''ZOOM OUT (CALENDAR): ALT + MINUS'''
                self.keybindLastUpdate = time.time()
                calendarScalePrevious = self.calendarScale
                self.calendarScale = 10**(math.log(self.calendarScale+0.000001,10) + 500/2500)-0.000001
                self.calendarScale = max(0.25, min(self.calendarScale, 1))
                self.calendarOffset -= (self.calendarScale-calendarScalePrevious)*(self.my-50)/25
                self.interacting = -997


        '''Mouse Scroll'''
        self.mouseScroll = mouseScroll
        if abs(self.mouseScroll) > 0:
            if self.interacting == -999: self.interacting = -996
            if self.interacting == -996:
                '''Scrolling!'''
                if self.mouseInReminderSection:
                    self.scheduleSection("r")
                    rmx = self.mx - 478
                    rmy = self.my - 14
                    if 58 < rmy and rmy < 640:
                        self.reminderScrollOffset += self.mouseScroll/2
                        self.reminderScrollOffset = max(0, min(self.reminderScrollOffset, (len(self.reminders[self.selectedRemindersList])-1)*73))
                    elif 640 <= rmy:
                        self.reminderTabScrollOffset += self.mouseScroll/2
                        self.reminderTabScrollOffset = max(0, min(self.reminderTabScrollOffset, (len(self.reminders.keys())-1)*100))
                if self.mouseInCalanderSection:
                    rmx = self.mx - 14
                    rmy = self.my - 14
                    self.calendarOffset += self.mouseScroll/100
        else:
            if self.interacting == -996: self.interacting = -999
        pass

        self.calendarOffset = max(-0.25, min(self.calendarOffset,-((670-50)*(self.calendarScale+0.000001)/25-25)))

        '''Mouse Pressed Activations'''
        if self.mouseInReminderSection and self.mRising and self.interacting == -999:
            self.scheduleSection("r")
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
                if 0 <= i and i <= len(self.reminders.keys())-1:
                    if list(self.reminders.keys())[i] != self.selectedRemindersList:
                        self.selectedRemindersList = list(self.reminders.keys())[i]
                        self.interacting = -997
                    elif list(self.reminders.keys())[i] == self.selectedRemindersList:
                        self.interacting = self.c.c()
                        self.temporaryInteracting = self.interacting
                        self.stringKeyQueue = self.selectedRemindersList
                        self.ivos[self.interacting] = ["r", EditableTextBoxVisualObject(f"C{i}", (i*100+10-self.reminderTabScrollOffset, 645), self.stringKeyQueue)]
                elif len(self.reminders.keys())-1 < i:
                    self.reminders[f"New List {len(self.reminders.keys())}"] = [["New Reminder", (time.time()//86400)*86400 + 86400, False]]
        if self.mouseInDateSection and self.mRising and self.interacting == -999:
            i = ((self.my-99)//35)*7+(self.mx-940)//55
            if 0 <= i and i <= 41:
                self.selectedCalendarIndex = i
                now = time.localtime()
                yearNow = now.tm_year
                monthNow = now.tm_mon
                firstDayInMonth = time.mktime((yearNow, monthNow, 1, 0, 0, 0, 0, 0, -1))
                monthDay = 1 + (7*(i//7)) + (i%7-time.localtime(firstDayInMonth).tm_wday)
                if monthDay < 1: monthDay += 7
                date = (yearNow, monthNow, monthDay, 0, 0, 0, 0, 0, -1)
                epochSeconds = time.mktime(date)
                daysSinceEpoch = epochSeconds // (24 * 3600) - 1
                self.selectedCalendarDate = daysSinceEpoch
                self.scheduleSection("d")
        if self.mouseInCalanderSection and self.mRising and self.interacting == -999:
            if not(self.editingEvent):
                temp = ((self.my-14-50)*(self.calendarScale)/25+self.calendarOffset-TIMEZONE_OFFSET)*3600+self.selectedCalendarDate*86400
                action = ""
                for i in range(len(self.calendar)):
                    if self.calendar[i][1] <= temp and temp <= self.calendar[i][2]:
                        action = i
                        break
                if action != "":
                    self.editingEvent = True
                    self.ivos[-99][1].updateText(self.calendar[i][0])
                    self.ivos[-98][1].updateText(FORMAT_TIME_FANCY(self.calendar[i][1]))
                    self.ivos[-97][1].updateText(FORMAT_TIME_FANCY(self.calendar[i][2]))
                    self.ivos[-94][1].data = i
                if action == "":
                    temp = round(temp/900)*900
                    self.calendar.append(["New Event", temp, temp+3600, generatePastelLight()])

        '''Editing Events'''
        if self.interacting == -96:
            i = int(self.ivos[-94][1].data)
            result = []
            for timestamp in [self.ivos[-98][1].txt, self.ivos[-97][1].txt]:
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
                    try:
                        result.append(int(round(time.mktime(time.strptime(timestamp, "%m %d %Y %I %M %S ")))+offset))
                    except:
                        result.append(int(round(time.mktime(time.strptime(timestamp, "%m %d %Y %I %M ")))+offset))
                except:
                    pass
            if len(result) == 2:
                if result[0] != result[1]:
                    self.calendar[i][0] = self.ivos[-99][1].txt
                    self.calendar[i][1] = min(result[0], result[1])
                    self.calendar[i][2] = max(result[0], result[1])

            self.editingEvent = False
        if self.interacting == -95:
            self.editingEvent = False


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

        if self.temporaryInteracting != -999:
            self.scheduleSection(self.ivos[self.temporaryInteracting][0])
        self.scheduleSection("c")
        self.scheduleSection("p")
        self.scheduleSection("t")

    def processCalander(self, im):
        '''Calander Area: `(  14,  14) to ( 463, 683)` : size `( 450, 670)`'''
        img = im.copy()
        rmx = self.mx - 14
        rmy = self.my - 14

        for i in range(25):
            y = (i-self.calendarOffset)*25/(self.calendarScale+0.000001) + 50
            if (i//12) % 2 == 0: placeOver(img, displayText(f"{12 if i%12 == 0 else i%12} AM", "s"), (20,y), True)
            else: placeOver(img, displayText(f"{12 if i%12 == 0 else i%12} PM", "s"), (20,y), True)
            placeOver(img, CALANDER_BAR, (37, y))

        for event in self.calendar:
            temp = time.mktime(time.localtime(event[1]))
            temp = (temp - self.selectedCalendarDate*86400)/3600 + TIMEZONE_OFFSET
            y1 = (temp-self.calendarOffset)*25/(self.calendarScale+0.000001) + 50
            temp = time.mktime(time.localtime(event[2]))
            temp = (temp - self.selectedCalendarDate*86400)/3600 + TIMEZONE_OFFSET
            y2 = (temp-self.calendarOffset)*25/(self.calendarScale+0.000001) + 50
            if (y1 <= 683) or (50 <= y2):
                if y1 < 50:
                    if y2 > 683:
                        # Larger than the calendar screen on both ends
                        temp = generateColorBox((400, 633), event[3])
                        placeOver(temp, displayText(event[0], "m"), (5,5))
                        placeOver(temp, displayText(FORMAT_TIME_FANCY(event[1]), "sm"), (5,25))
                        placeOver(temp, displayText(FORMAT_TIME_FANCY(event[2]), "sm"), (200,25))
                        placeOver(img, temp, (37, 50))
                    else:
                        # Top peeks above screen
                        temp = generateColorBox((400, round(y2-50)), event[3])
                        if abs(y2-50) > 20:
                            placeOver(temp, displayText(event[0], "m"), (5,5))
                        if abs(y2-50) > 38:
                            placeOver(temp, displayText(FORMAT_TIME_FANCY(event[1]), "sm"), (5,25))
                            placeOver(temp, displayText(FORMAT_TIME_FANCY(event[2]), "sm"), (200,25))
                        placeOver(img, temp, (37, 55))
                else:
                    if y2 > 683:
                        # Bottom peeks below screen
                        temp = generateColorBox((400, round(683-y1)), event[3])
                        if abs(683-y1) > 20:
                            placeOver(temp, displayText(event[0], "m"), (5,5))
                        if abs(683-y1) > 38:
                            placeOver(temp, displayText(FORMAT_TIME_FANCY(event[1]), "sm"), (5,25))
                            placeOver(temp, displayText(FORMAT_TIME_FANCY(event[2]), "sm"), (200,25))
                        placeOver(img, temp, (37, y1))
                    else:
                        # Smaller than the calendar screen
                        temp = generateColorBox((400, round(y2-y1)), event[3])
                        if abs(y2-y1) > 20:
                            placeOver(temp, displayText(event[0], "m"), (5,5))
                        if abs(y2-y1) > 38:
                            placeOver(temp, displayText(FORMAT_TIME_FANCY(event[1]), "sm"), (5,25))
                            placeOver(temp, displayText(FORMAT_TIME_FANCY(event[2]), "sm"), (200,25))
                        placeOver(img, temp, (37, min(y1,y2)))

        placeOver(img, generateColorBox((444,50), FILL_COLOR_RGBA), (3,3))
        placeOver(img, generateColorBox((300,2), FRAME_COLOR_RGBA), (76,51))
        placeOver(img, displayText(f"Calendar", "m"), (20,20))


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
                        placeOver(img, getRegion(displayText(listname, "m", colorTXT=(0,0,0,255) if listname == self.selectedRemindersList else (100,100,100,255)), (abs(shift)+3,0), (90,25)), (3,645))
                    elif shift > 360:
                        placeOver(img, getRegion(displayText(listname, "m", colorTXT=(0,0,0,255) if listname == self.selectedRemindersList else (100,100,100,255)), (0,0), (90-(shift-360+4),25)), (shift,645))
                    else:
                        placeOver(img, getRegion(displayText(listname, "m", colorTXT=(0,0,0,255) if listname == self.selectedRemindersList else (100,100,100,255)), (0,0), (90,25)), (shift,645))
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
        days = [FORMAT_DELTA("%d", delta+i*86400) for i in range(42)]
        months = [FORMAT_DELTA("%m", delta+i*86400) for i in range(42)]
        currentMonth = FORMAT_NOW("%m")
        currentDay = FORMAT_NOW("%d")

        for i in range(7):
            placeOver(img, displayText("SMTWTFS"[i], "m"), (i*55+25, 75))

        for i in range(42):
            placeOver(img, displayText(str(days[i]), "m", (200,200,255,255) if i == self.selectedCalendarIndex else (0,0,0,0), ((0,0,0,255) if days[i] == currentDay else (150,150,150,255)) if months[i] == currentMonth else (200,200,200,255)), (i%7*55+25, i//7*35+105))

        for id in self.ivos:
            if self.ivos[id][0] == "d":
                self.ivos[id][1].tick(img, self.interacting==id)

        return img    

    def processTimer(self, im):
        '''Timer Area:    `( 942, 356) to (1351, 683)` : size `( 410, 328)`'''
        img = im.copy()
        rmx = self.mx - 942
        rmy = self.my - 356

        # placeOver(img, displayText(f"FPS: {self.fps}", "m"), (20,20))
        # placeOver(img, displayText(f"Interacting With: {self.interacting}", "m"), (20,55))
        # placeOver(img, displayText(f"length of IVO: {len(self.ivos)}", "m"), (20,90))
        # placeOver(img, displayText(f"Mouse Pos: ({self.mx}, {self.my})", "m"), (200,20))
        # placeOver(img, displayText(f"Mouse Press: {self.mPressed}", "m", colorTXT=(100,255,100,255) if self.mPressed else (255,100,100,255)), (200,55))
        # placeOver(img, displayText(f"Temp Interacting: {self.temporaryInteracting}", "m"), (200,90))

        placeOver(img, displayText(FORMAT_NOW("%m-%d-%Y"), "l"), (205,40), True)
        placeOver(img, displayText(FORMAT_NOW("%I:%M:%S %p"), "l"), (205,75), True)

        action = ""
        for i in range(len(self.calendar)):
            if (self.calendar[i][1] <= self.now) and (self.now <= self.calendar[i][2]):
                action = i
                break

        if action != "":
            passed = (self.now - self.calendar[action][1])/(self.calendar[action][2]-self.calendar[action][1])
            placeOver(img, displayText(f"Current Event: {self.calendar[action][0]}", "m"), (205,260), True)
            placeOver(img, generateColorBox((round(300*passed),30), (175,175,175,255)), (55,270))
            placeOver(img, generateColorBox((round(300*(1-passed)),30), (255,100,100,255)), (55 + round(300*passed),270))
            temp = math.ceil(self.calendar[action][2] - self.now)
            placeOver(img, displayText(f"{FORMAT_TIME_DIFF(temp)}", "m"), (205,285), True)
        else:
            action = ""
            for i in range(len(self.calendar)):
                action = i + 1
                if (self.calendar[i][1] < self.now):
                    break
            if not(0 <= action and action <= len(self.calendar)-1) or (self.calendar[action][1] < self.now):
                action = ""
            placeOver(img, generateColorBox((300, 30), (175,175,175,255)), (55, 270))
            if action != "":
                placeOver(img, displayText(f"Next Event: {self.calendar[action][0]}", "m"), (205,260), True)
                temp = math.ceil(self.calendar[action][1] - self.now)
                placeOver(img, displayText(f"{FORMAT_TIME_DIFF(temp)}", "m"), (205,285), True)
            else:
                placeOver(img, displayText("No Future Events!", "m"), (205,260), True)

        placeOver(img, CLOCK, (205,167), True)

        for id in self.ivos:
            if self.ivos[id][0] == "t":
                self.ivos[id][1].tick(img, self.interacting==id)

        return img    


    def scheduleSection(self, section):
        if not(section in self.updateSection):
            self.updateSection.append(section)

    def saveState(self):
        pass

    def close(self):
        pass

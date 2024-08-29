'''This file is just the window that pops up and refreshes itself!'''

from settings import *
import tkinter as tk
from PIL import ImageTk, Image
import time, math
from subsystems.interface import Interface
from subsystems.label import LabelWrapper
from subsystems.render import arrayToImage
from settings import *

class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window = tk.Tk()
        self.window.grid()
        self.window.title("Reminders")
        self.window.geometry("1366x698")
        # self.window.minsize(500,500)
        # self.window.maxsize(500,500)
        self.window.configure(background=BACKGROUND_COLOR)
        self.fps = 0
        self.fpsTimestamps = []
        self.mPressed = False
        self.keysPressed = []
        self.mouseScroll = 0

        '''load test image'''
        testImage = ImageTk.PhotoImage(PLACEHOLDER_IMAGE)
        self.labels = {}
        self.blankLabels = {}
        for section in SECTIONS:
            self.labels[section] = LabelWrapper(self.window, SECTIONS_DATA[section][2], SECTIONS_DATA[section][0], SECTIONS_DATA[section][0], FILL_COLOR, SECTIONS_FRAME_INSTRUCTIONS[section])
            self.blankLabels[section] = self.labels[section].getBlank() 

        '''start interface'''
        self.interface = Interface()

        self.processFunctions = {
            "c" : self.interface.processCalander,
            "p" : self.interface.processPopup   ,
            "r" : self.interface.processReminder,
            # "d" : self.interface.processDate    ,
            "t" : self.interface.processTimer   ,
        }
        self.processFunctionsRegions = list(self.processFunctions.keys())

    def windowProcesses(self):
        '''window processes'''
        mx = self.window.winfo_pointerx()-self.window.winfo_rootx()
        my = self.window.winfo_pointery()-self.window.winfo_rooty()
        if self.mPressed > 0: self.mPressed += 1
        else: self.mPressed = 0

        '''update screens'''
        self.interface.tick(mx,my,self.mPressed, self.fps, self.keysPressed, self.mouseScroll)
        self.mouseScroll = 0
        
        for region in self.processFunctionsRegions:
            if self.labels[region].shown:
                self.labels[region].update(arrayToImage(self.processFunctions[region](self.blankLabels[region])))

        now = time.time()
        self.fpsTimestamps.append(now)
        while now-self.fpsTimestamps[0] > 1:
            self.fpsTimestamps.pop(0)
        self.fps = len(self.fpsTimestamps)

        self.window.after(TICK_MS, self.windowProcesses)

    def windowOccasionalProcesses(self):
        '''window processes that happen less frequently (once every 5 seconds)'''
        print("windowOccaionalProcess")
        self.window.title(f"Reminders")
        print(self.getFPS())
        self.labels["d"].update(arrayToImage(self.interface.processDate(self.blankLabels["d"])))
        self.window.after(OCCASIONAL_TICK_MS, self.windowOccasionalProcesses)

    def windowStartupProcesses(self):
        '''window processes that occur once when startup'''
        print("windowStartupProcess")
        pass
    
    def getFPS(self): return self.fps
    def mPress(self, side = 0): self.mPressed = 1
    def mRelease(self, side = 0): self.mPressed = -999
    def mouseWheel(self, event): self.mouseScroll -= event.delta
    def keyPressed(self, key): 
        if (not str(key.keysym) in self.keysPressed) and (not str(key.keysym) in KB_IGNORE):
            self.keysPressed.append(str(key.keysym))
    def keyReleased(self, key):
        if str(key.keysym) in self.keysPressed:
            self.keysPressed.remove(str(key.keysym))
    
    def start(self):
        '''start window main loop'''
        print("windowStart")
        
        self.window.bind("<ButtonPress-1>", self.mPress)
        self.window.bind("<ButtonRelease-1>", self.mRelease)
        self.window.bind("<KeyPress>", self.keyPressed)
        self.window.bind("<KeyRelease>", self.keyReleased)
        self.window.bind_all("<MouseWheel>", self.mouseWheel)

        self.window.after(2, self.windowProcesses)
        self.window.after(2, self.windowOccasionalProcesses)
        self.window.after(1, self.windowStartupProcesses)
        self.window.mainloop()
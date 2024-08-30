'''
Settings

Here are the parts:
- Calculation
- Visuals
- Saving
- Keybinds
- Constants (Please do not change!)
'''

'''Calculation'''
FLOAT_ACCURACY = 3 # The number of digits after the decimal point things will generally round to


'''Visuals'''
INTERFACE_FPS = 60 # The desired operating FPS
TICK_MS = 1 # Extra delay between frames, must be 1 or greater
OCCASIONAL_TICK_MS = 5000 # Should keep above 1 second, as it runs processes that do not need updates every tick

SHOW_CROSSHAIR = False # Shows a crosshair for the mouse's position

hexColorToRGBA = lambda hexcolor: tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

BACKGROUND_COLOR = "#303030" #Background color
FRAME_COLOR      = "#9b9b9b" #Borders and Frame color
SELECTED_COLOR   = "#696969" #Selected Element color
FILL_COLOR       = "#eeeeee" #Fill color

BACKGROUND_COLOR_RGBA = hexColorToRGBA(BACKGROUND_COLOR)
FRAME_COLOR_RGBA      = hexColorToRGBA(FRAME_COLOR     )
SELECTED_COLOR_RGBA   = hexColorToRGBA(SELECTED_COLOR  )
FILL_COLOR_RGBA       = hexColorToRGBA(FILL_COLOR      )


'''Saving'''
import os, time
PATH_SAVE_DEFAULT = os.path.join("saves")

FORMAT_TIME = lambda x: time.strftime("%I:%M:%S %p %m/%d/%Y", time.localtime(x))
FORMAT_NOW = lambda f: time.strftime(f, time.localtime(time.time()))
FORMAT_DELTA = lambda f,t: time.strftime(f, time.localtime(time.time()+t))
FORMAT_TIME_FANCY = lambda x: time.strftime("%m-%d-%Y - %I:%M:%S %p", time.localtime(x))

'''Keybinds'''
KB_IGNORE       = ["Win_L"]                                                                                                 # Keys to ignore
KB_DEL_REMINDER = lambda keys: (len(keys) == 2) and ("Shift_L" in keys) and ("BackSpace" in keys)                           # Deletes the reminder
KB_DEL_LIST     = lambda keys: (len(keys) == 3) and (  "Alt_L" in keys) and ("Shift_L" in keys) and ("BackSpace" in keys)   # Deletes the entire list
KB_NEW_REMINDER = lambda keys: (len(keys) == 2) and (  "Alt_L" in keys) and ("N" in keys or "n" in keys)                    # Creates a new reminder
KB_NEW_LIST     = lambda keys: (len(keys) == 2) and (  "Alt_L" in keys) and ("N" in keys or "n" in keys)                    # Creates a new list


'''Constants - DO NOT CHANGE!!!'''
'''Do not change these constants. Some are probably important. Some are used for testing purposes. 
   Editing certain constants will break things! You have been warned!'''
from PIL import Image, ImageFont
import numpy
from subsystems.simplefancy import *

# Version
VERSION = "v0.0.0"
SYS_IVOS = [-999,-998,-997,-996]

# Sections
'''
- Calander Area: `(  14,  14) to ( 463, 683)` : size `( 450, 670)`
- Popup Area:    `( 240,  14) to ( 463, 213)` : size `( 224, 200)`
- Reminder Area: `( 478,  14) to ( 927, 683)` : size `( 450, 670)`
- Date Area:     `( 942,  14) to (1351, 341)` : size `( 410, 328)`
- Timer Area:    `( 942, 356) to (1351, 683)` : size `( 410, 328)`

Region ID : Top Left, Bottom Right, Size, Keep In Relative Top Left, Keep In Relative Top Right
'''
SECTIONS_DATA = {
    " ": [(   0,   0),(   0,   0),(   0,   0),(   0,   0),(   0,   0)],
    "c": [(  14,  14),( 463, 683),( 450, 670),(   0,   0),( 450, 670)],
    "p": [( 240,  14),( 463, 213),( 224, 200),(   0,   0),( 224, 200)],
    "r": [( 478,  14),( 927, 683),( 450, 670),(   0,   0),( 450, 670)],
    "d": [( 942,  14),(1351, 341),( 410, 328),(   0,   0),( 410, 328)],
    "t": [( 942, 356),(1351, 683),( 410, 328),(   0,   0),( 410, 328)],
}
SECTIONS_FRAME_INSTRUCTIONS = {
    " ": [],
    "c": genereateThemedBorderRectangleInstructions(( 450, 670),hexColorToRGBA(FRAME_COLOR)),
    "p": genereateThemedBorderRectangleInstructions(( 224, 200),hexColorToRGBA(FRAME_COLOR)),
    "r": genereateThemedBorderRectangleInstructions(( 450, 670),hexColorToRGBA(FRAME_COLOR)),
    "d": genereateThemedBorderRectangleInstructions(( 410, 328),hexColorToRGBA(FRAME_COLOR)),
    "t": genereateThemedBorderRectangleInstructions(( 410, 328),hexColorToRGBA(FRAME_COLOR)),
}
SECTIONS = list(SECTIONS_DATA.keys())

# Imagery
LOADING_IMAGE = Image.open(os.path.join("resources", "loading.png")).convert("RGBA") # 1366x697, Solid, Loading Screen
LOADING_IMAGE_ARRAY = numpy.array(LOADING_IMAGE)
EMPTY_LARGE_IMAGE = Image.open(os.path.join("resources", "blank_large.png")).convert("RGBA")
EMPTY_LARGE_IMAGE_ARRAY = numpy.array(EMPTY_LARGE_IMAGE)
PLACEHOLDER_IMAGE = Image.open(os.path.join("resources", "placeholder", "placeholder.png")).convert("RGBA")    # 512x512, Solid, [black, white, grey]
PLACEHOLDER_IMAGE_ARRAY = numpy.array(PLACEHOLDER_IMAGE)
PLACEHOLDER_IMAGE_2 = Image.open(os.path.join("resources", "placeholder", "placeholder2.png")).convert("RGBA")  # 100x100, Transparent Background [black, white, grey]
PLACEHOLDER_IMAGE_2_ARRAY = numpy.array(PLACEHOLDER_IMAGE_2)
PLACEHOLDER_IMAGE_3 = Image.open(os.path.join("resources", "placeholder", "placeholder3.png")).convert("RGBA")  # 128x128, Solid Background [black, white, grey]
PLACEHOLDER_IMAGE_3_ARRAY = numpy.array(PLACEHOLDER_IMAGE_3)
PLACEHOLDER_IMAGE_4 = Image.open(os.path.join("resources", "placeholder", "placeholder4.png")).convert("RGBA")  # 16x16, Transparent Background [black, white]
PLACEHOLDER_IMAGE_4_ARRAY = numpy.array(PLACEHOLDER_IMAGE_4)
PLACEHOLDER_IMAGE_5 = Image.open(os.path.join("resources", "placeholder", "placeholder5.png")).convert("RGBA")  # 32x32, Solid Background [rainbow]
PLACEHOLDER_IMAGE_5_ARRAY = numpy.array(PLACEHOLDER_IMAGE_5)
MISSING_IMAGE_PATH = os.path.join("resources", "missing.png")
MISSING_IMAGE = Image.open(os.path.join("resources", "missing.png")).convert("RGBA")
MISSING_IMAGE_ARRAY = numpy.array(MISSING_IMAGE)
EMPTY_IMAGE_ARRAY = numpy.zeros((1, 1, 4), dtype=numpy.uint8)

# Fonts
FONT_LARGE = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 24)
FONT_MEDIUM = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 15)
FONT_SMALL_MEDIUM = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 12)
FONT_SMALL = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 10)
EDITOR_SPACING = lambda x: x*20+15

# Cursors
CURSOR_ARROW_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "cursor_arrow.png"))
CURSOR_SELECT_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "cursor_select.png"))

# Image Arrays
ORB_IDLE_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "orb_idle.png"))
ORB_SELECTED_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "orb_selected.png"))
POINT_IDLE_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "point_idle.png"))
POINT_SELECTED_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "point_selected.png"))
CHECKLIST_NORMAL_ARRAY = generateOutlinedCircle(16, (230,230,230,255), FRAME_COLOR_RGBA)
CHECKLIST_LATE_ARRAY = generateOutlinedCircle(16, (255,230,230,255), FRAME_COLOR_RGBA)
CHECKLIST_COMPLETE_ARRAY = generateOutlinedCircle(16, (230,255,230,255), FRAME_COLOR_RGBA)

# Icons
ICON_CONSOLE_ARRAY = getArrayImageRGBAFromPath(os.path.join("resources", "icon", "console.png"))

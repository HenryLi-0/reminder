'''This file contains functions related to fancy rendering, but does not import from setting'''

from PIL import Image
import numpy, random, colorsys

def getArrayImageRGBAFromPath(path):
    '''Given a path, opens the image, converts it to RGBA, and returns it as a numpy array.'''
    return numpy.array(Image.open(path).convert("RGBA"))

def generateColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color'''
    array = numpy.empty((max(0,size[1]), max(0,size[0]), 4), dtype=numpy.uint8)
    array[:, :] = color
    return array

def generateUnrestrictedColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color without restrictions'''
    array = numpy.empty((size[1], size[0], 4))
    array[:, :] = color
    return array

def generateBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a bordered box with a transparent inside, with transparent space of (size), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1]+2*outlineW, size[0]+2*outlineW, 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return array

def generateInwardsBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a inwards bordered box with a transparent inside, with transparent space of (size - outline), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1], size[0], 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return array

def generatePastelDark():
    '''Randomly generates a dark pastel color'''
    color = [100]
    color.insert(random.randrange(0,len(color)+1), random.randrange(100,200))
    color.insert(random.randrange(0,len(color)+1), random.randrange(100,200))
    color.append(255)
    return color

def translatePastelLight(color):
    '''Translate a dark pastel color to a light pastel color, given the color in RGBA form'''
    colorC = color[0:3]
    colorC = list(colorsys.rgb_to_hsv(colorC[0]/255,colorC[1]/255,colorC[2]/255))
    colorC[2] = 0.9
    colorC = colorsys.hsv_to_rgb(colorC[0],colorC[1],colorC[2])
    return [round(colorC[0]*255), round(colorC[1]*255), round(colorC[2]*255), color[3]]

def generatePastelLight():
    '''Randomly generate a light pastel color'''
    color = []
    color.insert(random.randrange(0,len(color)+1), random.randrange(150,200))
    color.insert(random.randrange(0,len(color)+1), random.randrange(175,225))
    color.insert(random.randrange(0,len(color)+1), random.randrange(200,250))
    color.append(255)
    return color

def genereateThemedBorderRectangleInstructions(size:list|tuple = (25,25),borderColor:list|tuple = (255,255,255,255)):
    instructions = []
    row = generateColorBox((size[0],3), borderColor)
    col = generateColorBox((3,size[1]), borderColor)
    instructions.append([row, (0,0)])
    instructions.append([col, (0,0)])
    instructions.append([row, (0,size[1]-3)])
    instructions.append([col, (size[0]-3,0)])

    delete = generateUnrestrictedColorBox((9,9), (-255,-255,-255,-255))
    temp = [(7,4),(8,4),(6,5),(7,5),(8,5),(5,6),(6,6),(7,6),(8,6),(4,7),(5,7),(6,7),(7,7),(8,7),(4,8),(5,8),(6,8),(7,8),(8,8)]
    for coord in temp: delete[coord] = (0,0,0,0)
    for coord in [(0,size[1]-9), (size[0]-9,size[1]-9), (size[0]-9,0), (0,0)]:
        delete = numpy.rot90(delete, k=1, axes=(0, 1))
        instructions.append([delete, coord])
    corner = generateColorBox((9,9), (0,0,0,0))
    temp = [(6,0),(7,0),(8,0),(4,1),(5,1),(6,1),(7,1),(8,1),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(1,5),(2,5),(3,5),(4,5),(5,5),(0,6),(1,6),(2,6),(3,6),(4,6),(0,7),(1,7),(2,7),(3,7),(0,8),(1,8),(2,8),(3,8)]
    for coord in temp: corner[coord] = borderColor
    for coord in [(0,size[1]-9), (size[0]-9,size[1]-9), (size[0]-9,0), (0,0)]:
        corner = numpy.rot90(corner, k=1, axes=(0, 1))
        instructions.append([corner, coord])
    return instructions

def generateSpecificThemedBorderRectangleInstructions(section, borderColor:list|tuple = (255,255,255,255)):
    '''Generates Instructions for a specific section's Themed Border Rectangle'''
    return None

def generateCircle(radius, color):
    '''Generates a circle paint brush with given radius (radius) and color (RGBA)'''
    diameter = radius * 2
    array = numpy.empty((diameter, diameter, 4), dtype=numpy.uint8)
    center = radius
    for y in range(diameter):
        for x in range(diameter):
            distance = numpy.sqrt((x-center)**2+(y-center)**2)
            if distance <= radius:
                array[y,x] = color
            else:
                array[y,x] = (0,0,0,0)
    return array

def generateOutlinedCircle(fullradius, innercolor, outercolor):
    '''Generates an outlined circle, given the full radius, inner color, and outer color'''
    from subsystems.render import placeOver
    temp = generateCircle(fullradius, outercolor)
    placeOver(temp, generateCircle(fullradius-3, innercolor), (3,3))
    return temp

def generateHalfColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size with the right half (color) color'''
    array = numpy.empty((max(0,size[1]), max(0,size[0]), 4), dtype=numpy.uint8)
    array[:, max(0, round(size[0]/2)):] = color
    array[:, :max(0, round(size[0]/2))] = (0,0,0,0)
    return array
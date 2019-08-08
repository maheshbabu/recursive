# make flipbook pages for an animated specimen
# https://codepen.io/thundernixon/pen/wVypxe?editors=1100

from drawBot import * # requires drawbot to be installed as module
import datetime
from fontTools.misc.bezierTools import splitCubicAtT


# fontFam = "Rec Mono Beta013 Var"

fontFam = "/Users/stephennixon/type-repos/recursive/src/proofs/drawbot-diagrams-etc/flipbook/fonts/Recursive-mono-full--w_ital_slnt-2019_07_25.ttf"
frames = 100
format = "gif"

frontmatter = False
debug = True

bookSize = 3.5
DPI = 150
pixels = DPI*bookSize



W, H = pixels, pixels # size is 72 dpi * bookSize



minWeight = 300.01
maxWeight = 899.99

minExpression = 0.01
maxExpression = 1

maxSlant = 0
minSlant = -15
    

def interp(a, b, t):
    distance = b-a
    return(a + distance * t)


# ---------------------------------------------------------
# ANIMATION -----------------------------------------------

curviness = 0.7
        
def getCurveXY(t):
    currrve = ((0,0), (pixels*curviness, 22), (pixels-(pixels*curviness),pixels), (pixels,pixels))
    split = splitCubicAtT(*currrve, t)
    x,y = split[0][-1][0], split[0][-1][1]
    return(x,y)

curveDict = {}

for frame in range(frames+1):
    t = frame / frames    
    x,y = getCurveXY(t)

    curveDict[t] = (x,y)

import pprint
pp = pprint.PrettyPrinter(width=80, compact=False)
pp.pprint(curveDict)

for frame in range(frames):
    
    newPage(W, H)
    font(fontFam)
    # font("fonts/Recursive-mono-full--w_ital_slnt-2019_07_24.ttf")
    
    frameDuration(1/60)
    fill(0)
    rect(0,0,W,H)
    
    t = frame / frames    
    x,y = getCurveXY(t)
    
    fill(1)
    
    factor = y / pixels
    
    # completionOnCurve = ease(t)
    
    # TODO: split into quarters for smoother weight progression
    
    # if in first half of frames

    if frame <= frames*0.25:

        minXprn = 0.001
        maxXprn = 0.5

        minWeight = 300.01
        maxWeight = 800 - 0.01

        minSlnt = 0.01
        maxSlnt = -7.5

        currentItal = 0

        # keyframe = frames*0.25

        # factor = y / pixels * 1 / (curveDict[0.25][1]/H) # 0.17392
        factor = y / pixels * 1 / (curveDict[0.25][1]/H) # 0.17392

        # print(curveDict["0.25"][1] / curveDict["1.0"][1])

    if frame > frames*0.25 and frame <= frames*0.5:
    # if frame <= frames*0.5:
        
        minXprn = 0.5
        maxXprn = 1
        
        minWeight = 800.01
        maxWeight = 900 - 0.01
        
        minSlnt = -7.5
        maxSlnt = -15
        
        currentItal = 0
                
        # completionOnCurve = y / H * 0.5
        # factor = y / pixels * 2 
        # factor = y / pixels * 1 / (curveDict[0.5][1]/H)
        factor = y / pixels * 1/ .484285714 # ((H-curveDict[0.5][1])/H)
        
        
        
    if frame > frames*0.5 and frame <= frames * 0.75:
        minXprn = 1
        maxXprn = 0
        
        minWeight = 900 - .01
        maxWeight = 800 + 0.01
        
        minSlnt = -15
        maxSlnt = 0
        
        currentItal = 1
        
        # factor = (y - 0.5) / pixels * 2 - 1
        factor = (y - 0.5) / pixels * 1/ .150357143 # ((H-curveDict[0.75][1])/H)
        
    if frame > frames*0.75:
        minXprn = 1
        maxXprn = 0
        
        minWeight = 800 - .01
        maxWeight = 300 + 0.01
        
        minSlnt = -15
        maxSlnt = 0
        
        currentItal = 1
        
        # factor = (y - 0.5) / pixels * 2 -1
        factor = y / pixels * 1/(curveDict[1.0][1]/H)
        
    # if frame > frames * 0.6:
        
    #     currentItal = 1
    
    
    currentXprn = interp(minXprn, maxXprn, factor)
    currentWeight = interp(minWeight, maxWeight, factor)
    currentSlnt = interp(minSlnt, maxSlnt, factor)
    
    fontVariations(
        wght=currentWeight,
        XPRN=currentXprn,
        slnt=currentSlnt,
        ital=currentItal
        )
    
    print(str(frame).ljust(3), " | factor: ", str(round(factor, 3)).ljust(5)," | t: ", str(round(t, 3)).ljust(5), " | wght: ", currentWeight)
    
    fontSize(W/1.4)
    text("rw", (W/15, H/12))
    
    fontSize(W/30)
    
    padding = 0.1
    # text(str(round(currentWeight)), (((W*0.1)+(W*completionOnCurve * 0.7)), H *0.7))
    
    x = str('{:4.2f}'.format(currentXprn))
    w = str('{:3.0f}'.format(currentWeight))
    s = str('{:5.2f}'.format(abs(currentSlnt)))
    i = str('{:4.2f}'.format(currentItal))
    text(f"p {str(0)}   x {x}   w {w}   s -{s}   i {i}", (((W*0.025)), H *0.025))

    print("*", end=" ")

    if debug:
        fill(1,0,1,1)
        size = pixels/pixels * 2
        # rect(0,H*.66, W*y/W, size)      # y - curved

        for i in range(frames):
            
            fill(0.6,0.6,0.6,0.25)
            t = i / frames

            x,y = getCurveXY(t)
            
            size = pixels/pixels * 4
            oval(x-size/2, (y*0.375)+(H/12)-(size/2), size, size)
            # oval(x-size/2, (y)-(size/2), size, size)
            
        fill(1,0,1,1)
        t = frame / frames
        
        x,y = getCurveXY(t)
                
        size = pixels/pixels * 6
        oval(x-size/2, (y*0.375)+(H/12)-(size/2), size, size)
        # oval(x-size/2, (y)-(size/2), size, size)


now = datetime.datetime.now().strftime("%Y_%m_%d-%H") # -%H_%M_%S

saveImage("/Users/stephennixon/type-repos/recursive/src/proofs/drawbot-diagrams-etc/flipbook/exports/recursive-flipbook-" + now + "." + format)
from psychopy import visual, core, event
from psychopy.visual.slider import Slider
from psychopy.hardware import keyboard
from psychopy.core import wait
import pathlib
import os
import pandas
from psychopy.clock import Clock

def present_img(win, ipath):

    "Part of Day 1 experiment. Presents image path passed to window passed"
    "win: window to be presented to (Psychopy window)"
    "ipath: path to image"

    "returns what patient entered disturbance level as, and reaction time"

    #Initialize sizes

    windowsize = win.size
    img = pathlib.Path(ipath).absolute().resolve()
    ssize = [6 * windowsize[0] / 8, windowsize[1]/25]
    isize = [windowsize[1]/2, windowsize[1]/2]
    ipos = [0, 1/8 * windowsize[1]]

    # Create a window

    # Create a slider
    spos = pos=(ipos[0], windowsize[1] / -4.0)
    vas = Slider(win,
                ticks=range(10),
                labels=range(0, 10),
                granularity=0.1,
                color='black',
                size=ssize, 
                pos=(spos),
                borderColor='black',
                style="slider"
                )

    # Create instructions text
    instructions = visual.TextStim(win, text="Please rate the level of distress caused by this image:", pos=(ipos[0], ipos[1] + isize[1] / 1.5)
                                   , color="black", font='arial')


    #create image
    image_stim = visual.ImageStim(win, image=img, pos=ipos, size=isize)

    c = Clock()

    startt = c.getTime()

    instructions.draw()
    image_stim.draw()
    vas.draw()
    val = vas.getMarkerPos()
    visual.TextStim(win, text=f"{val}", pos=(spos[0] + ssize[0] / 1.75, spos[1]), color="black", font = 'arial').draw()

    win.flip()

    while True:

        #Key decisions, if key is pressed, do ting

        keys = event.waitKeys()[0]
        endt = c.getTime()
        if 'escape' in keys or 'close' in keys:
            core.quit()
        try:
            keys = int(keys)
            if keys in range(1, 10):
                
                vas.setMarkerPos(keys)

                #Fade out image feature, might delete later idk
                for x in [x / 10 for x in range(0, 11)]:
                    image_stim.setOpacity(1 - x)
                    instructions.draw()
                    image_stim.draw()
                    vas.draw()
                    val = vas.getMarkerPos()
                    visual.TextStim(win, text=f"{val}", pos=(spos[0] + ssize[0] / 1.75, spos[1]), color="black").draw()
                    win.flip()
                break
        except:
            continue
        
    # Get the final rating
    return keys, endt - startt
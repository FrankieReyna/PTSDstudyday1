from psychopy import visual, core, event
from psychopy.visual.slider import Slider
from psychopy.hardware import keyboard
from psychopy.core import wait
import pathlib
import os
import pandas
from psychopy.clock import Clock

def present_img(win, ipath):
    windowsize = win.size
    img = pathlib.Path(ipath).absolute().resolve()

    ssize = [6 * windowsize[0] / 8, windowsize[1]/25]
    isize = [windowsize[1]/2, windowsize[1]/2]
    ipos = [0, 1/8 * windowsize[1]]

    # Create a window

    # Create a slider
    spos = pos=(ipos[0], windowsize[1] / -4.0)
    vas = Slider(win,
                ticks=range(11),
                labels=range(0, 11),
                granularity=0.1,
                color='black',
                size=ssize, 
                pos=(spos),
                borderColor='black',
                style="slider"
                )

    # Create instructions text
    instructions = visual.TextStim(win, text="Please rate the level of distress caused by this image:", pos=(ipos[0], ipos[1] + isize[1] / 1.5), color="black")

    # Create a "Next" button
    image_stim = visual.ImageStim(win, image=img, pos=ipos, size=isize)

    c = Clock()

    startt = c.getTime()

    while True:
        instructions.draw()
        image_stim.draw()
        vas.draw()
        val = vas.getMarkerPos()
        visual.TextStim(win, text=f"{val}", pos=(spos[0] + ssize[0] / 1.75, spos[1]), color="black").draw()
        
        # Update the window
        win.flip()

        

        keys = event.waitKeys()[0]
        endt = c.getTime()
        if 'escape' in keys:
            core.quit()
        try:
            keys = int(keys)
            if keys in range(1, 10):
                
                vas.setMarkerPos(keys)
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

def recursive_img(results, win, ipath, file):
    if os.path.isdir(ipath):
        for file in os.listdir(ipath):
            opath = os.path.join(ipath, file)
            recursive_img(results, win, opath, file)
    else:
        results[file] =  [present(win, ipath), ipath[-3:]]

if __name__ == "__main__":

    results = {}
    imgdir = "ipool"
    win = visual.Window(size=[800, 600], units="pix", color="white")

    recursive_img(results, win, imgdir, "")

    win.close()
    print(f"Final rating: {results}")
    df = pandas.DataFrame(results).transpose().rename_axis('Names')

    df.columns = ['Pscore', 'Neg/Neu']

    print(next(df.iterrows()))
    df.to_csv("results")


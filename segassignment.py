import os
import random
from segment import dirinfo, imginfo, Segment
import pathlib
from present import present_img
from psychopy import visual
import pandas as pd
import psychopy.gui as psygui


def pres_assign(imgdir):

    "Assigns each image in a directory to 'Mass' or 'Spaced'. Randomly done"
    "imgdir: directory of images to assign"

    #Create dictionary to store images in their sections (directory name/spaced or mass)

    dict = {}
    for val in os.listdir(imgdir):
        imgdirs = os.listdir(os.path.join(imgdir, val))
        mOs = ''
        for x in range(len(imgdirs)):
            img = random.choice(imgdirs)
            mOs =  "spaced" if x % 2 == 0 else "mass"
            direntry = dirinfo(img, val, mOs, os.path.join(imgdir, os.path.join(val, img)))
            imgdirs.remove(img)
            try:
                dict[os.path.join(val, mOs)].append(direntry)
            except KeyError:
                dict[os.path.join(val, mOs)] = [direntry]
        
    return(dict)

def seg_assign(imgdir, m_per_seg, num_segs):

    "Assigns the segments used in experient, returns segs as list. Each segment has m_per_seg. This is basically how many blocks there are."
    "For example, m_per_seg = 2 means (2massNeg, 2massNeu, 2spcNeg, 2spcNeu). Num_segs is how many individual segments there are."
    "The num_segs determines number of segments. This should mach the number of copies made for each image so spaced images are consistent."

    dict = pres_assign(imgdir)
    numvars = num_segs

    segs = []

    for x in range(num_segs):
        segs.append(Segment(numvars))
        
    dng = dict['Negative\\mass']
    dne = dict['Neutral\\mass']
        
    #runs through each segment, give each segment number of massed and spaced blocks needed

    for x in range(num_segs):
        
        for _ in range(m_per_seg):
            segs[x].add_mblock(dng[0])
            del dng[0]
            segs[x].add_mblock(dne[0])
            del dne[0]

    for x in range(len(dict['Negative\\spaced'])):
        for y in range(num_segs):
            segs[y].add_sblock(dict['Negative\\spaced'][x], y)
            segs[y].add_sblock(dict['Neutral\\spaced'][x], y)

    return segs

def present_segs(segs):

    #Get participant ID

    participant = {"Participant #": ""}
    pnum = psygui.DlgFromDict(participant)
    win = visual.Window(size=(1920, 1080), units="pix", color="white")
    nsegs = list(segs)
    df = pd.DataFrame()

    #Go thorugh each seg, randomly presenting blocks of each segment

    for i in range(len(nsegs)):
        idx = random.randint(0, len(nsegs) - 1)
        seglist = nsegs[idx].get_blocks()
        del nsegs[idx]
        for j in range(len(seglist)):
            idx = random.randint(0, len(seglist) - 1)
            block = seglist[idx]
            del seglist[idx]
            for k in range(len(block)):
                idx = random.randint(0, len(block) - 1)
                img = block[idx]
                score, rt = present_img(win, img.path)
                df = pd.concat([df, pd.DataFrame({"partinum" : participant['Participant #'], "imgname" : img.name, "valScore" : score, "resptime" : rt, "val" : img.val, "pres" : img.pres, "path" : img.path}, index = [0])], ignore_index=True)
                del block[idx]

    return df, participant



import os
import random
import segment
from segment import dirinfo, imginfo, Segment
import pillow
import pathlib
from present import present_img
from psychopy import visual
import pandas as pd
import psychopy.gui as psygui


def pres_assign(imgdir):
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
    dict = pres_assign("ipool2")
    numvars = num_segs

    segs = []

    for x in range(num_segs):
        segs.append(Segment(numvars))
        
    dng = dict['Negative\\mass']
    dne = dict['Neutral\\mass']
        
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
    participant = {"Participant #": ""}
    pnum = psygui.DlgFromDict(participant)
    win = visual.Window(size=(800, 600), units="pix", color="white")
    nsegs = list(segs)
    df = pd.DataFrame()

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
                print(df)
                del block[idx]
    df.to_csv("results")


output = pathlib.Path("ipool2")

segs = seg_assign(output, 2, 4)
present_segs(segs)
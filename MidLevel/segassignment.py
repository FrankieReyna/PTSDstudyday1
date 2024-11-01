import os
import random
from MidLevel.segment import dirinfo, imginfo, Segment
from MidLevel.LowLevel.present import present_img, present_instruction
import pandas as pd
import datetime

#revamp this to just use a CSV file that records segment, val, pres type

def pres_assign(imgdir):

    "Assigns each image in a directory to 'Mass' or 'Spaced'. Randomly done"
    "imgdir: directory of images to assign"

    #Create dictionary to store images in their sections (directory name/spaced or mass)
    df = pd.DataFrame()
    for val in os.listdir(imgdir):
        valpath = os.path.join(imgdir, val)
        imgdirs = os.listdir(valpath)
        random.shuffle(imgdirs)
        mOs = ''
        x=0
        for img in imgdirs:
            mOs =  "spaced" if x % 2 == 0 else "mass"
            x += 1
            df = pd.concat([df, pd.DataFrame(data=[dirinfo(img, val, mOs, os.path.join(valpath, img))])], ignore_index=True) #you actually do need to include the path
    print(df)
        
    return(df)

def seg_assign(imgdir, m_per_seg, num_segs):

    "Assigns the segments used in experient, returns segs as list. Each segment has m_per_seg. This is basically how many blocks there are."
    "For example, m_per_seg = 2 means (2massNeg, 2massNeu, 2spcNeg, 2spcNeu). Num_segs is how many individual segments there are."
    "The num_segs determines number of segments. This should mach the number of copies made for each image so spaced images are consistent."

    df = pres_assign(imgdir)
    
    numvars = num_segs

    segs = []

    for x in range(num_segs):
        segs.append(Segment(numvars))
        
    dng = df.loc[(df['val'] == "Negative") & (df['pres'] == 'mass')]
    dne = df.loc[(df['val'] == "Neutral") & (df['pres'] == 'mass')]
        
    #runs through each segment, give each segment number of massed and spaced blocks needed

    y = 0
    for x in range(num_segs):
        
        for _ in range(m_per_seg):
            segs[x].add_mblock(dng.iloc[y])
            segs[x].add_mblock(dne.iloc[y])
            y += 1

    dng = df.loc[(df['val'] == "Negative") & (df['pres'] == 'spaced')]
    dne = df.loc[(df['val'] == "Neutral") & (df['pres'] == 'spaced')]

    for x in range(dng.shape[0]):
        for y in range(num_segs):
            segs[y].add_sblock(dng.iloc[x], y)
            segs[y].add_sblock(dne.iloc[x], y)

    return df, segs

def present_segs(win, segs, segfills, partnum, PRACMODE, BREAK=False, SEGSPERBREAK=0, BREAKSLIDEPATH=""):

    #Get participant ID


    nsegs = list(segs)
    df = pd.DataFrame()

    #Go thorugh each seg, randomly presenting blocks of each segment
    segcount = 0
    fillerstart = 0
    for _ in range(len(nsegs)):
        df = present_fillers(win, df, segfills, fillerstart, partnum, PRACMODE)
        fillerstart += segfills
        if segcount == SEGSPERBREAK and BREAK == True:
        #initiate break mode:
            segcount = 0
            present_instruction(win, BREAKSLIDEPATH, 5)
        idx = random.randint(0, len(nsegs) - 1)
        seglist = nsegs[idx].get_blocks()
        del nsegs[idx]
        segcount += 1
        for _ in range(len(seglist)):
            idx = random.randint(0, len(seglist) - 1)
            block = seglist[idx]
            del seglist[idx]
            for _ in range(len(block)):
                idx = random.randint(0, len(block) - 1)
                img = block[idx]
                score, rt = present_img(win, img.path, PRACMODE)
                df = pd.concat([df, pd.DataFrame({"partinum" : partnum, "orgimg" : img.dirname, "imgname" : img.name, "valScore" : score
                                                  ,"resptime" : rt, "val" : img.val, "pres" : img.pres, "path" : img.path, "date" : datetime.datetime.now()}, index = [0])], ignore_index=True)
                del block[idx]

    return df

def present_fillers(win, df, num_pres, start, partnum, PRACMODE):
    for img in os.listdir("fillers")[start:start+num_pres]:
        print(img)
        path =  os.path.join("fillers", img)
        score, rt = present_img(win, path, PRACMODE)
        df = pd.concat([df, pd.DataFrame({"partinum" : partnum, "orgimg" : "N/A", "imgname" : img, "valScore" : score
                                    ,"resptime" : rt, "val" : "fill", "pres" : "fill", "path" : path, "date" : datetime.datetime.now()}, index = [0])], ignore_index=True)
    return df


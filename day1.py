import MidLevel.segassignment as exp
import MidLevel.LowLevel.pillow as pill
from pathlib import Path
import os
from psychopy import visual
from MidLevel.LowLevel.present import present_instruction, present_img
import psychopy.gui as psygui

PRACMODE = False #Prac mode does not save data, good for not mudding everything up

"HERE WE ARE GOING TO DICTATE WHERE OUR RESULTS GO, WHERE TO GET/PUT IMAGES, AND THE PARAMETERS OF OUR EXPR"
result_export_dir = Path(r"results").resolve()
#Initialize what Directories used for image storage/presentation
source = "MainSource" # This directory should be split into two different ones, Negative and Neutral (Mainsource > Neg - Neutral)
pracsource = "PracSource" # Images in here will be presented in practice round at start, ALL WILL BE PRESENTED
copydir = "TransImgs" # No need to store antying

source = Path(source).resolve()
copydir = Path(copydir).resolve()

"number of segments determines # of copies for each image"

#number of images in each group (16Neg, 16Neu) = 16
num_imgs_per_val = 16
segfillers = 4 #how many fillers do we want presented before and after a new segment?
num_segs = 4 #number of segments in experiments
num_copies = num_segs #this ensures spaced repetitions are presented each segment
num_blocks = int(num_imgs_per_val / num_segs / 2) #dictates how many of each block (negmass, negspace, etc) are presented
sfactor = 3 #changes SkewFactor, how varied the image copies are

if num_imgs_per_val % num_segs != 0:
    raise Exception("please make sure # of images in Neu/Neg are == and divisible by num_segs")
if not os.path.exists(copydir):
    raise Exception("no source img dir found")



"Creates Image Copies, creates segments, assigns segments with images, collect participant info (pillow.py, segassign.py)"

# Creates image copies
pill.create_pool(source, copydir, num_copies, sfactor)
participant_pres, segs = exp.seg_assign(copydir, num_blocks, num_segs)
participant = {"Participant #": ""}
pnum = psygui.DlgFromDict(participant)
partnum = participant['Participant #']


"Presents Instructions, gives a practice round (present.py)"

#First set of instructions
win = visual.Window(fullscr=True, units="pix", color="white")
present_instruction(win, r'Ver2__PTSD_pilot_text\begininstr1.jpg')
present_instruction(win, r'Ver2__PTSD_pilot_text\begininstr2.jpg')
present_instruction(win, r'Ver2__PTSD_pilot_text\prac1.jpg')

#Practice

for img in os.listdir(pracsource): 
    present_img(win, os.path.join(pracsource, img), True)

present_instruction(win, r'Ver2__PTSD_pilot_text\prac2.jpg')



"Create datastrucutre to keep data, start presentation chain, decide whether to save data and to where."
"Both day1data and presentation order are reported (segassign.py, why is it there? might change)"

data = exp.present_segs(win, segs, segfillers, partnum, PRACMODE, BREAK=True, SEGSPERBREAK=1, BREAKSLIDEPATH=r'Ver2__PTSD_pilot_text\break.jpg')
present_instruction(win, r'Ver2__PTSD_pilot_text\expend.jpg')
ppath = os.path.join(result_export_dir, f"P{partnum}")
print(ppath)

if not os.path.exists(ppath):
    os.mkdir(ppath)
    print(ppath)
if(not PRACMODE):
    data.to_csv(os.path.join(ppath, "day1"))
    participant_pres.to_csv(os.path.join(ppath, "day1pres"))
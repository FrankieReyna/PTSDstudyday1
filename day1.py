import MidLevel.segassignment as exp
import MidLevel.LowLevel.pillow as pill
from pathlib import Path
import os
from psychopy import visual
from MidLevel.LowLevel.present import present_instruction, present_img
import psychopy.gui as psygui

"Create pool of images, making copies of images put into source"


result_export_dir = Path(r"results").resolve()

if not os.path.exists(result_export_dir):
    raise Exception("Results directory DNE")

#get source path

PRACMODE = False 

source = "MainSource"
pracsource = "PracSource"
copydir = "TransImgs"

if source == copydir:
    raise Exception("source dir should not be the same as copy dir")

source = Path(source).resolve()
copydir = Path(copydir).resolve()

"number of segments determines # of copies for each image"


#number of images in each group (16Neg, 16Neu) = 16
num_imgs_per_val = 16

segfillers = 4 #TO DO: need 4 in the beginning of seg, 4 at the end

num_segs = 4 #number of segments in experiments
num_copies = num_segs #make sure this is equal

num_m_blocks = int(num_imgs_per_val / num_segs / 2)

sfactor = 4 #changes SkewFactor

print(num_m_blocks)

if num_imgs_per_val % num_segs != 0:
    raise Exception("please make sure # of images in Neu/Neg are == and divisible by num_segs")

if not os.path.exists(copydir):
    raise Exception("no source img dir found")

pill.create_pool(source, copydir, num_copies, sfactor)

participant_pres, segs = exp.seg_assign(copydir, num_m_blocks, num_segs)

participant = {"Participant #": ""}
pnum = psygui.DlgFromDict(participant)
partnum = participant['Participant #']

#First set of instructions
win = visual.Window(fullscr=True, units="pix", color="white")
present_instruction(win, r'Ver2__PTSD_pilot_text\begininstr1.jpg')
present_instruction(win, r'Ver2__PTSD_pilot_text\begininstr2.jpg')
present_instruction(win, r'Ver2__PTSD_pilot_text\prac1.jpg')
#Practice

for img in os.listdir(pracsource): 
    present_img(win, os.path.join(pracsource, img), True)

present_instruction(win, r'Ver2__PTSD_pilot_text\prac2.jpg')

#Main stuff

data = exp.present_segs(win, segs, segfillers, partnum, PRACMODE, BREAK=True, SEGSPERBREAK=1, BREAKSLIDEPATH=r'Ver2__PTSD_pilot_text\break.jpg')

present_instruction(win, r'Ver2__PTSD_pilot_text\expend.jpg')

ppath = os.path.join(result_export_dir, f"P{partnum}")
print(ppath)

if not os.path.exists(ppath):
    os.mkdir(ppath)
    print(ppath)

print("pa")
if(not PRACMODE):
    print("ma")
    data.to_csv(os.path.join(ppath, "day1"))
    participant_pres.to_csv(os.path.join(ppath, "day1pres"))





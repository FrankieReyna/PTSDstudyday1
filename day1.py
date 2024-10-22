import MidLevel.segassignment as exp
import MidLevel.LowLevel.pillow as pill
from pathlib import Path
import os

"Create pool of images, making copies of images put into source"


result_export_dir = Path(r"C:\Users\Frankie\Documents\PTSDpsycho\results").resolve()

if not os.path.exists(result_export_dir):
    raise Exception("Results directory DNE")

#get source path

PRACMODE = True

source = "PracSource"
copydir = "TransImgs"

if source == copydir:
    raise Exception("source dir should not be the same as copy dir")

source = Path(source).resolve()
copydir = Path(copydir).resolve()

"number of segments determines # of copies for each image"

num_imgs_per_val = 2

num_segs = 1
num_copies = num_segs

num_m_blocks = int(num_imgs_per_val / num_segs / 2)

sfactor = 3

print(num_m_blocks)

if num_imgs_per_val % num_segs != 0:
    raise Exception("please make sure # of images in Neu/Neg are == and divisible by num_segs")

if not os.path.exists(copydir):
    raise Exception("no source img dir found")

pill.create_pool(source, copydir, num_copies, sfactor)

segs = exp.seg_assign(copydir, num_m_blocks, num_segs)

df, participant = exp.present_segs(segs, PRACMODE)

ppath = os.path.join(result_export_dir, f"P{participant['Participant #']}")

if not os.path.exists(ppath):
    os.mkdir(ppath)
    print(ppath)

ppath = os.path.join(ppath, "day1")

if(not PRACMODE):
    df.to_csv(ppath)





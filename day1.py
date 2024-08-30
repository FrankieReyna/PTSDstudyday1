import experiment as exp
import present as pres
import pillow as pill
from pathlib import Path
import os

#pill.create_pool(source, copydir, num_copies, sfactor)

source = Path("source").resolve()
copydir = Path("ipool").resolve()
num_copies = 4
num_m_blocks = 2
num_segs = num_copies
sfactor = 3



if not os.path.exists(copydir):
    raise Exception("no source img dir found")


segs = exp.seg_assign(copydir, num_m_blocks, num_segs)

exp.present_segs(segs)





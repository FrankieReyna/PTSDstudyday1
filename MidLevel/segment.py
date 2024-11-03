import os
import random
from collections import namedtuple

# need to implement segments:
    #from img dir, need to seperate each image into either spaced or neg
    #Need to assign each image after to its own segment 

#because of this, segments need to basically act as image categories for presentor to present
#After I will make file that combines everything

"Goes through each image directory and assigns it spaced or mass"
#image dir is ipool

dirinfo = namedtuple('dirinfo', ['name', 'val', 'pres', 'path'])
imginfo = namedtuple('imginfo', ['dirname', 'name', 'val', 'pres', 'path'])



class Segment():

    def __init__(self, num_vars, req_same_num = True):
        self.num_vars = num_vars
        self.req_same_num = req_same_num
        self.IMGS = []

    def get_blocks(self):
        return self.IMGS

    def add_mblock(self, dictinfo):
        m_block = []
        imgs = os.listdir(dictinfo.path)
        print(dictinfo['name'])
        if self.req_same_num and self.num_vars != len(imgs):
            raise RuntimeError(f"The # of images in {dictinfo.name} ({len(imgs)}) does not match num_vars for segment ({self.num_vars})")
        for img in imgs:
            imgentry = imginfo(dictinfo['name'], img, dictinfo.val, dictinfo.pres, os.path.join(dictinfo.path, img))
            m_block.append(imgentry)
        self.IMGS.append(m_block)

    def add_sblock(self, dictinfo, idx_var):
        s_block = []
        img = os.listdir(dictinfo.path)[idx_var]
        imgentry = imginfo(dictinfo['name'], img, dictinfo.val, dictinfo.pres, os.path.join(dictinfo.path, img))
        s_block.append(imgentry)
        self.IMGS.append(s_block)




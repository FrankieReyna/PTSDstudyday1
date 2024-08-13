from PIL import Image
import os
import random as r
import shutil
import numpy
import pathlib

def crop_vars(source, mwidth, mheight):

    "Randomly crops image from source based on minimum width and height"
    "returns newly cropped image copy"

    img_path = f"{source}"
    image = Image.open(img_path)

    width, height = image.size


    left = r.uniform(0, width - mwidth)
    right = left + mwidth
    top = r.uniform(0, height - mheight)
    bottom = top + mheight

    dim = [left, top, right, bottom]

    crop = image.crop(dim)

    return crop.resize((width, height))


def temp_change(source):

    "Randomly changes tempurature of image  of path passed."
    "returns new intensity transformed image"

    img = Image.open(source)
    R, b, g = [r.randint(100, 256), r.randint(100, 256), r.randint(100, 256)]
    M = (R/255.0, 0, 0, 0,
         0, g/255.0, 0, 0,
         0, 0, b/255.0, 0)
    return img.convert("RGB", M)

def quality(source, quality):

    "Returns quality reduced image."

    img = Image.open(source)
    size = img.size
    dim = ((int)(x / quality) for x in size)
    img = img.resize(dim)
    return img.resize(size)


def skew(source, factor):

    "performs and returns homographic transform on image passed to this method. Factor distorts the image"
    "the lower  it the value it."
    "img: image to be skewed"
    "skew: skew factor. higher less skew, lower more skew. (values between 0 - 2 make the image really weird)"

    img = Image.open(source)
    width, height = img.size
    matrix = []

    np1 = (0 + r.randint(0, int(width/factor)), 0 + r.randint(0, int(height/factor)))
    np2 = (width - r.randint(0, int(width/factor)), 0 + r.randint(0, int(height/factor)))
    np3 = (width - r.randint(0, int(width/factor)), height - r.randint(0, int(height/factor)))
    np4 = (0 + r.randint(0, int(width/factor)), height - r.randint(0, int(height/factor)))

    pb = [np1, np2, np3, np4] 
    
    pa = [(0, 0), (width, 0), (width, height), (0, height)]
    
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    coeffs = numpy.array(res).reshape(8)
    imgn = img.transform((width, height), Image.PERSPECTIVE, coeffs,Image.BICUBIC)
    return imgn
            
def create_copies(path, output, num_copies, sfact):

    tail = os.path.split(path)[1]
    file, ext = os.path.splitext(tail)

    if not os.path.exists(output):
        os.mkdir(output)

    output = os.path.join(output, file)
    if os.path.exists(output):
        shutil.rmtree(output)
    os.mkdir(output)

    for x in range(0, num_copies):
        nname = os.path.join(file + f"{x}" + ext)
        print(x)
        img = crop_vars(path, 500, 500)
        skew(path, sfact).save(os.path.join(output, nname))

def create_pool(sourcedir, outputdir, num_copies, sfact):

    "This method assumes 2 things"
    "   1: the source imgs are in a directory, within a directory"
    "   2: These directories are seperated based on 'Neg' and 'Neu'"

    if os.path.exists(outputdir):
        shutil.rmtree(outputdir)

    os.mkdir(outputdir)

    for root, dirs, files in os.walk(sourcedir):
        for name in files:
            if name != '.DS_Store':          
                source = pathlib.Path(os.path.join(root, name)).resolve()
                valdir = os.path.split(os.path.split(source)[0])[1]
                outdir = pathlib.Path(outputdir).resolve()
                outdir = os.path.join(outdir, valdir)
                create_copies(source, outdir,num_copies, sfact)

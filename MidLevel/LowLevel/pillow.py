from PIL import Image
import os
import random as r
import shutil
import numpy
import pathlib

def crop_vars(source, mwidth, mheight):

    "Randomly crops image from source based on minimum width and height"
    "returns newly cropped image copy"

    #opens image

    img_path = f"{source}"
    image = Image.open(img_path)

    #record width

    width, height = image.size

    #randomly determines lines from which to crop from

    left = r.uniform(0, width - mwidth)
    right = left + mwidth
    top = r.uniform(0, height - mheight)
    bottom = top + mheight

    dim = [left, top, right, bottom]

    #crop and return image

    crop = image.crop(dim)

    return crop.resize((width, height))


def temp_change(source):

    "Randomly changes tempurature of image  of path passed."
    "returns new intensity transformed image"

    #opens image

    img = Image.open(source)

    #randomly choose color

    R, b, g = [r.randint(100, 256), r.randint(100, 256), r.randint(100, 256)]
    M = (R/255.0, 0, 0, 0,
         0, g/255.0, 0, 0,
         0, 0, b/255.0, 0)
    
    #apply matrix to image

    return img.convert("RGB", M)

def quality(source, quality):

    "Returns quality reduced image."

    #funny thing with the resize feature, does not account for quality.
    #If you resize the image to be smaller, and then put it back to its original size,
    #It acts like youre changing the quality 

    img = Image.open(source)
    size = img.size
    dim = ((int)(x / quality) for x in size)
    img = img.resize(dim)
    return img.resize(size)


def skew(source, factor):

    "performs and returns homographic transform on image passed to this method. Factor distorts the image"
    "source: img path "
    "factor: skew factor. higher less skew, lower more skew. (values between 0 - 2 make the image really weird)"

    #Got someone to explain the homographic transform. Look it up on wiki or youtube if you want to know how its done
    #Basically open image, crate a matrix

    img = Image.open(source)
    width, height = img.size
    matrix = []

    #A homographic transform works by moving original corners to new corners (nps). So, determine new corners (randomly)

    np1 = (0 + r.randint(0, int(width/factor)), 0 + r.randint(0, int(height/factor)))
    np2 = (width - r.randint(0, int(width/factor)), 0 + r.randint(0, int(height/factor)))
    np3 = (width - r.randint(0, int(width/factor)), height - r.randint(0, int(height/factor)))
    np4 = (0 + r.randint(0, int(width/factor)), height - r.randint(0, int(height/factor)))

    #new corners

    pb = [np1, np2, np3, np4] 

    #old coners
    
    pa = [(0, 0), (width, 0), (width, height), (0, height)]

    #create homographic matrix
    
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    #apply image matrix with homographic matrix

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    coeffs = numpy.array(res).reshape(8)
    imgn = img.transform((width, height), Image.PERSPECTIVE, coeffs,Image.BICUBIC)
    return imgn

def create_copies(path, output, num_copies, sfact):

    "Using previous methods (Skew, crop) Allows for multiple variations of imgs to be made. cropping is random"
    "skew is determined by skew factor. Takes from a source img, puts into output directiry as a dir of img vars"
    "path: Image path to be copied"
    "output: output directory path to store copies)"
    "num_copies: how many copies need to be made"
    "sfactor: skew factor for images"

    #Figure out name of file

    tail = os.path.split(path)[1]
    file, ext = os.path.splitext(tail)

    #If the output doesnt exit, create it

    if not os.path.exists(output):
        os.mkdir(output)

    #If we havent got a section to put copies, make one

    output = os.path.join(output, file)
    if os.path.exists(output):
        shutil.rmtree(output)
    os.mkdir(output)
    
    #create copies

    for x in range(0, num_copies):
        nname = os.path.join(file + f"{x}" + ext)
        img = crop_vars(path, 100, 100) #changes crop of the images
        skew(path, sfact).save(os.path.join(output, nname))

def create_pool(sourcedir, outputdir, num_copies, sfact):

    "This method assumes 2 things"
    "   1: the source imgs are in a directory, within a directory"
    "   2: These directories are seperated based on 'Neg' and 'Neu'"

    #deletes then creates output directory

    if os.path.exists(outputdir):
        shutil.rmtree(outputdir)

    os.mkdir(outputdir)

    #for each image in the source directory, create copies of all images. 

    for root, dirs, files in os.walk(sourcedir):
        for name in files:
            if name != '.DS_Store':          
                source = pathlib.Path(os.path.join(root, name)).resolve()
                valdir = os.path.split(os.path.split(source)[0])[1]
                outdir = pathlib.Path(outputdir).resolve()
                outdir = os.path.join(outdir, valdir)
                create_copies(source, outdir,num_copies, sfact)

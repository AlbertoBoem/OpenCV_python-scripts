import math
import operator
from PIL import Image
import sys
import os
import glob
import subprocess
import shutil
from functools import reduce

# Requires FFMPEG

def compare(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    h1 = image1.histogram()
    h2 = image2.histogram()
    rms = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    return rms

if __name__=='__main__':

    # use ffmpeg filter to locate I frames (aka keyframes)
    cmd = ["ffmpeg", "-i", sys.argv[1], "-vf", "select='eq(pict_type,I)'", "-vsync", "0", "-f", "image2", "decomp/%09d.jpg"]
    # -i (get information about video file), select='eq(pict_type,I) (select only I frames)

    subprocess.call(cmd)

    print("Done")

    file_list = glob.glob(os.path.join("decomp", '*.jpg'))
    file_list.sort()
    for ii in range(0, len(file_list)):
        if ii < len(file_list)-1:
            if compare(file_list[ii], file_list[ii+1]) == 0:
                print('Found similar images: ' + file_list[ii] + " and " + file_list[ii+1])
            else:
                head, tail = os.path.split(file_list[ii])
                shutil.copyfile(file_list[ii], sys.argv[2] + os.path.sep + tail)
        else:
            shutil.copyfile(file_list[ii], sys.argv[2] + os.path.sep + tail)
    shutil.rmtree("decomp")

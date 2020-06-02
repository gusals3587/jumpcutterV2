#external lib

#internal lib
import math
import sys
import time
import os
import subprocess
import argparse
#import gc
from shutil import rmtree
from datetime import timedelta

TEMP_FOLDER = '.TEMP_LONG'

parser = argparse.ArgumentParser()
parser.add_argument("videoFile", help="the path to the video file you want modified.")
# parser.add_argument('-v', '--videoSpeed', type=float, default=1.0,
#     help='the speed that the video plays at.')
parser.add_argument("--silentSpeed", "-s", type=float, default=99999,
    help="the speed that silent frames should be played at.")
parser.add_argument("--silentThreshold", "-t", type=float, default=0.04,
    help="the volume that frames audio needs to surpass to be sounded. It ranges from 0 to 1.")
parser.add_argument("--frameMargin", "-m", type=int, default=4,
    help="tells how many frames on either side of speech should be included.")
args = parser.parse_args()

videoFile = args.videoFile

try:
    os.mkdir(TEMP_FOLDER)
except OSError:
    rmtree(TEMP_FOLDER)
    os.mkdir(TEMP_FOLDER)

#splitting
filename, filetype = os.path.splitext(videoFile)
splitVideo = 'ffmpeg -i "{}" -acodec copy -f segment -segment_time 1800 -vcodec copy -reset_timestamps 1 -map 0 {}/%d{}'.format(
    videoFile, TEMP_FOLDER, filetype
)
subprocess.run(splitVideo, shell=True)

#processing
for files in os.listdir(TEMP_FOLDER):
    videoPath = '{}/{}'.format(TEMP_FOLDER, files)
    subprocess.run(['python3', 'fast_video.py', "-s", str(args.silentSpeed), "-m", str(args.frameMargin), "-t", str(args.silentThreshold), videoPath])
    os.remove(videoPath)

#mergeing
generateFile = "for f in ./{}/*.mp4; do echo \"file '$f'\" >> mylist.txt; done".format(TEMP_FOLDER)
os.system(generateFile)
concatVideo = "ffmpeg -f concat -safe 0 -i mylist.txt -c copy {}_faster.mp4".format(filename)
os.system(concatVideo)
os.remove("mylist.txt")

rmtree(TEMP_FOLDER)
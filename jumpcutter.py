import sys
import os
import subprocess
import argparse
from shutil import rmtree
from fastVideo import fastVideo

TEMP_FOLDER = ".TEMP_LONG"

parser = argparse.ArgumentParser()
parser.add_argument("videoFile", help="the path to the video file you want modified.")
parser.add_argument(
    "-v",
    "--videoSpeed",
    type=float,
    default=1.0,
    help="the speed that the video plays at.",
)
parser.add_argument(
    "--silentSpeed",
    "-s",
    type=float,
    default=99999,
    help="the speed that silent frames should be played at.",
)
parser.add_argument(
    "--silentThreshold",
    "-t",
    type=float,
    default=0.04,
    help="the volume that frames audio needs to surpass to be sounded. It ranges from 0 to 1.",
)
parser.add_argument(
    "--frameMargin",
    "-m",
    type=int,
    default=4,
    help="tells how many frames on either side of speech should be included.",
)
args = parser.parse_args()

videoFile = args.videoFile

try:
    os.mkdir(TEMP_FOLDER)
except OSError:
    rmtree(TEMP_FOLDER)
    os.mkdir(TEMP_FOLDER)

# splitting
filename, filetype = os.path.splitext(videoFile)
splitVideo = 'ffmpeg -i "{}" -acodec copy -f segment -segment_time 1800 -vcodec copy -reset_timestamps 1 -map 0 {}/%d{}'.format(
    videoFile, TEMP_FOLDER, filetype
)
subprocess.call(splitVideo, shell=True)

# processing
for files in os.listdir(TEMP_FOLDER):
    videoPath = "{}/{}".format(TEMP_FOLDER, files)
    fastVideo(
        videoPath,
        args.silentSpeed,
        args.videoSpeed,
        args.silentThreshold,
        args.frameMargin,
    )
    os.remove(videoPath)

# mergeing
generateFile = "for f in ./{}/*.mp4; do echo \"file '$f'\" >> mylist.txt; done".format(
    TEMP_FOLDER
)
subprocess.call(generateFile, shell=True)

concatVideo = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "mylist.txt"]
concatVideo.extend(["-c", "copy", filename + "_faster.mp4"])

subprocess.call(concatVideo)

os.remove("mylist.txt")

outFile = filename + "_faster.mp4"

if not os.path.isfile(outFile):
    raise IOError(f"the file {outFile} was not created")

try:  # should work on Windows
    os.startfile(outFile)
except AttributeError:
    try:  # should work on MacOS and most linux versions
        subprocess.call(["open", outFile])
    except:
        print("could not open output file")

rmtree(TEMP_FOLDER)

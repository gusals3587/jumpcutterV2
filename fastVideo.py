# External libraries
import cv2
import numpy as np
from scipy.io import wavfile
from audiotsm import phasevocoder
from readAudio import ArrReader, ArrWriter

# Internal libraries
import math
import sys
import time
import os
import subprocess
import argparse
from shutil import rmtree
from datetime import timedelta

nFrames = 0

def getAudioChunks(audioData, sampleRate, frameRate, SILENT_THRESHOLD, LOUD_THRESHOLD, FRAME_SPREADAGE):

    def getMaxVolume(s):
        maxv = float(np.max(s))
        minv = float(np.min(s))
        return max(maxv, -minv)

    audioSampleCount = audioData.shape[0]
    maxAudioVolume = getMaxVolume(audioData)

    samplesPerFrame = sampleRate / frameRate
    audioFrameCount = int(math.ceil(audioSampleCount / samplesPerFrame))
    hasLoudAudio = np.zeros((audioFrameCount))

    for i in range(audioFrameCount):
        start = int(i * samplesPerFrame)
        end = min(int((i+1) * samplesPerFrame), audioSampleCount)
        audiochunks = audioData[start:end]
        maxchunksVolume = getMaxVolume(audiochunks) / maxAudioVolume
        if(maxchunksVolume >= LOUD_THRESHOLD):
            hasLoudAudio[i] = 2
        elif(maxchunksVolume >= SILENT_THRESHOLD):
            hasLoudAudio[i] = 1

    chunks = [[0, 0, 0]]
    shouldIncludeFrame = np.zeros((audioFrameCount))
    for i in range(audioFrameCount):
        start = int(max(0, i-FRAME_SPREADAGE))
        end = int(min(audioFrameCount, i+1+FRAME_SPREADAGE))
        shouldIncludeFrame[i] = min(1, np.max(hasLoudAudio[start:end]))

        if (i >= 1 and shouldIncludeFrame[i] != shouldIncludeFrame[i-1]):
            chunks.append([chunks[-1][1], i, shouldIncludeFrame[i-1]])

    chunks.append([chunks[-1][1], audioFrameCount, shouldIncludeFrame[i-1]])
    chunks = chunks[1:]

    return chunks

def fastVideo(videoFile, silentSpeed, videoSpeed, silentThreshold, frameMargin):
    videoFile = videoFile
    silentSpeed = silentSpeed
    videoSpeed = videoSpeed
    silentThreshold = silentThreshold
    frameMargin = frameMargin

    TEMP = ".TEMP"
    FADE_SIZE = 400
    NEW_SPEED = [silentSpeed, videoSpeed]

    cap = cv2.VideoCapture(videoFile)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = round(cap.get(cv2.CAP_PROP_FPS))

    try:
        os.mkdir(TEMP)
    except OSError:
        rmtree(TEMP)
        os.mkdir(TEMP)

    extractAudio = ["ffmpeg", "-i", videoFile, "-ab", "160k", "-ac", "2", "-ar"]
    extractAudio.extend(["44100", "-vn", f"{TEMP}/output.wav", "-nostats", "-loglevel"])
    extractAudio.extend(["0"])

    subprocess.call(extractAudio)

    out = cv2.VideoWriter(TEMP + "/spedup.mp4", fourcc, fps, (width, height))
    sampleRate, audioData = wavfile.read(TEMP + "/output.wav")

    chunks = getAudioChunks(audioData, sampleRate, fps, silentThreshold, 2, frameMargin)

    skipped = 0
    channels = int(audioData.shape[1])

    switchStart = 0

    needChange = False
    preve = None
    endMargin = 0

    y = np.zeros_like(audioData, dtype=np.int16)
    yPointer = 0
    frameBuffer = []

    premask = np.arange(FADE_SIZE) / FADE_SIZE
    mask = np.repeat(premask[:, np.newaxis], 2, axis=1)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cframe = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) # current frame

        # we are rewriting the function so it uses chunks to determine cuts
        state = None
        for chunk in chunks:
            if(cframe >= chunk[0] and cframe <= chunk[1]):
                state = chunk[2]
                break

        if(state is not None):
            if(state == 1):
                out.write(frame)
        else:
            print('error')
            sys.exit()

        # handle audio

        currentTime = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        audioSampleStart = math.floor(currentTime * sampleRate)
        audioSampleStart = math.floor(currentTime * sampleRate)

        audioSampleEnd = audioSampleStart + (sampleRate // fps)

        switchEnd = audioSampleEnd

        audioChunk = audioData[audioSampleStart:audioSampleEnd]

        state = None
        normal = True
        for chunk in chunks:
            if(cframe >= chunk[0] and cframe <= chunk[1]):
                state = chunk[2]
                if(cframe == chunk[1]):
                    normal = False
                break
        if(state == 1):
            if(normal):
                switchStart = switchEnd

                yPointerEnd = yPointer + audioChunk.shape[0]
                y[yPointer : yPointerEnd] = audioChunk
                yPointer = yPointerEnd
            else:
                spedChunk = audioData[switchStart:switchEnd]
                spedupAudio = np.zeros((0,2), dtype=np.int16)
                with ArrReader(spedChunk, channels, sampleRate, 2) as reader:
                    with ArrWriter(spedupAudio, channels, sampleRate, 2) as writer:
                        phasevocoder(reader.channels, speed=silentSpeed).run(reader, writer)
                        spedupAudio = writer.output

                yPointerEnd = yPointer + spedupAudio.shape[0]
                y[yPointer : yPointerEnd] = spedupAudio
                yPointer = yPointerEnd

                switchStart = switchEnd

    # finish audio
    y = y[:yPointer]
    wavfile.write(TEMP+"/spedupAudio.wav", sampleRate, y)

    if not os.path.isfile(TEMP+"/spedupAudio.wav"):
        raise IOError('audio file not created.')

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    first = videoFile[: videoFile.rfind(".")]
    extension = videoFile[videoFile.rfind(".") :]

    outFile = f"{first}_faster{extension}"

    cmd = ["ffmpeg", "-y", "-i", f"{TEMP}/spedup.mp4", "-i"]
    cmd.extend([f"{TEMP}/spedupAudio.wav", "-c:v", "copy", "-c:a", "aac", outFile])
    cmd.extend(["-nostats", "-loglevel", "0"])
    subprocess.call(cmd)

    if not os.path.isfile(outFile):
        raise IOError(f"the file {outFile} was not created")

    rmtree(TEMP)



if(__name__ == '__main__'):
    # for testing purposes
    fastVideo('/Users/wyattblue/media/1m.mp4', 99999, 1, 0.04, 4)

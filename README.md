# jumpcutterV2
Automatically edits videos - Originally inspired by carykh, then inspired by gusals3587, to be later fixed by WyattBlue.

Carykh's video: https://www.youtube.com/watch?v=DQ8orIurGxw

Carykh's program: https://github.com/carykh/jumpcutter

# Windows download
https://github.com/seaty6/jumpcutterV2/releases/latest/download/fast_video.exe
The above is simply the python file compiled with pyinstaller - it should work on Windows without having to install Python, FFMpeg, or any other dependencies. 

# Differences
1. Can no longer specify:
  a. sounded_speed
  b. frame_rate
  c. frame_quality
2. Can't download youtube videos
3. Doesn't take up a large amount of space by splitting up each frame
4. Goes much faster.

# Usage
Windows:
`fast_video.exe {video file name} --silentSpeed {float} --silentThreshold {float}`
Python:
`python3 fast_video.py {video file name} --silentSpeed {float} --silentThreshold {float}`

Using shorts:
`fast_video.exe {video file name} -s {float} -t {float}`

> Note: On Linux and Windows, `python3` doesn't work. Use `python` instead. ALternativly, you could use the executable if on Windows, in the releases tab.
# Heads up
Based on Python3

# Credits:
Thanks to https://github.com/gusals3587/jumpcutterV2 for reworking the code to be much more optimized
Thanks to https://github.com/WyattBlue/jumpcutterV2 for adding back the all but the frame_margin parameter

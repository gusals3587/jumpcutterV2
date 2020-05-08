# jumpcutterV2
automatically edits videos, originally inspired by carykh

original inspiration: https://www.youtube.com/watch?v=DQ8orIurGxw

the program he made: https://github.com/carykh/jumpcutter

I saw some limits to the approach
1. He extracted EVERY frame and put it into a single, giant folder. While that is easier to work with, it require's GBs, maybe even TBs of free storage.
2. There were some syncing issues involved if it worked with long videos.
3. While it was working on the audio, it kept making small, temp audio files that made it very slow.

I decided to solve it, and heavily modified the code so it can fix all those problems.

# Differences
Due to the modifications, you can no longer specify sounded_speed, frame_margin, frame_rate, frame_quality, that is all handled internally. (it also doesn't download youtube videos automatically). I tried to make the code a lot simpler but I'm open to PR request that can still enhance the repo.

PS, if you want sounded speech speedup, I would recommend just speeding up the video on the player.

# Usage
`python3 fast_video.py {video file name} --silentSpeed float --silentThreshold float`

Using shorts
`python3 fast_video.py {video file name} -s float -t float`

> Note: On Linux and Windows, `python3` doesn't work. Use `python` instead.
# heads up
I've only tested this with mp4 file, not sure about other formats.

I also use python3, not planning any backward compatibility.

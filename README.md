# jumpcutterV2
automatically edits videos, originally inspired by carykh

original inspiration: https://www.youtube.com/watch?v=DQ8orIurGxw

the program he made: https://github.com/carykh/jumpcutter

I saw some limits to the approach
1. he extracted EVERY frame and put it into a single, giant folder. While that it is easier to work with, it will require GBs, maybe even TBs of user's storage space (albeit temporary)
2. there were some syncing issues involved if it worked with long videos
3. while it was working on the audio, it kept making small, temp audio files that made it very slow

I decided to solve it, and heavily modified the code so it can fix all those problems

# Differences
due to the modifications, you can no longer specify silent-threshold, sounded_speed, frame_margin, frame_rate, frame_quality, that is all handled internally. (it also doesn't downlaod youtube video automatically). I tried to make the code a lot simpler but I'm open to PR request that can still enhance the repo

PS, if you want sounded speech speedup, I would recommend just speeding up the video on the player

# Usage
`python fast_video.py {video file name} {silent speed(float)}

# heads up
I've only tested this with mp4 file, not sure about other format

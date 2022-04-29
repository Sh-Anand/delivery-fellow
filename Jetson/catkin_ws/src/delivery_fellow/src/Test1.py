#! /usr/bin/python3

import AutoFollow
import Camera
import jetson.utils
import time

af = AutoFollow.AutoFollow()
c = Camera.Camera('/dev/video0', angle=160, ratio=0.5)
# c = Camera.Camera('csi://0', angle=160, ratio=0.4)
# c = Camera.Camera('../media/test-videos/vid-wii-2.mp4', angle=120, ratio=0.5)
af.setCamera(c)
out = jetson.utils.videoOutput()

prev = time.time()
while True:
    res = af.getSteering(debugOut=out)
    # if res is None:
    #     x = y = a = 0
    # else:
    #     ((x,y),a) = res
    # now = time.time()
    # fps = 1/(now-prev)
    # prev = now
    # print('FPS:{:4.1f} x:{:5.3f} y:{:5.3f} a:{:5.3f}'.format(fps, x, y, a))
    
#/usr/bin/python3

import cv2
import jetson.utils
import math
import numpy as np

class Camera:

    def __init__(self, url, angle=110, ratio=1.0):
        self.cam = jetson.utils.videoSource(url)
        self.ang = angle
        self.r = ratio

        self.ha = self.getHfromD(angle)
        self.va = self.getVfromD(angle)
        
        self.cam.Capture()

    def getHfromD(self, ang):
        w = self.getWidth()
        h = self.getHeight()
        return math.degrees(2 * math.atan((w * math.tan(math.radians(ang) / 2.0)) / math.sqrt(w ** 2 + h ** 2)))

    def getVfromD(self, ang):
        w = self.getWidth()
        h = self.getHeight()
        return math.degrees(2 * math.atan((h * math.tan(math.radians(ang) / 2.0)) / math.sqrt(w ** 2 + h ** 2)))

    def setResizeFactor(self, ratio):
        self.r = min(ratio, 1.0)

    def Capture(self):
        img = self.cam.Capture()
        if self.r == 1:
            return img
        img2 = jetson.utils.cudaAllocMapped(width=self.r*img.width, height=self.r*img.height, format=img.format)
        jetson.utils.cudaResize(img, img2)
        return img2

    def getCVFrame(self):
        img = self.Capture()
        return Camera.cudaToNumpy(img)

    def getWidth(self):
        return self.cam.GetWidth() * self.r

    def getHeight(self):
        return self.cam.GetHeight() * self.r
    
    def getCenter(self):
        x = int(self.getWidth()/2)
        y = int(self.getHeight()/2)
        return (x,y)

    @staticmethod
    def cudaToNumpy(img):
        w = img.width
        h = img.height
        img2 = np.ascontiguousarray(jetson.utils.cudaToNumpy(img, w, h, 4), dtype=np.uint8)
        # img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
        return img2

    @staticmethod
    def cudaFromNumpy(img):
        # img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img3 = jetson.utils.cudaFromNumpy(img)
        return img3

    def distanceToCenter(self, fromPos):
        (x, y) = fromPos
        w = self.getWidth()
        h = self.getHeight()
        # CALCULATE ON SCREEN DIFFERENCE
        dx = + (0.5 - x/w)
        dy = - (0.5 - y/h)
        # print('from x:{} y:{} to center of w:{} h:{} is dx{} dy{}'.format(x, y, w, h, dx, dy)) # DEBUG
        return (dx, dy)

    def angleToCenter(self, fromPos):
        (dx, dy) = self.distanceToCenter(fromPos)
        ax = self.ha * dx * 3.14159265 / 180
        ay = self.va * dy * 3.14159265 / 180
        # print('from dx:{} dy:{} angle ax:{} ay:{}'.format(dx,dy,ax,ay)) # DEBUG
        return (ax, ay)

    def getRelativeArea(self, area):
        return 1.0*area/(self.getHeight() * self.getWidth())

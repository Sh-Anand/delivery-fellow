#! /usr/bin/python3

import cv2
import jetson.utils
import jetson.inference
import numpy as np
import time as tm
from pathlib import Path
import Boxtimate
import Camera
import time
# from skimage.util import compare_images
from Constants import *


class AutoFollow:

    # net      the NN used for object detection
    # camera   the active camera
    # prev     the previous detection box with velocity approximate

    def __init__(self):
        self.net = jetson.inference.detectNet(DETECT_MODEL_NAME, threshold=DETECT_MODEL_PROBABILITY)
        self.camera = None

        self.prevBox = None
        self.prevRecheck = None
        self.prevHist = None
        self.prevWorld = None
        self.lastDetectTime = 0

        self.hists = []
        for p in Path('/home/delifelly/delivery-fellow/Jetson/catkin_ws/src/delivery_fellow/media/target').iterdir():
            avg = None # np.zeros(32 * 32).reshape([32, 32])
            count = 0
            for f in p.iterdir():
                count += 1
                img = cv2.imread('/'.join(f.parts))
                if avg is None:
                    avg = AutoFollow.histogram(img, HIST_CREATE_METHOD)
                else:
                    avg += AutoFollow.histogram(img, HIST_CREATE_METHOD)
            avg /= count
            self.hists.append(avg)


    def setCamera(self, cam):
        self.camera = cam
        # RESET PREVIOUS DETECTIONS
        self.prevBox = None
        self.prevHist = None
        self.prevWorld = None

    def getSteering(self, batch=0, debugOut=None):
        # DETECT OBJECTS
        img = self.camera.Capture()
        imgNp = Camera.Camera.cudaToNumpy(img)
        worldHist_new = AutoFollow.histogram(imgNp, HIST_CREATE_METHOD)
        if self.prevWorld is None:
            self.prevWorld = worldHist_new * WORLD_HIST_MULTIP
        else:
            self.prevWorld = self.prevWorld * (1-NEXT_WORLD_RATIO) + worldHist_new * NEXT_WORLD_RATIO
            self.prevWorld *= WORLD_HIST_MULTIP / np.sum(self.prevWorld)
        now = tm.time()
        detections = self.net.Detect(img, overlay='none')
        # print(len(detections))
        
        # FILTER PEOPLE
        ppl = []
        for d in detections:
            # print(d.ClassID, end=", ")
            # continue
            if d.ClassID == DETECT_MODEL_PERSON_ID and self.camera.getRelativeArea(d.Area) > THRESHOLD_BBOX_MIN_SIZE :
                ppl.append(d)
        detections = ppl


        if debugOut is not None:
            imgPr = Camera.Camera.cudaToNumpy(img)
            for d in detections:
                cv2.rectangle(imgPr, (int(d.Left), int(d.Top)), (int(d.Right), int(d.Bottom)), (0, 0, 0), 2)
                cv2.putText(imgPr, str(d.ClassID)+' - '+str(d.Confidence)+'%', (int(d.Left), int(d.Bottom)), 0, 1, 128)

        # MATCH TO PREVIOUS but not longer than timeout
        if self.prevBox is not None and now <= self.prevRecheck+TIMEOUT_BEFORE_RECHECK:
            if len(detections) > 0:
                rankBB = np.zeros(len(detections))
                for i, d in enumerate(detections):
                    rankBB[i] = self.prevBox.getInterOverUnion(d, now)
                maxBBs = []
                for i,r in enumerate(rankBB):
                    if r > THRESHOLD_BBOX_SIMILARITY:
                        maxBBs.append(i)
                
                hists = {}
                if len(maxBBs) == 1:
                    maxId = maxBBs[0]
                    imgCut = AutoFollow.cutout(imgNp, detections[maxId])
                    hists[maxId] = np.clip(AutoFollow.histogram(imgCut, HIST_CREATE_METHOD) - self.prevWorld, 0, 1e10)     
                else:
                    rankHS = np.zeros(len(detections))
                    hists = {}
                    for i in maxBBs:
                        imgCut = AutoFollow.cutout(imgNp, detections[i])
                        hists[i] = np.clip(AutoFollow.histogram(imgCut, HIST_CREATE_METHOD) - self.prevWorld, 0, 1e10)
                        rankHS[i] = AutoFollow.compareHistograms(self.prevHist, hists[i], HIST_COMPARE_METHOD)                                    
                    maxId = np.argmax(rankHS)

                    if rankHS[maxId] < THRESHOLD_HIST_SIMILARITY_NEXT:
                        maxId = -1

                if maxId != -1:
                    hist = hists[maxId]
                    (x1, y1) = self.prevBox.getCenter()
                    (x2, y2) = detections[maxId].Center
                    vx = self.prevBox.vel[0]*(1-NEXT_VEL_RATIO) + (x2 - x1)/(now - self.prevBox.time)*(NEXT_VEL_RATIO)
                    vy = self.prevBox.vel[1]*(1-NEXT_VEL_RATIO) + (y2 - y1)/(now - self.prevBox.time)*(NEXT_VEL_RATIO)
                    self.prevBox = Boxtimate.Boxtimate(detections[maxId], (vx, vy), now)
                    self.lastDetectTime = now
                    imgCut = AutoFollow.cutout(imgNp, detections[maxId])
                    if self.prevHist is not None:
                        self.prevHist = self.prevHist*(1-NEXT_HIST_RATIO) + hist*NEXT_HIST_RATIO
                        self.prevHist /= np.sum(self.prevHist)
                    else:
                        self.prevHist = hist
                    if debugOut is not None:
                        cv2.arrowedLine(imgPr, self.camera.getCenter(), (int(x2), int(y2)), (0, 0, 255), 10) # blue
                        cv2.arrowedLine(imgPr, (int(x2), int(y2)), (int(x2+vx), int(y2+vy)), (128, 128, 128), 5)
                        debugOut.Render(Camera.Camera.cudaFromNumpy(imgPr))
                    return (self.camera.angleToCenter((x2, y2)), self.camera.getRelativeArea(detections[maxId].Height))

            # NO CONFIDENT DETECTION -> approximate with previous untill timeout

            if now - self.prevBox.time < TIMEOUT_BLIND_GUESS:  # threshold on timeout in seconds
                (x, y) = self.prevBox.getNextCenter(now)
                if debugOut is not None:
                    cv2.arrowedLine(imgPr, self.camera.getCenter(), (int(x), int(y)), (0, 255, 0), 10) # green
                    cv2.arrowedLine(imgPr, (int(x), int(y)), (int(x+self.prevBox.vel[0]), int(y+self.prevBox.vel[1])), (128, 128, 128), 5)
                    debugOut.Render(Camera.Camera.cudaFromNumpy(imgPr))
                (retX, retY) = self.camera.angleToCenter((x, y))
                retX *= MULTIP_BLIND_GUESS
                retY *= MULTIP_BLIND_GUESS
                return ((retX, retY), self.camera.getRelativeArea(self.prevBox.getHeight()))

            # TIMEOUT

        # NONE OR WEAK PREVIOUS MATCH

        if len(detections)>0:

            # RANK BY HISTOGRAMS
            hists = []
            for d in detections:
                    imgCut = AutoFollow.cutout(imgNp, d)
                    hists.append(np.clip(AutoFollow.histogram(imgCut, HIST_CREATE_METHOD) - self.prevWorld, 0, 1e10))
            rank = []
            if self.prevHist is None:
                #print('first')
                for h in hists:
                    bestScore = 1e100
                    for hist2 in self.hists :
                        score = AutoFollow.compareHistograms(h, hist2, HIST_COMPARE_METHOD)
                        bestScore = min(bestScore, score)
                    rank.append(bestScore)
                #print(rank)
            else:
                for h in hists:
                    rank.append(AutoFollow.compareHistograms(h, self.prevHist, HIST_COMPARE_METHOD))

            maxId = np.argmax(rank)

            #print('rank\n',rank)

            if rank[maxId] > THRESHOLD_HIST_SIMILARITY_NEW or self.lastDetectTime + TIMEOUT_NEW_PERSON < now: # TODO when timeout new person,choose from the initial clothes
                self.prevBox = Boxtimate.Boxtimate(detections[maxId], (0, 0), now)
                if self.prevHist is not None:
                    self.prevHist = self.prevHist*(1-NEXT_HIST_RATIO) + hists[maxId]*NEXT_HIST_RATIO
                    self.prevHist /= np.sum(self.prevHist)
                else:
                    self.prevHist = hists[maxId]
                self.prevRecheck = now
                self.lastDetectTime = now
                if debugOut is not None:
                    x = int(detections[maxId].Center[0])
                    y = int(detections[maxId].Center[1])
                    cv2.arrowedLine(imgPr, self.camera.getCenter(), (x,y), (255, 0, 0), 10) # red
                    cv2.arrowedLine(imgPr, (int(x), int(y)), (int(x+self.prevBox.vel[0]), int(y+self.prevBox.vel[1])), (128, 128, 128), 5)
                    debugOut.Render(Camera.Camera.cudaFromNumpy(imgPr))
                return (self.camera.angleToCenter(detections[maxId].Center), self.camera.getRelativeArea(detections[maxId].Height))

        # NOTHING FOUND WITH HIGH ENOUGH CONFIDENCE
        if debugOut is not None:
            debugOut.Render(Camera.Camera.cudaFromNumpy(imgPr))
        return None

    @staticmethod
    def histogram(img, method=1):
        if method == 1:
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([img2], [0,1], None, [32,32], [0,256,0,256])
            flat = hist.flatten()
            flat /= np.sum(flat)
            return np.array(flat, dtype=np.float32)
        if method == 2:
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([img2], [0,1,2], None, [32,32,32], [0,256,0,256,0,256])
            flat = hist.flatten()
            flat /= np.sum(flat)
            return np.array(flat, dtype=np.float32)
        if method == 3:
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([img2], [0,1], None, [128,128], [0,256,0,256])
            flat = hist.flatten()
            flat /= np.sum(flat)
            return np.array(flat, dtype=np.float32)
        else:
            return AutoFollow.histogram(img, 1)
        # else: # default to method == 0
        #     img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #     hist = cv2.calcHist([img2], [0,1], None, [32,32], [0, 250, 0, 250])
        #     return hist / (img.shape[0]*img.shape[1])

    @staticmethod
    def compareHistograms(a, b, method=1):
        if a is None or b is None:
            return 0.0;
        elif method == 1:
            return cv2.compareHist(a, b, cv2.HISTCMP_CORREL)
        elif method == 2:
            return -1 * cv2.compareHist(a, b, cv2.HISTCMP_CHISQR)
        elif method == 3:
            return cv2.compareHist(a, b, cv2.HISTCMP_INTERSECT)
        elif method == 4:
            return -1 * cv2.compareHist(a, b, cv2.HISTCMP_BHATTACHARYYA)
        elif method == 5:
            return -1 * cv2.compareHist(a, b, cv2.HISTCMP_CHISQR_ALT)
        elif method == 6:
            return cv2.compareHist(a, b, cv2.HISTCMP_KL_DIV)
        else:
            return AutoFollow.compareHistograms(a, b, 1)
        # else: # default to method == 0
        #     return 1 - np.sum(compare_images(a, b, method='diff'))

    @staticmethod
    def cutout(img, d):
        T = int( d.Center[1]-d.Height*(0.5-HIST_CROP_TOP))  # 10% crop top
        B = int( d.Center[1]+d.Height*(0.5-HIST_CROP_BOTTOM))  # 50% crop botton
        L = int( d.Center[0]-d.Width *(0.5-HIST_CROP_LEFT))  # 10% crop left
        R = int( d.Center[0]+d.Width *(0.5-HIST_CROP_RIGHT))  # 10% crom right
        # cv2.imwrite('cuts/'+str(time.time())+'.jpg', img[T:B, L:R])
        # time.sleep(0.2)
        return np.ascontiguousarray(img[T:B, L:R])

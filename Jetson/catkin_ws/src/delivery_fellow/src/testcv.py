#/usr/bin/python3

import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.util import compare_images

def compare(a, b):
    return np.sum(compare_images(a, b, method='diff'))

def histogram(img):
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([img2], [0,1], None, [32,32], [0, 250, 0, 250])
    return hist / (img.shape[0]*img.shape[1])

avg = np.zeros(32*32).reshape([32,32])
hists = []
for i in range(8):
    img = cv2.imread('../media/target/sweater/{}.jpg'.format(i))
    hist = histogram(img)
    hists.append(hist)
    # norm = cv2.normalize(hist, 0, 255, cv2.NORM_L1)
    avg += hist

avg /= 8

# for i, h in enumerate(hists):
#     print(i, compare(avg, h))


for n in range(8):
    img = cv2.imread('../media/test-imgs/sweater/'+str(n)+'.jpeg')
    factor = 0.25
    res = cv2.resize(img, (int(img.shape[1]*factor), int(img.shape[0]*factor)))

    w = res.shape[1]
    h = res.shape[0]
    countx = 9
    county = 12
    overlayx = 3
    overlayy = 4
    stepx = 1.0 / countx
    stepy = 1.0 / county
    maxx = 0
    maxy = 0
    scores = np.zeros((countx-overlayx)*(county-overlayy)).reshape([(countx-overlayx),(county-overlayy)])
    for i in range(countx-overlayx):
        for j in range(county-overlayy):
            L = int(w * stepx * i)
            R = int(w * stepx * (i+1+overlayx))
            U = int(h * stepy * j)
            D = int(h * stepy * (j+1+overlayy))
            part = res[U:D,L:R]
            hist = histogram(part)
            scores[i][j] = compare(avg, hist)
            if scores[i][j] < scores[maxx][maxy]:
                maxx = i
                maxy = j

    print(n, scores[maxx][maxy])

    out = cv2.rectangle(res, (int(w * stepx * maxx),int(h * stepy * maxy)), (int(w * stepx * (maxx+1+overlayx)),int(h * stepy * (maxy+1+overlayy))), (255,0,0), 2)
    cv2.imshow('box', out)
    cv2.waitKey(1)

# plt.imshow(scores)
# plt.show()



# plt.imshow(np.log(avg+1))
# plt.show()



    # factor = 0.3
    # res = cv2.resize(img, (int(img.shape[1]*factor), int(img.shape[0]*factor)))
    # bw  = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    
    # lower = np.array([100, 50, 50])
    # upper = np.array([110, 110, 220])

    # mask = cv2.inRange(hsv, lower, upper)

    # fin  = cv2.bitwise_and(res, res, mask=mask)

    # contours,hierarchy = cv2.findContours(mask*255, 1, 2)

    # n = []
    # for cn in contours:
    #     n.append(cv2.contourArea(cn))
    # ids = np.argsort(n)
    # cnt = contours[ids[-1]]

    # for i in range(10):
    #     cv2.drawContours(res,contours,ids[-i],(np.random.randint(256), np.random.randint(256), np.random.randint(256)),2)

    # cv2.imshow('image', res)
    # cv2.waitKey(0)
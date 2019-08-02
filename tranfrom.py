import cv2
import numpy as np
import math

def order_point(conts) :
    rect = np.zeros((4, 2), dtype="float32")
    s = conts.sum(axis=1)
    rect[0] = conts[np.argmin(s)]
    rect[2] = conts[np.argmax(s)]


    diff = np.diff(conts, axis=1)
    rect[1] = conts[np.argmin(diff)]
    rect[3] = conts[np.argmax(diff)]

    return rect

def four_point_transform(image,point) :
    rect=order_point(point)
    #print(rect)
    [a,b,c,d]=rect
    #print(a,b,c,d)
    widthA=math.sqrt(((a[0]-b[0])**2+(a[1]-b[1])**2))
    widthB=math.sqrt(((c[0]-d[0])**2+(c[1]-d[1])**2))
    maxwidth = max(int(widthA),int(widthB))

    hightA=math.sqrt(((a[0]-d[0])**2+(a[1]-d[1])**2))
    hightB=math.sqrt(((b[0]-c[0])**2+(b[1]-c[1])**2))
    maxhight=max(int(hightA),int(hightB))

    dst = np.array([[0, 0],[maxwidth - 1, 0],[maxwidth- 1, maxhight - 1],[0, maxhight - 1]], dtype="float32")

    #print(maxhight,maxwidth)
    M=cv2.getPerspectiveTransform(rect,dst)
    wapper=cv2.warpPerspective(image,M,(maxwidth,maxhight))

    return wapper

# k=np.array([[82,124],[77,630],[471,621],[462,128]])
#
# img=cv2.imread("anh\\anh3.jpg")
#
# cv2.imshow("a",four_point_transform(img,k))
#
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()


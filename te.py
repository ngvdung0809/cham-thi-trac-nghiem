import cv2
import numpy
#img=cv2.imread("anh\\hoasen.jpg",1)



# dieu chinh do sang do tuong phan
# for i in range(387) :
#     for j in range(580) :
#         for k in range(3) :
#             src[i,j,k]=2*img[i,j,k] + 30

#gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# blud=cv2.GaussianBlur(img,(5,5),0)
# cv2.imshow("blud",blud)
#
# # cân bằng ảnh màu
# src=cv2.cvtColor(blud,cv2.COLOR_BGR2HSV) # chuyen sang kênh mau hsv
# chanel=cv2.split(src) # cat ra ba gia trị
# print(chanel)
# chanel[2]=cv2.equalizeHist(chanel[2]) # cân bằng độ giá trị v
# cv2.merge(chanel,src) ## trộn ảnh
# disp=cv2.cvtColor(src,cv2.COLOR_HSV2BGR)
# cv2.imshow("disp",disp)
# cv2.imshow('img',img)



#chuyen đổi các không gian màu
#src=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)



#nhi phan hoa anh
#thresh = cv2.threshold(src,0,255,cv2.THRESH_BINARY_INV)[1]

#flag=[i for i in dir(cv2) if i.startswith("COLOR_")]
#print(flag)
#cv2.imshow("src",src)



#cân bằng ảnh xám
# src=cv2.equalizeHist(img)
# cv2.imshow("src",src)
# cv2.imshow("img",img)


# mở video
cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame',frame)


    if cv2.waitKey(1) == 27:
        break


cap.release()
cv2.destroyAllWindows()
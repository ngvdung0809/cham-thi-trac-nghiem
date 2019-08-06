import cv2
import numpy as np
import imutils
from imutils import contours
import tranfrom as trf

def show(a) :
    n = len((a))

    # xác định các đường tròn trong bài thi
    for i in range(n):
        for k in range(len(a[i]) - 1):
            cv2.line(exp, tuple(a[i][k][0]), tuple(a[i][k + 1][0]), (0, 60, 255), 2)
    for i in range(n):
        l = len(a[i])
        cv2.line(exp, tuple(a[i][0][0]), tuple(a[i][l - 1][0]), (0, 60, 255), 2)  # chưa vẽ đc toàn bộ hình tròn.

img=cv2.imread("anh\\anh5.jpg",1)
cv2.imshow("nguon",img)


cpy=img.copy()

ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

# tìm biên ảnh bằng hàm canny
#lưu ý ảnh phải xác định các cạnh của bài thi, 4 đỉnh rõ ràng
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0) # lọc gauss để xóa nhiễu
#cv2.imshow("bl",blurred)
edged = cv2.Canny(blurred, 75, 200) #dùng hàm canny để tìm cạnh của bài thi
#cv2.imshow("edge",edged) # hien thi canny cua bai thi

#tìm đường nét với các tham số là chế độ tìm đường bao và phương pháp xấp xỉ đường bao

conts=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
conts=conts[0] if imutils.is_cv2() else conts[1]
doccnt=None
#print(conts)

# đảm bảo là tìm thấy được đường viền
if len(conts)>0 :
    conts=sorted(conts, key=cv2.contourArea, reverse=True) # sắp xếp theo thứ tự giảm dần
    #print(conts)
    #lặp trên các đường viền sau khi được sắp xếp
    for c in conts :
        #print(c)
        peri=cv2.arcLength(c,True)
        #print(peri)
        approx=cv2.approxPolyDP(c,0.02*peri, True)
        #print(approx)
        # giả sử đường bao có 4 điểm coi như đã tìm thấy bài kiểm tra
        if len(approx)==4 :
            doccnt=approx
            break
#print(doccnt)
# vẽ 4 đỉnh của bài thi
#src=cv2.drawContours(img, doccnt, -1,255, 3)
#cv2.imshow("src",src)
#
#vẽ 4 cạnh của bài thi
arc=cv2.line(cpy,tuple(doccnt[0][0]),tuple(doccnt[1][0]),(0,255,255),3)
arc=cv2.line(cpy,tuple(doccnt[0][0]),tuple(doccnt[3][0]),(0,255,255),3)
arc=cv2.line(cpy,tuple(doccnt[1][0]),tuple(doccnt[2][0]),(0,255,255),3)
arc=cv2.line(cpy,tuple(doccnt[2][0]),tuple(doccnt[3][0]),(0,255,255),3)
#cv2.imshow("arc",arc)

# doccnt chinh la 4 goc cua bai thi kiem tra

#print(doccnt)

# tìm ra bai thi của thí sinh, cắt hình mới
paper = trf.four_point_transform(img, doccnt.reshape(4, 2))   # cắt ảnh bìa thi bằng ảnh gốc
warped = trf.four_point_transform(gray, doccnt.reshape(4, 2)) # cắt bài thi với ảnh xám
exp =  trf.four_point_transform(img, doccnt.reshape(4, 2))
#cv2.imshow('paper',paper)
# cv2.imshow('gr',warped)

# BẮT ĐẦU ĐỌC TỪ ĐÂY!!!!!!

#nhi phan hoa anh
thresh=cv2.threshold(warped,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] # tim hieu nhi phan hoa anh.
#cv2.imshow("thresh",thresh)

cnts=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=cnts[0] if imutils.is_cv2() else cnts[1]
Questioncnts=[]
for c in cnts:
    (x,y,w,h)=cv2.boundingRect(c)
    #print(x,y,w,h)
    ar=w/float(h)
    if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1 :
        Questioncnts.append(c)
#print(len(Questioncnts))

show(Questioncnts)
#cv2.imshow("example",exp)
# thresh.shape: lấy ra số pixel có trong khung hình.

Questioncnts=contours.sort_contours(Questioncnts,"top-to-bottom")[0]
# for i in Questioncnts:
#     (m,n,b,v)=cv2.boundingRect(i)
#     print(m,n,b,v)
#print(Questioncnts)
correct=0
count=0
for (q,i) in enumerate(np.arange(0,len(Questioncnts),5)):
    cntt=contours.sort_contours(Questioncnts[i:i+5])[0]
    #print(cntt)
    bubble=[-1,-1]
    for(j,c) in enumerate(cntt) :
        mask=np.zeros(thresh.shape,dtype="uint8")
        cv2.drawContours(mask,[c],-1,255,-1)
        mask=cv2.bitwise_and(thresh,thresh,mask=mask)
        total=cv2.countNonZero(mask)
        # print(total)
        # tim so dap an khoanh
        if total >600 :
            bubble=[total,j]
            count +=1

    color = (0, 0, 255)
    k = ANSWER_KEY[q]

    #print(bubble)
    #print(count)
    # kiem tra dap an dung
    # kiem tra dap an xem co khoanh nhieu hon 1 dap an hay k

    if count ==1:
        if k == bubble[1]:
            color = (0, 255, 0)
            correct += 1
    count =0

    # ve hinh tron quannh dap an dung, dung thi xanh, sai thi do
    #print(color)
    cv2.drawContours(paper, [cntt[k]], -1, color, 3)
# so dap an dung la
print("So cau dung la:",correct,"/5")
cv2.imshow("Exam", paper)

correct=correct/5*10
print("Diem la:",correct)

cv2.waitKey(0)
cv2.destroyAllWindows()




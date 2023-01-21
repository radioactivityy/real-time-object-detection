import cv2
import numpy as np
def nothing(x):
    # operasyon için
    pass

cap = cv2.VideoCapture(1) # 2. kamera için

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H","Trackbars", 0,180,nothing)
cv2.createTrackbar("L-S","Trackbars", 153,255,nothing)
cv2.createTrackbar("L-V","Trackbars", 125,255,nothing)
cv2.createTrackbar("U-H","Trackbars", 180,180,nothing)
cv2.createTrackbar("U-S","Trackbars", 255,255,nothing)
cv2.createTrackbar("U-H","Trackbars", 243,255,nothing)

while True:
    _, frame= cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H","Trackbars")
    l_s = cv2.getTrackbarPos("L-S","Trackbars")
    l_v = cv2.getTrackbarPos("L-V","Trackbars")
    u_h = cv2.getTrackbarPos("U-H","Trackbars")
    u_s = cv2.getTrackbarPos("U-S","Trackbars")
    u_h = cv2.getTrackbarPos("U-H","Trackbars")

    font = cv2.FONT_HERSHEY_COMPLEX


    lower_red = np.array([l_h ,l_s,l_v])
    upper_red = np.array ([u_h, u_s,u_h])

    mask=cv2.inRange(hsv,lower_red,upper_red)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode (mask,kernel) # konturun çevresindeki bozulmaları kaldırmak için

    # Kontur tespiti
    contours,hierachy = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Kontur çizimi
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
        x= approx.ravel()[0]
        y= approx.ravel()[1]

        if area > 400: #gürültüyü azalttım

            cv2.drawContours(frame,[approx],0,(0,0,0),5)
            if 10< len(approx) <20:
                cv2.putText(frame,"Daire", (x,y), font,1,(0,0,0))

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
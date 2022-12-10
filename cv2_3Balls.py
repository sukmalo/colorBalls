import cv2
import numpy as np

cv2. namedWindow('Image', cv2.WINDOW_FULLSCREEN)
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) #установка экспозиции
cam.set(cv2.CAP_PROP_EXPOSURE, -2)
cam.set(cv2.CAP_PROP_AUTO_WB, 0)

#green = 58-62 140-150 100-130
lower1 = np.array([50, 90, 80])
upper1 = np.array([70, 168, 155])

#orange 3 160-180 220-250
lower2 = np.array([0, 140, 200])
upper2 = np.array([10, 190, 260])

#blue 100-110 200-220 120-180
lower3 = np.array([95, 190, 110])
upper3 = np.array([120, 230, 190])

pixel = None

while cam.isOpened():
    _, frame = cam.read()
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)
    mask3 = cv2.inRange(hsv, lower3, upper3)            
    
    conturs1, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conturs2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conturs3, _ = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(conturs1) > 0:
        c = max(conturs1, key = cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > 20:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 0)
            pixel = 'Green'
    if len(conturs2) > 0:
        c = max(conturs2, key = cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > 20:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 0)
            pixel = 'Orange'
            
    if len(conturs3) > 0:
        c = max(conturs3, key = cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > 20:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 0)
            pixel = 'Blue'
    
    cv2.putText(frame, f"Ball is {pixel}", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 0))
    cv2.imshow("Image", frame)
    pixel = None
    key = cv2.waitKey(50)
    if key == ord('q'): #выключить
        break
    
    
cv2.destroyAllWindows()
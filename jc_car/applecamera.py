import cv2
import time

cap = cv2.VideoCapture(0)

i = 1

while(i < 50):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    filen = 'image_B_' + str(i) + '.jpg'
    out = cv2.imwrite(filen, frame)
    time.sleep(1)
    i = i + 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

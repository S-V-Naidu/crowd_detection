from numba import jit, cuda
import numpy as np
import cv2
import threading
#from pycuda import driver
from queue import Queue
  
cap = cv2.VideoCapture('rtsp://admin:Unidad123@192.168.2.103/udp/1')
ret , frame = cap.read()

#@jit(target_backend='cuda')                        
def frame_show():
    global cap
    global frame
    color = (255, 128, 0)
    
    while True:
        ret, frame = cap.read()
      

@jit(target_backend='cuda')   #, forceobj=True) 
def detection(img):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    color = (255, 128, 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    print(faces)
    print('No. of faces detected: ', len(faces))
    i=0
    for (x, y, w, h) in faces:
        i+=1
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(img, f'{i}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.25, color, 2, cv2.LINE_AA)
    cv2.imshow('Crowd count!!', img)
    

t1 = threading.Thread(target=frame_show, args=())
t1.start()
#while True:
#    detection(frame)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#            break

t1.join()
# Release the video capture and close any open windows
cap.release()
cv2.destroyAllWindows()
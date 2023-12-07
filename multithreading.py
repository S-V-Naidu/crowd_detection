#from numba import jit, cuda
import numpy as np
import cv2
import threading
from queue import Queue
  
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture('rtsp://admin:Unidad123@192.168.2.109/udp/1')
#cap = cv2.VideoCapture(0)
ret , frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
# function optimized to run on gpu 

#@jit(target_backend='cuda')                        
def frame_show():
    global cap
    global frame
    global faces
    color = (255, 128, 0)
    
    while True:
        ret, frame = cap.read()
        try:
            print(faces)
            i=0
            for (x, y, w, h) in faces:
                i+=1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(frame, f'{i}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.25, color, 2, cv2.LINE_AA)  
        except Exception as e:
            print('ERROR: ',e)
        cv2.imshow('Crowd count!!', frame)
        # Exit the loop if 'q' is pressed    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the video capture and close any open windows
    cap.release()
    cv2.destroyAllWindows()

#@jit(target_backend='cuda', forceobj=True) 
def detection():
    global frame
    global faces
    global x,y,h,w
    color = (255, 128, 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # loop over the detected faces
    print('No. of faces detected: ', len(faces))
    #i=0
    #for (x, y, w, h) in faces:
    #    i+=1
    #    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
    #    cv2.putText(frame, f'{i}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.25, color, 2, cv2.LINE_AA)
    #cv2.imshow('Crowd count!!', frame)


t1 = threading.Thread(target=frame_show, args=())
t1.start()
while True:
    detection()

t1.join()

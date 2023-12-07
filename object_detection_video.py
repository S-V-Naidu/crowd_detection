import numpy as np
import cv2
import datetime
import threading
from imutils.video import videostream

from queue import Queue

flag = 0 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video_cap = cv2.VideoCapture('rtsp://admin:Unidad123@192.168.2.44/udp/1')
video_cap.set(cv2.CAP_PROP_FPS, 25)
success, frame = video_cap.read()

# grab the width and the height of the video stream
frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# path to the weights and model files
weights = "ssd_mobilenet/frozen_inference_graph.pb"
model = "ssd_mobilenet/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
# load the MobileNet SSD model trained  on the COCO dataset
net = cv2.dnn.readNetFromTensorflow(weights, model)
gen1 = "models/gender_deploy.prototxt"
gen2 = "models/gender_net.caffemodel"
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
gender = ''
gen = cv2.dnn.readNet(gen2, gen1)

# create a blob from the frame
blob = cv2.dnn.blobFromImage(
    frame, 1.0/127.5, (320, 320), [127.5, 127.5, 127.5])
# pass the blog through our network and get the output predictions
net.setInput(blob)
output = net.forward() # shape: (1, 1, 100, 7)

def frame_show():
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(len(class_names), 3))
    global video_cap
    global frame
    global output
    global flag
    global gender
    while flag!=1:
        success, frame = video_cap.read()
        h = frame.shape[0]
        w = frame.shape[1]

        
        # loop over the number of detected objects
        for detection in output[0, 0, :, :]: # output[0, 0, :, :] has a shape of: (100, 7)
            if detection[2] < 0.5:
                continue

            # extract the ID of the detected object to get
            # its name and the color associated with it
            class_id = int(detection[1])
            label = class_names[class_id - 1].upper()
            color = colors[class_id]
            B, G, R = int(color[0]), int(color[1]), int(color[2])
            # perform element-wise multiplication to get
            # the (x, y) coordinates of the bounding box
            box = [int(a * b) for a, b in zip(detection[3:7], [w, h, w, h])]
            box = tuple(box)
            # draw the bounding box of the object
            if label == 'PERSON':
                cv2.rectangle(frame, box[:2], box[2:], (B, G, R), thickness=2)

                # draw the name of the predicted object along with the probability
                if gender != '':
                    text = f"{gender} {detection[2] * 100:.2f}%"
                    gender = ''
                else:
                    text = f"{label} {detection[2] * 100:.2f}%"
                cv2.putText(frame, text, (box[0], box[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Output", frame)
        if cv2.waitKey(10) == ord("q"):
            break

    # release the video capture, video writer, and close all windows
    video_cap.release()
    #writer.release()
    cv2.destroyAllWindows()

def personDetection():
    global frame
    global output
    global net
    global flag
    while flag!=1:
        # create a blob from the frame
        blob = cv2.dnn.blobFromImage(
           frame, 1.0/127.5, (320, 320), [127.5, 127.5, 127.5])
        # pass the blog through our network and get the output predictions
        net.setInput(blob)
        output = net.forward() # shape: (1, 1, 100, 7)

def genderDetection():
    global frame
    global faces
    global gender
    global gen
    global flag
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    lg = ['Male', 'Female']
    color = (255, 128, 0)
    while flag!=1:
        for (x, y, w, h) in faces:
            gen = cv2.dnn.readNet(gen2, gen1)
            face = frame[y:y + h+10, x:x + w+10]
            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            gen.setInput(blob)
            pred1 = gen.forward()
            gender = lg[pred1[0].argmax()]
            print(gender)

def faceDetection():
    global frame
    global faces
    global flag
    color = (255, 128, 0)
    while flag!=1:
        image = cv2.resize(frame, (720, 640))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)



# load the class labels the model was trained on
class_names = []
with open("ssd_mobilenet/coco_names.txt", "r") as f:
    class_names = f.read().strip().split("\n")

t1 = threading.Thread(target=personDetection, args=())
t2 = threading.Thread(target=genderDetection, args=())
t3 = threading.Thread(target=faceDetection, args=())
t1.start()
t2.start()
t3.start()

frame_show()

flag=1
t1.join()
t2.join()
t3.join()

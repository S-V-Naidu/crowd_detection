import numpy as np
import cv2
import datetime
import threading
import time
import socket, pickle,struct, imutils
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import base64
from queue import Queue

flag = 0 
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

# create a blob from the frame
blob = cv2.dnn.blobFromImage(
    frame, 1.0/127.5, (320, 320), [127.5, 127.5, 127.5])
# pass the blog through our network and get the output predictions
net.setInput(blob)
output = net.forward() # shape: (1, 1, 100, 7)
reading = 0

def frame_show():
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(len(class_names), 3))
    global frame
    global reading
    global output
    while flag!=1:
        success, frame = video_cap.read()
        h = frame.shape[0]
        w = frame.shape[1]

        count=0
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
                text = f"{label} {detection[2] * 100:.2f}%"
                cv2.putText(frame, text, (box[0], box[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                count+=1
        reading = count
        
        #cv2.imshow("Output", frame)
        if cv2.waitKey(10) == ord("q"):
            break

    # release the video capture, video writer, and close all windows
    video_cap.release()
    #writer.release()
    cv2.destroyAllWindows()

def personDetection():
    global output
    global net
    while flag!=1:
        # create a blob from the frame
        blob = cv2.dnn.blobFromImage(
           frame, 1.0/127.5, (320, 320), [127.5, 127.5, 127.5])
        # pass the blog through our network and get the output predictions
        net.setInput(blob)
        output = net.forward() # shape: (1, 1, 100, 7)

# load the class labels the model was trained on
class_names = []
with open("ssd_mobilenet/coco_names.txt", "r") as f:
    class_names = f.read().strip().split("\n")

t1 = threading.Thread(target=personDetection, args=())
t2 = threading.Thread(target=frame_show, args=())
t1.start()
t2.start()

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:8002",
    "http://192.168.2.126:8002",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def video_stream(websocket: WebSocket):
    while True:
        # Encode the frame as JPEG
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = base64.b64encode(buffer).decode("utf-8")

        # Send the frame to the client
        await websocket.send_text(frame_bytes)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await video_stream(websocket)



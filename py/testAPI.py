import threading
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
import websockets
import os
from starlette.datastructures import FormData
from typing import Generator, List
import uvicorn
from queue import Queue
import asyncio
import ast


# path to the weights and model files
weights = "ssd_mobilenet/frozen_inference_graph.pb"
model = "ssd_mobilenet/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
# load the MobileNet SSD model trained  on the COCO dataset
net = cv2.dnn.readNetFromTensorflow(weights, model)

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

reading = 1
stop=0


def detect():
    global reading
    global cap
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(len(class_names), 3))
    while True:
        ret , frame = cap.read()
        try:
            count = 0
            # create a blob from the frame
            blob = cv2.dnn.blobFromImage(
                frame, 1.0/127.5, (320, 320), [127.5, 127.5, 127.5])
            # pass the blog through our network and get the output predictions
            net.setInput(blob)
            output = net.forward() # shape: (1, 1, 100, 7)
            for detection in output[0, 0, :, :]: # output[0, 0, :, :] has a shape of: (100, 7)
                if detection[2] < 0.5:
                    continue

                # extract the ID of the detected object to get
                # its name and the color associated with it
                class_id = int(detection[1])
                label = class_names[class_id - 1].upper()
                if label == 'PERSON':
                    count+=1
            reading = count
            if cv2.waitKey(10) == ord("q"):
                break
        except Exception as e:
            #print("ERROR: - ",e)
            #print("No frame read")
            continue

cap = cv2.VideoCapture('http://192.168.2.126:8080/')
class_names = []
with open("ssd_mobilenet/coco_names.txt", "r") as f:
    class_names = f.read().strip().split("\n")

t1 = threading.Thread(target=detect, args=())
t1.start()
flag = 0

def sleep(t):
    for i in range(t):
        continue


@app.websocket("/ws")
async def send_value(websocket:WebSocket): 
    await websocket.accept()

    while flag != -1:
        await websocket.send_text(str(reading))
        print(reading)
    #await asyncio.sleep(1)
        sleep(2)
@app.post("/cmd")
async def read_cmd(action: str, value:str):
    #data = ast.literal_eval(cmd)
    global flag
    data = {'action':action, 'value':value}
    if action == "save":
        saveImages(data)
    elif action == "clear":
        deleteImages(data)
    elif action == "stop":
        stopDetection(data)
        flag = -1
    elif action == "start":
        print(f"Received from client: {data}")
        flag=1
    else:
        print(f"Unprocessable Entry: {data}")    
    return {"status":"success","code":200}



def saveImages(data):
    print(f"Received from client: {data}")
    
    
def deleteImages(data):
    print(f"Received from client: {data}")


def stopDetection(data):
    print(f"Received from client: {data}")

        


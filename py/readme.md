Run the testAPI on port 8000 to get the number of faces detected count published on websocket and to accept any http commands from the browser
sstreamDetection is for streaming the detected video result from py
resultStream is to stream the content so that it can be read from js to display on the webpage (run it on port 8001)

Now if you run the resultSteam program then no need to run testAPI or sstreamDetection as it will take care of both the functions
However you have to run the captureAPI to take in commands from the browser and perform necessary actions (run this on port 8000)

cmd to fun these files-
uvicorn <filename>:app --host 0.0.0.0 --port <port> --reload

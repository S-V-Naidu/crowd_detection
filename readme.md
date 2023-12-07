Run the http-server in this directory which will load the index.html as the default page

To start that server-
python -m http.server

Also, in analyse.js file change the socket and api IP to your host IP


Totally create 2 API ports-
1. hosting the web application to display the html
2. To host the websocket and transmit the video frames with boxes around people
3. To send and receive commands to the browser and perform actions (send count of people, save captured images, delete captured images...)

1st one will be hosted on port 8002
2nd one will be hosted on port 8001
3rd one will be hosted on port 8000
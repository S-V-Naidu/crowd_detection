// const socket = new WebSocket('ws://192.168.2.101:8000/ws'); //-> Use this is you are using testAPI.py at the backend and want to receive continous stream of count of people in the frame
const streamSocket = new WebSocket("ws://localhost:8001/ws");
function init_api() {
    console.log("init api");
    //btn1.onclick = runAPI;
    document.getElementById("btn1").addEventListener("click", runAPI);
    btn2.onclick = captureFrame;
    // btn3.onclick = stopAPI;
    // $("apiresponse").scrollTop($("apiResponse").children().height());
    // setTimeout(function() {
    // 	openStatus();
	// }, 5000);

	const videoFrame = document.getElementById("videoPlayer");
        
    streamSocket.onmessage = (event) => {
        const frameData = event.data;
        videoFrame.src = "data:image/jpeg;base64," + frameData;
    };

    streamSocket.onclose = () => {
        console.log("WebSocket connection closed.");
    };
}

// function openStatus(){
// 	socket.addEventListener('open', (event) => {
//         console.log('WebSocket is now OPEN to send data');
// 	});

// 	// streamSoc.addEventListener('open', (event) => {
//     //     console.log('WebSocket is now OPEN to receive data');
// 	// });
// }

var cap = null;

function runAPI(){
	console.log("Run btn is clicked");
	const message = {"action":"start","data":[]};
    if (streamSocket.readyState == WebSocket.OPEN) {
    	// socket.send(JSON.stringify(message));
    	// document.getElementById('apiResponse').innerHTML += "<br>Starting the face detections from the feed";

		var xmlHttp = new XMLHttpRequest();
	    xmlHttp.open( "GET", "http://localhost:8000/cmd/count", false ); // false for synchronous request
	    xmlHttp.send( null );
		document.getElementById('apiResponse').innerHTML += "<br>Faces detected in the frame: "+xmlHttp.responseText;
        console.log("Message received = "+xmlHttp.responseText);		

    	// streamSocket.onmessage = function (evt) {
        // 	//alert("About to receive data");
        // 	var received_msg = evt.data;
        // 	document.getElementById('apiResponse').innerHTML += "<br>Faces detected in the frame: "+received_msg;
        // 	console.log("Message received = "+received_msg);
		// };
    } 
    else{
    	console.error('WebSocket is not open. Cannot send the start signal.');
    }
		//document.getElementById('apiResponse').innerHTML = "\nFaces detected in the frame: "+count;
		
		//soc.addEventListener('message', (event) => {
        // const data = event.data;
        // document.getElementById('apiResponse').innerHTML += "<br>Faces detected in the frame: "+data;
      	//});
}

async function captureFrame(){
	console.log("Frame captured! Saved in the /captured folder");
	document.getElementById('captureAlert').innerHTML = "Frame captured"
	setTimeout(function() {
    	document.getElementById('captureAlert').innerHTML = " ";
	}, 1000);
	// document.getElementById('captureAlert').innerHTML = "";
	//document.getElementById('canvasHeading').innerHTML = JSON.stringify("Latest Captured Image");
  	document.getElementById('canvasHeading').innerHTML = "Latest Captured Image";
  	captureFrameAndSave();
}

function captureFrameAndSave() {
    // Create a canvas to draw the captured frame
    var outputCanvas = document.getElementById("canvasDisplay");
 	var video = document.getElementById("videoPlayer");
    const canvas = document.createElement('canvas');
    canvas.width = video.width;
    canvas.height = video.height;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Calculate the desired dimensions for the resized image
    const maxWidth = 780; // Change this to your desired width
    const maxHeight = 240; // Change this to your desired height
    const aspectRatio = canvas.width / canvas.height;

    let newWidth, newHeight;
    if (aspectRatio > (maxWidth / maxHeight)) {
        newWidth = maxWidth;
        newHeight = newWidth / aspectRatio;
    } else {
        newHeight = maxHeight;
        newWidth = newHeight * aspectRatio;
    }

    // Create a new canvas for the resized image
    outputCanvas.width = newWidth;
    outputCanvas.height = newHeight;
    const outputContext = outputCanvas.getContext('2d');

    // Draw the captured frame onto the new canvas with the desired dimensions
    outputContext.drawImage(canvas, 0, 0, newWidth, newHeight);

    const message = {"action":"save","data":[outputContext]};
    if (streamSocket.readyState === WebSocket.OPEN) {
    	//socket.send(JSON.stringify(message));
    	fetch("http://localhost:8000/cmd?action=save&value=null", {
			method: "POST",
			body: 
			{
				"action":"save",
				"value":[outputContext]
			},
			headers: {
			"Content-type": "application/json; charset=UTF-8"
			}
		});
    } else{
    	console.error('WebSocket is not open. Cannot send the message.');
    }
}

// function stopAPI(){
// 	if (flag == 1){
// 		console.log("Now stopping the face detections thread");
// 		const message = {"action":"stop","data":[]};
// 	    if (streamSocket.readyState === WebSocket.OPEN) {
// 	    	//socket.send(JSON.stringify(message));
// 	    	fetch("http://192.168.2.101:8001/cmd?action=stop&value=null", {
//   				method: "POST",
//   				body: 
//   				{
//   					"action":"stop",
//   					"value":null
//   				},
//   				headers: {
//     				"Content-type": "application/json; charset=UTF-8"
//   				}
// 			});

// 	    	document.getElementById('apiResponse').innerHTML += "<br>Stopped detection.";
// 	    	flag = 0;
// 	    } else{
// 	    	console.error('WebSocket is not open. Cannot send the stop signal.');
// 	    }	
// 	}
// 	else{
// 		console.log("First start the detection, later we can worry about stopping it!");
// 		// var content = document.createTextNode("<br>Nothing Running to stop");
// 		// document.getElementById('apiResponse').appendChild(content);
// 		document.getElementById('apiResponse').innerHTML += "<br>Nothing Running to stop";		
// 	}
// }


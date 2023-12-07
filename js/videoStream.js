//Constants
var SESSION_STATUS = Flashphoner.constants.SESSION_STATUS;
var STREAM_STATUS = Flashphoner.constants.STREAM_STATUS;
var session;
var stream;
  
//Init Flashphoner API on page load
function init_api() {
    console.log("init api");
    Flashphoner.init({});
    btn1.onclick = connect;
    btn2.onclick = stopPublish;
}
  
//Connect to WCS server over websockets
function connect() {
    session = Flashphoner.createSession({
        urlServer: "wss://demo.flashphoner.com"
    }).on(SESSION_STATUS.ESTABLISHED, function(session) {
        publishStream(session);
    });
}

//Publish stream
function publishStream(session) {
    var options = {name: "rtsp://admin:Unidad123@192.168.2.102:554?channel=1&subtype=1",display:document.getElementById("videoPlayer")};
    stream = session.createStream(options)
    stream.publish();
    console.log("Started detecting faces")
}
 
//Stopping stream
function stopPublish() {
    stream.stop();
    console.log("Stopped detection")
}

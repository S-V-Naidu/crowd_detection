
function init_api() {
    console.log("init api");
    clearBtn.onclick = deleteImages;
    document.getElementById("nothing").innerHTML = " Nothing captured yet:/";
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/captures/", true);
    xhr.responseType = 'document';
    xhr.onload = () => {
        if (xhr.status === 200) {
            var elements = xhr.response.getElementsByTagName("a");
            for (x of elements) {
                if ( x.href.match(/\.(jpe?g|png|gif)$/) ) { 
                  let img = document.createElement("img");
                  img.src = x.href;
                  document.getElementById("captures").appendChild(img);
                } 
            };
            document.getElementById("nothing").innerHTML = "";
        } 
        else {
            alert('Request failed. Returned status of ' + xhr.status);
        }
    }
    
    xhr.send()
}

function deleteImages(){
    console.log("Cleared all the captured images from the folder.");
    const message = {"action":"clear","data":[]};
    fetch("http://192.168.2.101:8000/cmd?action=clear&value=null", {
        method: "POST",
        body: 
        {
            "action":"clear",
            "value":null
        },
        headers: {
        "Content-type": "application/json; charset=UTF-8"
        }
    });
    alert("Emptied the captured images")
}

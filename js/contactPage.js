function init_api(){
    document.getElementById("entry").addEventListener("click", contactSubmit);
}

function contactSubmit(){
    nameInput = document.getElementById("name1").value;
    emailInput = document.getElementById("email1").value;
    issueInput = document.getElementById("issue1").value;

    const message = {"name":nameInput,"email":emailInput, "issue":issueInput};
    fetch("http://localhost:8000/cmd?action=submit&value="+JSON.stringify(message), {
        method: "POST",
        body: 
        {
            "action":"submit",
            "value":JSON.stringify(message)
        },
        headers: {
        "Content-type": "application/json; charset=UTF-8"
        }
    });

    document.getElementById("name1").value = "";
    document.getElementById("email1").value = "";
    document.getElementById("issue1").value = "";
    console.log(message);

    alert("Your query has been recorded. The issue will soon be fixed.");
}
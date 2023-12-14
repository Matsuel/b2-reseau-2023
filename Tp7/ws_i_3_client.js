const websocket = new WebSocket("ws://localhost:8000");

websocket.onopen = function (event) {
    const username=prompt("Enter your username");
    console.log("Connection established!");
    websocket.send("join|"+username);
    websocket.onmessage = function (event) {
        const messageDiv = document.createElement("div");
        messageDiv.innerHTML = event.data;
        document.getElementById("output").appendChild(messageDiv);
    }
}

function send(){
    event.preventDefault();
    const inputValue=document.getElementById("input").value;
    document.getElementById("input").value="";
    const messageDiv = document.createElement("div");
    messageDiv.innerHTML = "Vous avez dit: "+inputValue;
    document.getElementById("output").appendChild(messageDiv);
    websocket.send("message|"+inputValue);

    websocket.onmessage = function(event){
        const messageDiv = document.createElement("div");
        messageDiv.innerHTML = event.data;
        document.getElementById("output").appendChild(messageDiv);
    }
}
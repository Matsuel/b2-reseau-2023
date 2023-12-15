const websocket = new WebSocket("ws://localhost:8000");

websocket.onopen = function (event) {
    const username=prompt("Enter your username");
    console.log("Connection established!");
    websocket.send(JSON.stringify({type:"join",pseudo:username}));
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
    websocket.send(JSON.stringify({type:"message",message:inputValue}));

    websocket.onmessage = function(event){
        const messageDiv = document.createElement("div");
        messageDiv.innerHTML = event.data;
        document.getElementById("output").appendChild(messageDiv);
    }
}
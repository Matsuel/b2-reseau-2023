const websocket = new WebSocket("ws://localhost:8000");

function send(){
    event.preventDefault();
    const inputValue=document.getElementById("input").value;
    websocket.send(inputValue);
    
    websocket.onmessage = function(event){
        console.log(event.data);
        const responseDiv = document.getElementById("output");
        responseDiv.innerHTML = event.data;
    }
}
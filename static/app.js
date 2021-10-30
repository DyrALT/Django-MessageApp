const roomName = JSON.parse(document.getElementById('room-name').textContent);
const conversation=document.getElementById("conversation");
const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);

chatSocket.onmessage=function (e) {
    const data = JSON.parse(e.data);

}

chatSocket.onclose=function(e){
  console.error(e);
}
const sendButton=document.getElementById("sendmsg");
const inputField=document.getElementById("mytext");
inputField.focus();
inputField.onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter, return
    document.querySelector("#sendmsg").click();
  }
};

sendButton.click=function (e){
  const messsage=inputField.value
  chatSocket.send(JSON.stringify({
    "message":messsage
  }));
  inputField.value = "";
  console.log(messsage);
}
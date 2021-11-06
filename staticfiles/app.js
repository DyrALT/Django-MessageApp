const roomName = JSON.parse(document.getElementById("room-name").textContent);
const user = JSON.parse(document.getElementById("user").textContent);
const conversation = document.getElementById("conversation");
const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  const message_type = data.typess;
  if (message_type==="text") {
    var message = data.message;
  }else if(message_type ==="image"){
    var message=`<img id="myImg" width="250" height="250" src="${data.message}">`
  }
  // console.log(data.type);
  if (user === data.user) {
    var message = `<div class="row message-body">
      <div class="col-sm-12 message-main-sender">
         <div class="sender">
          <div class="message-text">${message}</div>
          <span class="message-time pull-right">${data.created_date}</span>
        </div> 
      </div>
    </div>
  </div>`;
  } else {
    var message = `<div class="row message-body">
      <div class="col-sm-12 message-main-receiver">
         <div class="receiver">
          <div class="message-text">${message}</div>
          <span class="message-time pull-right">${data.created_date}</span>
        </div> 
      </div>
    </div>
  </div>`;
  }
  conversation.innerHTML += message;
};

chatSocket.onclose = function (e) {
  console.error(e);
};
const sendButton = document.getElementById("sendmsg");
const inputField = document.getElementById("mytext");
inputField.focus();
inputField.onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter, return
    document.querySelector("#sendmsg").click();
  }
};

sendButton.click = function (e) {
  const messsage = inputField.value;
  chatSocket.send(
    JSON.stringify({
      "message": messsage,
      "typess":"text"
    })
  );
  console.log(messsage.type);
  inputField.value = "";
};


document.getElementById("hiddeninput").addEventListener("change",handleFileSelect,false);

function getBase64(file,fileType) {
  var reader = new FileReader()
  var type=fileType.split("/")[0]
  reader.readAsDataURL(file)
  console.log(type);
  reader.onload=function(){
    chatSocket.send(JSON.stringify({
      "message":reader.result,
      "typess" : type
    }))
  }
}

function handleFileSelect() {
  var file=document.getElementById('hiddeninput').files[0];
  console.log(file.type);
  getBase64(file,file.type);
  console.log(file);
}

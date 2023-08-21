const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("user-input");

$("#user-input").keyup(function (event) {
  if (event.keyCode === 13 && $("#user-input").val().trim().length > 0) {
    $("#sendMessageBtn").click();
  }
});

function sendMessage() {
  if ($("#user-input").val().trim().length == 0) {
    return false;
  }
  const userMessage = userInput.value;
  displayMessage("You", userMessage, "sent");
  userInput.value = "";

  // Make an API call to the Flask backend to get the chatbot response
  fetch("/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `user_input=${userMessage}`,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Response:", data.message);
      displayMessage("PyGPT", data.message, "received");
    })
    .catch((error) => {
      console.error("Error:", error.message);
    });
}

function displayMessage(sender, message, messageType) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", messageType);
  messageElement.innerHTML = `<span><b>${sender}:</b> ${message}</span>`;
  chatbox.appendChild(messageElement);
  chatbox.scrollTop = chatbox.scrollHeight;
}

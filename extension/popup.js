document.addEventListener("DOMContentLoaded", function() {
    const sendBtn = document.getElementById("sendBtn");
    const userInput = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");

    function appendMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
        messageDiv.innerText = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll hacia abajo
    }

    sendBtn.addEventListener("click", function() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(message, "user");
        userInput.value = ""; // Limpiar input

        chrome.runtime.sendMessage({ action: "fetchGPT", prompt: message }, function(response) {
            if (response.error) {
                appendMessage("Error: " + response.error, "bot");
            } else {
                appendMessage(response.reply, "bot");
            }
        });
    });
});

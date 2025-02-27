chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "fetchGPT") {
        fetch('https://qpfef368k7.execute-api.us-east-1.amazonaws.com/endpoint_gpt', {
            method: 'POST',
            mode: 'cors',
            credentials: 'omit',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: request.prompt })
        })
        .then(response => response.json())
        .then(data => sendResponse({ reply: data.body.reply }))
        .catch(error => sendResponse({ error: error.message }));
        
        return true;  // Mantiene el canal abierto para sendResponse()
    }
});

console.log("Let's be great!!!");

// Function to send message to localhost:9000
function sendMessage(message) {
    // Add user message to UI
    addMessageToUI(message, "user");

    // fetch the current tab url and cache it
    chrome.tabs.query({ "active": true }, function (tab) {
        try {
            const video_url = tab[0]["url"];
            const video_id = extractVideoId(video_url);
        } catch (e) {
            console.log(e);
        }
    });

    // Retrieve the value of video_id from Chrome storage
    chrome.storage.local.get(["video_id"]).then((result) => { 
        let video_id = result["video_id"]; 
        console.log("Checking if the value was retured: ",video_id);

        // TODO: Retrieve backend URL from environment variable
        const backendUrl = 'http://localhost:8000';

        // Construct the URL for the POST request
        let apiUrl = `${backendUrl}/chat/${video_id}`;

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Message sent successfully:', data);
                // Add response to UI
                addMessageToUI(data.message, 'ai'); // Include timestamp and specify message type
            })
            .catch(error => {
                console.error('Error sending message:', error);
            });
    });
}

// Function to get current time
function getTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0'); // Get hours and pad with leading zero if necessary
    const minutes = now.getMinutes().toString().padStart(2, '0'); // Get minutes and pad with leading zero if necessary
    return `${hours}:${minutes}`; // Return formatted time (HH:MM)
}


// Function to add message to UI
function addMessageToUI(message, messageType) {
    const messageBox = document.querySelector('.messages_box');
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message-container', messageType + '-message'); // Add message type class

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.textContent = message;

    // Create and append timestamp element
    const timestamp = document.createElement('div');
    timestamp.classList.add('timestamp');
    timestamp.textContent = getTime();
    messageContainer.appendChild(messageContent);
    messageContainer.appendChild(timestamp);

    messageBox.appendChild(messageContainer);

    // Scroll to the bottom of the message box
    messageBox.scrollTop = messageBox.scrollHeight;
}

// Function to handle form submission
function handleSubmit(event) {
    event.preventDefault();
    const input = document.querySelector('#messageInput');
    const message = input.value.trim();
    if (message !== '') {
        // Send the message
        sendMessage(message);
        // Clear input field
        input.value = '';
    }
}

// Extract video id
function extractVideoId(url) {
    // Split the URL string at 'v=' and return the last part
    const parts = url.split('v=');
    console.log(parts);
    if (parts.length > 1) {
        let video_id = parts[1];
        chrome.storage.local.set({ "video_id": video_id }).then(() => { console.log("Value is set"); });
    } else {
        console.error('Invalid YouTube URL');
        return null;
    }
}

// Add event listener to form for handling submission
document.querySelector('#messageForm').addEventListener('submit', handleSubmit);

// Initial message
addMessageToUI("Hello, welcome to YTC, ask me anything about the current video and I will answer", 'ai'); // Include timestamp and specify message type
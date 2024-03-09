/**
 * Used channels tutorial https://channels.readthedocs.io/en/stable/tutorial/index.html as initial reference
 */

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const thisUsername = JSON.parse(document.getElementById('username').textContent);
const chatLog = JSON.parse(document.getElementById('chat-log').textContent);
let messageGroupNum = 0;
let lastUserWhoSendsMessage = null;
let typingStatusUsers = new Map();
let isTyping = false;

console.log("chat log is: " + chatLog);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === "chat-message") {
        console.log("chat message received");
        showMessage(data);
    } else if (data.type === "typing-status") {
        console.log("typing status received");
        showTypingStatus(data);
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();

document.querySelector('#chat-message-input').onkeyup = function(e) {
    // for firefox ref: https://developer.mozilla.org/en-US/docs/Web/API/Element/keyup_event
    if (e.isComposing || e.keyCode == 229) {
        return;
    };
    if (e.key === "Enter" && e.shiftKey == false) {
        document.querySelector('#chat-message-submit').click();
    } else {
        sendTypingStatus(e);
    };
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message.trim().length === 0) {
        return;
    }
    chatSocket.send(JSON.stringify({
        "message": message,
        "type": "chat-message"
    }))
    messageInputDom.value = "";
};

function isOwnMessage(senderUsername) {
    if (thisUsername.toLowerCase() === senderUsername.toLowerCase()) {
        return true;
    } else {
        return false;
    };
};

function showMessage(data) {
    const area = document.getElementById("chat-message-area");

    // every message will be put in message group
    // message group will have one user name tag (if not one's own message)
    let messageGroup = null;

    // find if this message should be inserted into the previous message group
    if (data.username === lastUserWhoSendsMessage) {
        // this message will be inserted into the previous message group
        messageGroup = document.getElementById("message-group-" + messageGroupNum);
    } else {
        // create new message group
        messageGroup = document.createElement("div");
        messageGroupNum += 1;
        messageGroup.id = "message-group-" + messageGroupNum;
        let messageGroupClass = "d-flex flex-column m-5";

        // determine if this is one's own message
        if (isOwnMessage(data.username) === true) {
            messageGroupClass += " align-items-end";
        } else {
            messageGroupClass += " align-items-start";

            // create name tag
            let messageUsernameTag = document.createElement("div");
            messageUsernameTag.classList.add("message-username-tag");
            messageUsernameTag.appendChild(document.createTextNode(data.username));
            messageGroup.appendChild(messageUsernameTag);
        };
        messageGroup.setAttribute("class", messageGroupClass);
    }

    // create new message row which contains message box and timestamp
    const messageRow = document.createElement("div");
    let messageRowClass = "d-flex align-items-end"
    if (isOwnMessage(data.username) === true) {
        messageRowClass += " flex-row-reverse";
    } else {
        messageRowClass += " flex-row";
    }
    messageRow.setAttribute("class", messageRowClass);

    // create timestamp
    const messageTime = document.createElement("div");
    // YYYYMMDDHHmmss
    const hour = data.time.substring(8, 10);
    const minute = data.time.substring(10, 12);
    messageTime.appendChild(document.createTextNode(hour + ":" + minute));
    messageTime.setAttribute("class", "message-time")
    
    // create message box
    const messageBox = document.createElement("div");
    messageBox.classList.add("message-box");
    const messageBoxContent = document.createElement("div");

    // append everything together
    messageBoxContent.appendChild(document.createTextNode(data.message));
    messageBox.appendChild(messageBoxContent);
    messageRow.appendChild(messageBox);
    messageRow.appendChild(messageTime);
    messageGroup.appendChild(messageRow);
    area.appendChild(messageGroup);

    messageRow.scrollIntoView();
    lastUserWhoSendsMessage = data.username;

};

function sendTypingStatus(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message.trim().length === 0) {
        return;
    };
    if (isTyping === false) {
        chatSocket.send(JSON.stringify({
            "type": "typing-status"
        }));
        // to reduce the number of message
        isTyping = true;
        setTimeout(function() {
            isTyping = false;
        }, 1.75 * 1000);
    }

};

function showTypingStatus(data) {

    if (isOwnMessage(data.username)) {
        return;
    }

    let timeoutID;
    // if the user name is already displayed, refresh the timeout
    // by replacing it with the new timeout
    if (typingStatusUsers.has(data.username)) {
        timeoutID = typingStatusUsers.get(data.username);
        clearTimeout(timeoutID)
    }
    timeoutID = setTimeout(function() {
        removeTypingStatus(data.username)
    }, 2 * 1000);
    typingStatusUsers.set(data.username, timeoutID);
    displayTypingStatus();
}

function removeTypingStatus(username) {
    typingStatusUsers.delete(username);
    displayTypingStatus();
}

function displayTypingStatus() {
    const area = document.getElementById("typing-status-area");
    let text = "";
    if (typingStatusUsers.size > 0) {
        text = [...typingStatusUsers.keys()].join(", ") + " is typing...";
    };
    area.textContent = text;
}

function showChatHistory(log) {
    for (const data in log) {
        showMessage(log[data]);
    };
}

showChatHistory(chatLog);
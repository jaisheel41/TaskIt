
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const thisUsername = JSON.parse(document.getElementById('username').textContent);
const chatLog = JSON.parse(document.getElementById('chat-log').textContent);
let messageGroupNum = 0;
let lastUserWhoSendsMessage = null;
let emptyUpdateNum = 0;
let typingStatusUsers = new Map();
let isTyping = false;
let lastDate = "";

let lastTimeStamp = "";
let refreshTimer;

let userImages = new Map();

function getCookie(name) {
    // this function is from django documentation
    // https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.querySelector('#chat-message-input').focus();

$('#chat-message-input').keyup(function(e) {
    // for firefox ref: https://developer.mozilla.org/en-US/docs/Web/API/Element/keyup_event
    if (e.isComposing || e.keyCode == 229) {
        return;
    };
    if (e.key === "Enter" && e.shiftKey == false) {
        document.querySelector('#chat-message-submit').click();
    } else {
        sendTypingStatus(e);
    };
});

$("#chat-message-submit").click(function() {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message.trim().length === 0) {
        return;
    } else if (message.trim().length > 2000) {
        displayTooLongMessage();
        return;
    }
    $.ajax({
        url: '/chat/send-message/',
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            "type": "chat_message",
            "room": roomName,
            "username": thisUsername,
            "content": message
        }),
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
        },
        success: (data) => {
            //update();
            refreshNow();
        },
        error: (error) => {
            console.log(error);
        }
    });
    messageInputDom.value = "";
})

function update() {
    $.ajax({
        url: '/chat/update/',
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            "room": roomName,
            "username": thisUsername,
            "last-timestamp": lastTimeStamp
        }),
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
        },
        success: (data) => {
            if ($.isEmptyObject(data)) {
                emptyUpdateNum += 1;
            } else {
                emptyUpdateNum = 0;
            }
            handleReturnMessage(data['chat_message']);
            handleReturnTypingStatus(data['typing_status']);
        },
        error: (error) => {
            console.log(error);
        }
    });

}

function isOwnMessage(senderUsername) {
    if (thisUsername.toLowerCase() === senderUsername.toLowerCase()) {
        return true;
    } else {
        return false;
    };
};

function showMessage(data) {
    const area = document.getElementById("chat-message-area");

    // wrapper is user image and message group
    let messageWrapper = null;

    // every message will be put in message group
    // message group will have one user name tag (if not one's own message)
    let messageGroup = null;

    // find if new date should be inserted
    if (lastDate === "" | data.time.substring(0, 8) != lastDate) {
        // Create new date tag
        dateWrapper = document.createElement("div");
        dateWrapper.classList.add("date-wrapper");
        dateTag = document.createElement("div");
        dateTag.classList.add("date-tag");
        dateText = formatDate(data.time.substring(0, 8));

        dateTag.appendChild(document.createTextNode(dateText));
        dateWrapper.appendChild(dateTag);
        area.appendChild(dateWrapper);
        lastDate = data.time.substring(0, 8);
    }

    // find if this message should be inserted into the previous message group
    if (data.username === lastUserWhoSendsMessage && data.time.substring(0, 8) === lastDate) {
        // this message will be inserted into the previous message group
        messageWrapper = document.getElementById("message-wrapper-" + messageGroupNum);
        messageGroup = document.getElementById("message-group-" + messageGroupNum);
    } else {
        messageGroupNum += 1;
        
        // create new message wrapper
        messageWrapper = document.createElement("div");
        messageWrapper.classList.add("message-wrapper");
        messageWrapper.id = "message-wrapper-" + messageGroupNum;
        let messageWrapperClass = "d-flex flex-column";

        // create new message group
        messageGroup = document.createElement("div");
        messageGroup.id = "message-group-" + messageGroupNum;
        let messageGroupClass = "d-inline-flex flex-column m-5";

        // determine if this is one's own message
        if (isOwnMessage(data.username) === true) {
            messageWrapperClass += " align-items-end owned-message-wrapper";
            messageGroupClass += " align-items-end owned-message-group";
        } else {
            messageWrapperClass += " align-items-start not-owned-message-wrapper";
            messageGroupClass += " align-items-start not-owned-message-group";

            // create user image
            // wrapper
            let messageUserImageBox = document.createElement("div");
            messageUserImageBox.classList.add("message-user-image-box");
            messageUserImageBox.classList.add("message-user-image-box-" + data.username);

            // name wrapper
            let messageNameWrapper = document.createElement("div");
            messageNameWrapper.classList.add("message-name-wrapper");

            // image
            let messageUserImage = document.createElement("img");
            messageUserImage.classList.add("message-user-image");
            messageUserImage.src = "/static/media/userpic/" + data.userid + ".jpg";
            messageUserImageBox.appendChild(messageUserImage);

            messageNameWrapper.appendChild(messageUserImageBox);

            // create name tag
            let messageUsernameTag = document.createElement("div");
            messageUsernameTag.classList.add("message-username-tag");
            messageUsernameTag.appendChild(document.createTextNode(data.username));
            messageNameWrapper.appendChild(messageUsernameTag);
            messageGroup.appendChild(messageNameWrapper);
        };
        messageWrapper.setAttribute("class", messageWrapperClass);
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
    // YYYYMMDDHHmmss (and then ffffff)
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
    messageWrapper.appendChild(messageGroup);
    area.appendChild(messageWrapper);

    messageRow.scrollIntoView();
    lastUserWhoSendsMessage = data.username;

};

function handleReturnMessage(data) {
    for (let key in data) {
        if (data[key].time == lastTimeStamp) {
            break;
        }
        showMessage(data[key]);
        lastTimeStamp = data[key].time;
    }
}

function handleReturnTypingStatus(data) {
    for (let key in data) {
        showTypingStatus(data[key]);
    }
}

function refresh() {
    update();
    interval = 2.0 * 1000;
    if (emptyUpdateNum > 60) {
        interval = 5.0 * 1000;
    } else if (emptyUpdateNum > 100) {
        interval = 10.0 *1000;
    }
    refreshTimer = setTimeout(() => {
        refresh();
    }, interval);
}

function refreshNow() {
    clearTimeout(refreshTimer);
    refresh();
}

function sendTypingStatus(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message.trim().length === 0) {
        return;
    };
    if (isTyping === false) {
        $.ajax({
            url: '/chat/send-message/',
            type: "POST",
            dataType: "json",
            data: JSON.stringify({
                "type": "typing_status",
                "room": roomName,
                "username": thisUsername
            }),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrftoken,
            },
            success: (data) => {
                //update();
                refreshNow();
            },
            error: (error) => {
                console.log(error);
            }
        });
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
    }, 2.25 * 1000);
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

function displayTooLongMessage() {
    const area = document.getElementById("warning-message-area");
    let text = "Message exceeds the maximum character limit of 2000. Please shorten your message and try again.";
    area.textContent = text;
    timeoutID = setTimeout(function() {
        area.textContent = "";
    }, 3 * 1000);
}

function formatDate(daystamp) {

    const year = daystamp.substring(0, 4);
    const month = daystamp.substring(4, 6);
    const day = daystamp.substring(6, 8);

    const date = new Date(year, month - 1, day);
    const monthText = date.toLocaleString('default', {month: 'short'});
    const format = `${date.getDate()} ${monthText} ${date.getFullYear()}`;

    const today = new Date();
    let text = format;
    if (today.getFullYear() === date.getFullYear()
            && today.getMonth() === date.getMonth()) {
        // if it's today
        if (today.getDate() === date.getDate()) {
            text = "Today";
        } else {
            dayDiff = findDayDifference(today, date);
            console.log(dayDiff);
            if (dayDiff == 1) {
                text = "Yesterday";
            } else if (dayDiff < 7) {
                text = `${dayDiff} days ago`;
            } else if (dayDiff < 10) {
                text = `a week ago`;
            }
        }
    }
    
    return text;
}

function findDayDifference(a, b) {
    const calc = 1000 * 60 * 60 *24;
    const day1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
    const day2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());

    return Math.floor(Math.abs(day1 - day2) / calc);
}


handleReturnMessage(chatLog);

setTimeout(() => {
    refresh();
}, "3000");

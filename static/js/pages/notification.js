window.toggleNotifications = toggleNotifications;

document.addEventListener('DOMContentLoaded', function() {
    fetchNotifications();
});

function toggleNotifications() {
    var popup = document.getElementById("notification-popup");
    var isDisplayed = popup.style.display === "block";
    popup.style.display = isDisplayed ? "none" : "block";

    if (!isDisplayed) {
        fetchNotifications();
    }
}

function fetchNotifications() {
    fetch('/task/notifications/fetch/')
        .then(response => response.json())
        .then(data => {
            displayNotifications(data.notifications);
            updateNotificationBell(data.notifications.length);
        });
}

function updateNotificationBell(count) {
    const bellIcon = document.getElementById("notification-count");
    if (count > 0) {
        bellIcon.innerText = count;
        bellIcon.style.display = "block";
    } else {
        bellIcon.style.display = "none";
    }
}

function displayNotifications(notifications) {
    var notificationPopup = document.getElementById("notification-popup");
    notificationPopup.innerHTML = ''; // Clear previous notifications
    notifications.forEach(notification => {
        var notificationItem = document.createElement("div");
        notificationItem.innerHTML = notification.message;
        notificationItem.onclick = function() {
            markNotificationRead(notification.id);
            notificationItem.remove(); // Optionally remove the notification from the popup
        };
        notificationPopup.appendChild(notificationItem);
    });
}


// function displayNotifications(notifications) {
//     var notificationPopup = document.getElementById("notification-popup");
//     notificationPopup.innerHTML = ''; 
//     notifications.forEach(notification => {
//         var notificationItem = document.createElement("div");
//         notificationItem.innerHTML = notification.message;
//         notificationItem.onclick = function() {
//             markNotificationRead(notification.id);
//         };
//         notificationPopup.appendChild(notificationItem);
//     });

    
//     addClearButtonListener();
// }

function addClearButtonListener() {
    setTimeout(function() {
        var clearBtn = document.getElementById('clear-notifications-btn');
        if (clearBtn) {
            clearBtn.removeEventListener('click', clearReadNotifications);
            clearBtn.addEventListener('click', clearReadNotifications);
        }
    }, 0);
}

function markNotificationRead(notificationId) {
    fetch(`/notifications/read/${notificationId}/`)
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                fetchNotifications(); // Refetch to update UI
            }
        });
}

function clearReadNotifications() {
    fetch('/task/notifications/clear/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), 
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            
            let notificationsPopup = document.getElementById('notification-popup');
            notificationsPopup.innerHTML = ''; 
            console.log('All read notifications have been cleared.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

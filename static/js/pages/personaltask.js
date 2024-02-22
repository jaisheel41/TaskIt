function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    // ... other event listeners ...

    // This variable will hold the ID of the task to delete
    let taskToDeleteId = null;

    // Event listener for all delete buttons
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            taskToDeleteId = this.dataset.taskId;
            $('#deleteConfirmationModal').modal('show');
        });
    });

    // Event listener for the confirmation button in the delete modal
    document.getElementById('deleteTaskConfirm').addEventListener('click', function() {
        if (taskToDeleteId) {
            fetch(`/task/delete/${taskToDeleteId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'task_id': taskToDeleteId })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                $('#deleteConfirmationModal').modal('hide');
                if (data.success) {
                    document.querySelector(`[data-task-id="${taskToDeleteId}"]`).closest('.task-card').remove();
                } else {
                    alert('Error: Task could not be deleted.');
                }
            })
            .catch(error => {
                alert('Error: ' + error.message);
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var createTaskBtn = document.getElementById('create-task-btn');
    var createTaskModal = document.getElementById('create-task-modal');
    var createTaskForm = document.getElementById('create-task-form');

    // Function to show the task creation modal
    function showModal() {
        createTaskModal.style.display = 'flex';
    }

    // Function to hide the task creation modal
    function hideModal() {
        createTaskModal.style.display = 'none';
    }

    // Event listener for the 'Create Task' button
    createTaskBtn.addEventListener('click', function() {
        showModal();
    });


    // Event listener for the form submission
    createTaskForm.addEventListener('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(createTaskForm);

        fetch('/task/create/', { // Make sure this URL is correct
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Correctly getting the CSRF token
            },
            credentials: 'same-origin' // Changed from 'include' to 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if(data.error) {
                alert('An error occurred, please try again');
            } else {
                hideModal();
                location.reload(); // Simplest approach
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    // Close modal if clicked outside of the form
    window.onclick = function(event) {
        if (event.target == createTaskModal) {
            hideModal();
        }
    };
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function updateTaskCard(task, taskId) {
    const taskCard = document.querySelector('.task-card[data-task-id="' + taskId + '"]');
    taskCard.querySelector('.card-title').textContent = task.taskname;
    taskCard.querySelector('.card-text').textContent = task.description;
    const deadlineDate = new Date(task.end_time); // Assuming 'end_time' is in ISO format
    const formattedDate = deadlineDate.toLocaleDateString('en-US', {
        year: 'numeric', 
        month: 'short', 
        day: 'numeric'
    });
    taskCard.querySelector('.card-deadline').textContent = 'Deadline: ' + formattedDate;
    // taskCard.querySelector('.card-deadline').textContent = 'Deadline: ' + new Date(task.end_time).toLocaleDateString();
    // Update other task card elements as needed
}

document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.save-edit-btn');

    editButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const taskId = this.dataset.taskId;
            const form = document.getElementById('edit-task-form-' + taskId);
            const formData = new FormData(form);
            formData.append('csrfmiddlewaretoken', getCSRFToken()); // Append CSRF Token to the form data
            
            fetch(`/task/update/${taskId}/`, { // Update with the correct URL pattern for updating tasks
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                $('#editTaskModal-' + taskId).modal('hide');
                updateTaskCard(data.task, taskId);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

const uuid = JSON.parse(document.getElementById('uuid').textContent);
const projectID = JSON.parse(document.getElementById('project-id').textContent);

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
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

function onTaskDeleted() {
    window.location.reload(true); // Force reload from the server, not cache
}

document.addEventListener('DOMContentLoaded', function() {
    
    let taskToDeleteId = null;

    // Event listener for all delete buttons
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            // Get the taskId from the button's dataset
            let taskId = this.dataset.taskId;
            // Store taskId in the confirm button's dataset
            document.getElementById('deleteTaskConfirm').dataset.taskId = taskId;
            // Show the modal
            $('#deleteConfirmationModal').modal('show');
        });
    });

    // Event listener for the confirmation button in the delete modal
    document.getElementById('deleteTaskConfirm').addEventListener('click', function() {
        // Retrieve taskId from the confirm button's dataset
        let taskId = this.dataset.taskId;
        if (taskId) {
            fetch(`/task/project/${uuid}/delete/${taskId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'task_id': taskId })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    // Reload the page to reflect the changes
                    window.location.reload(true);
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
        formData.append("project", projectID);

        fetch(`/task/project/${uuid}/create/`, { 
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') //  getting the CSRF token
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
                location.reload(); 
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
    const deadlineDate = new Date(task.end_time); 
    const formattedDate = deadlineDate.toLocaleDateString('en-US', {
        year: 'numeric', 
        month: 'short', 
        day: 'numeric'
    });
    taskCard.querySelector('.card-deadline').textContent = 'Deadline: ' + formattedDate;

    const progressBar = taskCard.querySelector('.progress-bar');
    progressBar.style.width = task.status + '%';
    progressBar.setAttribute('aria-valuenow', task.status);
    progressBar.textContent = task.status + '%';
}

document.querySelectorAll('.save-edit-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        const taskId = this.dataset.taskId;
        const form = document.getElementById('edit-task-form-' + taskId);
        const formData = new FormData(form);
        formData.append("project", projectID);

        fetch(`/task/project/${uuid}/update/${taskId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert('An error occurred, please try again');
            } else {
                // Update the task card on the page
                updateTaskCard(data.task, taskId);
                $('#editTaskModal-' + taskId).modal('hide');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});


function updateMinEndDate(startInput, endInputId) {
    const endDateInput = document.getElementById(endInputId);
    if (endDateInput) {
        endDateInput.min = startInput.value;
    }
}

$('#editTaskModal').on('hidden.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var taskId = button.data('task-id'); 
    var savedTaskStatus = button.data('task-status'); // This should be the saved status, not the one from the unsaved modal state

    // Find the progress elements within the modal
    var modal = $(this);
    var progressBar = modal.find('.progress-bar[id="progressBar-' + taskId + '"]');
    var progressInput = modal.find('input[type="range"][id="statusInput-' + taskId + '"]');

    // Reset the progress bar and input to the saved status
    progressBar.css('width', savedTaskStatus + '%').attr('aria-valuenow', savedTaskStatus).text(savedTaskStatus + '%');
    progressInput.val(savedTaskStatus);
});

$('#editTaskModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var taskId = button.data('task-id');

    fetch(`/get-task-status/${taskId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            var taskStatus = data.taskStatus;

            var modal = $(this);
            var progressBar = modal.find('.progress-bar[id="progressBar-' + taskId + '"]');
            var progressInput = modal.find('input[type="range"][id="statusInput-' + taskId + '"]');

            // Update the progress bar and range input to reflect the latest saved task status
            progressBar.css('width', taskStatus + '%').attr('aria-valuenow', taskStatus).text(taskStatus + '%');
            progressInput.val(taskStatus);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

document.addEventListener('DOMContentLoaded', function() {
    const startTimeInputs = document.querySelectorAll('.start-time-input');
    startTimeInputs.forEach(input => {
        const endInputId = input.id.replace('startTime', 'endTime');
        updateMinEndDate(input, endInputId);
    });

    const descriptionInputs = document.querySelectorAll('textarea[id^="taskDescription"]');

    descriptionInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.length > 200) { 
                alert("Description cannot exceed 200 characters.");
                this.value = this.value.substring(0, 200); 
            }
        });
    });
});

function updateProgress(inputElement, taskId) {
    var progressValue = inputElement.value;
    var progressBar = document.getElementById('progressBar-' + taskId);
    progressBar.style.width = progressValue + '%';
    progressBar.setAttribute('aria-valuenow', progressValue);
    progressBar.textContent = progressValue + '%';
}

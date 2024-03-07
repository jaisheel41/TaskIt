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

document.addEventListener('DOMContentLoaded', function() {
    var createProjectBtn = document.getElementById('create-project-btn');
    var createProjectModal = document.getElementById('create-project-modal');
    var createProjectForm = document.getElementById('create-project-form');



    // Show the project creation modal
    function showModal() {
        createProjectModal.style.display = 'flex';
    }

    // Hide the project creation modal
    function hideModal() {
        createProjectModal.style.display = 'none';
    }

    // Event listener for the 'Create New Project' button
    createProjectBtn.addEventListener('click', function() {
        showModal();
    });

    // Submit the form for creating a new project
    createProjectForm.addEventListener('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(createProjectForm);
        var selectUsersElement = document.getElementById('projectUsers');
        var selectedUsers = [...selectUsersElement.selectedOptions].map(option => option.value);

    // Append selected user ids to FormData
        selectedUsers.forEach((userId, index) => formData.append('project_users_' + index, userId));

        fetch('/project/create/', { // Ensure this URL matches your route for project creation
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin'
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
                location.reload(); // Reload the page to show the new project
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });


    });



    // Close modal if clicked outside of it
    window.onclick = function(event) {
        if (event.target == createProjectModal) {
            hideModal();
        }
    };
});

// Load users into the 'Select Users' dropdown
document.addEventListener('DOMContentLoaded', function() {
    fetch('/users/list/', { // Ensure this URL matches your route for listing users
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        const selectUsers = document.getElementById('projectUsers');
        console.log(data);
        data.forEach(user => {
            let option = new Option(user.id, user.id); // Assuming 'user' objects have 'id' and 'name'
            selectUsers.appendChild(option);
        });
    })
    .catch(error => console.error('Error:', error));


    document.addEventListener('click', function(event) {
    if (event.target.classList.contains('btn-delete')) {
        const projectId = event.target.getAttribute('data-project-id');
        if (confirm('Are you sure you want to delete this project?')) {
            fetch(`/task/project/delete/${projectId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'project_id': projectId })
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    // Optionally, remove the project card from the DOM
                    document.querySelector(`.project-card[data-project-id="${projectId}"]`).remove();
                    alert('Project successfully deleted.');
                } else {
                    alert('An error occurred. Please try again.');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }
    });

    document.querySelectorAll('.save-edit-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        const projectId = this.dataset.projectId;
        const form = document.getElementById(`edit-project-form-${projectId}`);
        const formData = new FormData(form);

        fetch(`/task/project/update/${projectId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                // Close modal and optionally refresh data or the whole page to show changes
                $('#editProjectModal-' + projectId).modal('hide');
                alert('Project successfully updated.');
                location.reload();  // For simplicity, though it's better to dynamically update the page content
            } else {
                alert('An error occurred. Please try again.');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

});

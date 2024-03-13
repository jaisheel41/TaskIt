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
    function getCSRFToken() {
        return getCookie('csrftoken');
    }



});

    // Event listener for all delete buttons
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            // Get the projectId from the button's dataset
            let projectId = this.dataset.projectId; // Ensure your button has `data-project-id`
            // Store projectId in the confirm button's dataset for later use
            document.getElementById('deleteProjectConfirm').dataset.projectId = projectId;
            // Show the modal
            $('#deleteConfirmationModal').modal('show');
        });
    });

    // Event listener for the confirmation button in the delete modal
    document.getElementById('deleteProjectConfirm').addEventListener('click', function() {
        let projectId = this.dataset.projectId; // Retrieve projectId from the dataset
        if (projectId) {
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
                if (data.status === 'success') {
                    window.location.reload(true); // Reload the page to reflect changes
                } else {
                    alert('Error: Project could not be deleted.');
                }
            })
            .catch(error => {
                alert('Error: ' + error.message);
            });
        }
    });

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
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

    }).catch(error => console.error('Error:', error));
        // Initialize select2 for Create New Project modal
    $('#projectUsers').select2();

    // Initialize select2 for all Edit Project modals on page load
    initializeSelect2ForEditModals();

    // Rest of your existing code
    // ...

    // This function initializes select2 for Edit Project modals
    function initializeSelect2ForEditModals() {
        // This selector matches any select element with an ID starting with 'projectUsers-'
        $('[id^="projectUsers-"]').each(function() {
            $(this).select2();
        });
    }

    // Event listener for edit button, which triggers modal and select2 initialization
    $('.btn-edit').on('click', function() {
        // Extract project ID from the button's data attribute
        var projectId = $(this).data('projectId');
        // Initialize select2 for the edit modal related to the clicked project
        $('#projectUsers-' + projectId).select2();
        // Show the edit modal
        $('#editProjectModal-' + projectId).modal('show');
    })





    document.querySelectorAll('.save-edit-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        const projectId = this.dataset.projectId;
        const form = document.getElementById(`edit-project-form-${projectId}`);
        const formData = new FormData(form);

        // Get the selected user IDs from the select2 control
        const selectedUserIds = $(`#projectUsers-${projectId}`).select2('val');

        // Remove any previous user entries in formData
        formData.delete('project_users');

        // Add all selected user IDs to formData
        selectedUserIds.forEach(userId => {
            formData.append('project_users', userId);
        });

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
                updateProjectCard(data.project, projectId);
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

function updateProjectCard(project, projectId) {
    const taskCard = document.querySelector('.solution_card[data-project-id="' + projectId + '"]');
    if (taskCard) {
        taskCard.querySelector('.solu_title div').textContent = project.project_name;
        taskCard.querySelector('.solu_description p').textContent = project.project_description;
    } else {
        console.error('Project card not found for projectId:', projectId);
    }
}

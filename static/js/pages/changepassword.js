document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("changePasswordForm");
    const modal = document.getElementById("messageModal");
    const modalMessage = document.getElementById("modalMessage");
    const closeSpan = document.getElementsByClassName("close")[0];
  
    form.addEventListener("submit", function(event) {
      event.preventDefault();

      // Initialize a new FormData object from the form
      var formData = new FormData(form);
      
      // Make the AJAX request to the server
      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Ensure CSRF token is included
        },
        credentials: 'same-origin' // Include cookies in the request
      })
      .then(response => response.json())
      .then(data => {
        // Check if the password change was successful
        if (data.success) {
          // Password change was successful
          modalMessage.textContent = "Your password was successfully updated! Redirecting...";
          modal.style.display = "block";
          // Redirect after a short delay
          setTimeout(function() {
            window.location.href = "/"; // Replace with your homepage URL
          }, 2000); // Redirect delay in milliseconds
        } else {
          // Password change failed, show an error message
          modalMessage.textContent = data.error;
          modal.style.display = "block";
        }
      })
      .catch(error => {
        // Handle any other errors (like network issues)
        modalMessage.textContent = "An error occurred. Please try again.";
        modal.style.display = "block";
      });
    });
  
    // When the user clicks on <span> (x), close the modal
    closeSpan.onclick = function() {
      modal.style.display = "none";
    }
  
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
});

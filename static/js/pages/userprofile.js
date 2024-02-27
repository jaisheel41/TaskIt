document.getElementById('id_avatar').addEventListener('change', function() {
	var input = this;
	var file = input.files[0];
	
	if (file) {
		const reader = new FileReader();
				reader.onload = function() {
					const img = document.getElementById('userImage');
					img.src = reader.result;
				}
				reader.readAsDataURL(file);
		document.getElementById('label_avatar').style.background='#0d37a3';
	}
});

document.getElementById('saveChangesBtn').addEventListener('click', function() {
 
	uploadFile();
});

function uploadFile() {
	var fileInput = document.getElementById('id_avatar');
	var file = fileInput.files[0]; 

	var formData = new FormData();
	
	const csrfToken = getCookie('csrftoken');
	formData.append('csrfmiddlewaretoken', csrfToken);
	formData.append('avatar', file);
	
	var usernamelInput = document.getElementById('id_username').value;
	formData.append('username', usernamelInput);
	
	var emailInput = document.getElementById('id_email').value;
	formData.append('email', emailInput);
	
	var datejoinedlInput = document.getElementById('id_date_joined').value;
	formData.append('date_joined', datejoinedlInput);
	

	fetch("{% url 'profilesv' %}", { 
		method: 'POST',
		body: formData
	})
	.then(function(response) {
		if (response.ok) {
			return response.json();
		} else {
			throw new Error('Network response was not ok.');
		}
	})
	.then(function(data) {
		
		if (data.success){
			alert(data.message);
		}else{
			alert(data.message);
		}
		window.location.reload();
	})
	.catch(function(error) {
		console.error('error2:', error);
	});
};

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
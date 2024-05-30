document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loginForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(this); // Use 'this' to refer to the form element
    
        // Send the form data to the server
        fetch('/login/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Ensure you include the CSRF token
            }
        })
        .then(response => {
            console.log('Response received:', response);
            return response.json();
        })
        .then(data => {
            // print("to js")
            if (data.status === 'success') {
                if(data.message == 'client'){
                    // alert('Login success: ' + data.message);
                    window.location.href = '/home/'; // Redirect to the home page
                }else if(data.message == 'clinic'){
                    // alert('Login success: ' + data.message);
                    window.location.href = '/clinic/home/'; // Redirect to the home page
                }else if(data.message == 'doctor'){
                    // alert('Login success: ' + data.message);
                    window.location.href = '/doctor/page/'; // Redirect to the home page
                }else{

                }
            } else {
                alert('Login failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});
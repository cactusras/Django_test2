
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

            window.localStorage.clear()
            window.localStorage.setItem('user_type',data.user_type)
            window.localStorage.setItem('username',data.username)
            if (data.status === 'success') {
                if(data.user_type == 'client'){
                    // alert('Login success: ' + data.message);
                    window.location.href = '/home/'; // Redirect to the home page
                }else if(data.user_type == 'clinic'){
                    // alert('Login success: ' + data.message);
                    window.location.href = '/clinic/home/'; // Redirect to the home page
                }else if(data.user_type == 'doctor'){
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
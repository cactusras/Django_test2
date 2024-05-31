var clinField = {
    email: "",
    name: "",
    phone_number: "",
    license_number: "",
    password: "",
    introduction: "",
    address: "",
    photo: null,
};

function fetch_element() {
    clinField['email'] = document.getElementById('email').value;
    clinField['name'] = document.getElementById('name').value;
    clinField['phone_number'] = document.getElementById('phone_number').value;
    clinField['license_number'] = document.getElementById('license_number').value;
    clinField['password'] = document.getElementById('password').value;
    clinField['introduction'] = document.getElementById('introduction').value;
    clinField['address'] = document.getElementById('address').value;
    clinField['photo'] = document.getElementById('photo').files[0];
    console.log('phone_number: ' + clinField['phone_number']);
}

document.addEventListener('DOMContentLoaded', function () {
    // Ensure elements are loaded
    const btnRegis = document.getElementById('btnClinRegis');
    const btnDocManage = document.getElementById('btnDocManage');
    const barTitle = document.getElementById('barTitle');
    //fetch_element();

    // Handle login state
    if (window.isLogin) {
        fetch_element();
        barTitle.innerText = '診所資料';
        btnDocManage.hidden = false;
        btnDocManage.addEventListener('click', function () {
            window.location.href = "doctor_management.html";
        });
        btnRegis.addEventListener('click', function () {
            window.location.href = "clinicPage.html";
        });
        fetch_info();
    } else if(!window.isLogin) {
        btnDocManage.hidden = true;
        barTitle.innerText = '註冊';
    }
});

async function isUniqueLicense(license_number) {
    try {
        const response = await fetch('/isUniqueLicense_clin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ license_number: license_number })
        });
        const uniqueLicense = await response.json();
        return uniqueLicense.isUnique;
    } catch (error) {
        console.log('Error fetching registered licenses:', error);
        return false;
    }
}

async function isUniqueEmail(email) {
    try {
        const response = await fetch('/isUniqueEmail_clin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email })
        });
        const uniqueEmail = await response.json();
        return uniqueEmail.isUnique;
    } catch (error) {
        console.log('Error fetching registered emails:', error);
        return false;
    }
}

function fetch_info() {
    fetch('/clinic_info/', {
        method: 'GET'
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // 解析 JSON 响应
        })
        .then(infoDic => {
            username = infoDic['name'];
            for (var key in infoDic) {
                if (infoDic.hasOwnProperty(key)) {
                    clinField[key] = infoDic[key];
                }
            }
        })
        .catch(error => {
            console.log('Error:', error);
        });
}

document.getElementById('clinicForm').addEventListener('submit', async function (event) {
    let isValid = false;
    console.log("clicked regis");
    event.preventDefault(); // Prevent form submission if validation fails

    // Fetch form elements
    // fetch_element();

    // Use FormData for handling file uploads
    const formData = new FormData(document.getElementById('clinicForm'));

    // Validate form data
    if (formData.get('name').length > 100) {
        alert("Name cannot exceed 100 characters");
        return;
    } else if (!(/^\d+$/.test(formData.get('phone_number')))) {
        alert("Phone number can only contain digits");
        return;
    } else if (formData.get('phone_number').length > 15) {
        alert("Phone number cannot exceed 15 digits");
        return;
    } else if (!await isUniqueEmail(formData.get('email'))) {
        alert("Email already registered");
        return;
    } else if (!await isUniqueLicense(formData.get('email'))) {
        alert("License already registered");
        return;
    } else {
        isValid = true;
    }

    if (isValid) {

        // Send AJAX request
        fetch('/add/clinic/', {
            method: 'POST',
            body: formData,
            headers: {
                // 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Ensure you include the CSRF token
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
                window.location.href = '/loginP/';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }
});
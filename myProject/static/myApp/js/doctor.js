var docField = {
    email: "",
    name: "",
    phone_number: "",
    password: "",
    introduction: "",
    address: "",
    photo: null,
};

function fetch_element() {
    docField['email'] = document.getElementById('email').value;
    docField['name'] = document.getElementById('name').value;
    docField['phone_number'] = document.getElementById('phone_number').value;
    docField['password'] = document.getElementById('password').value;
   // docField['introduction'] = document.getElementById('introduction').value;
  //  docField['address'] = document.getElementById('address').value;
    docField['photo'] = document.getElementById('photo').files[0];
    console.log('phone_number' + docField['phone_number']);
}

document.addEventListener('DOMContentLoaded', function () {
    const btnRegis = document.getElementById('btnDocRegis');
    const btnDocManage = document.getElementById('btnDocManage');
    const barTitle = document.getElementById('barTitle');
    const docForm = document.getElementById('doctorForm');
    fetch_element();

    if (window.localStorage.getItem('isLogin') == 'success') {
        barTitle.innerText = '医生资料';
        btnDocManage.hidden = false;
        btnRegis.innerText = '完成';
        btnDocManage.addEventListener('click', function () {
            window.location.href = "/doctor/manage";
        });
        btnRegis.addEventListener('click', function () {
            window.location.href = "/clinic/home";
        });
        fetch_info(docForm);
    } else if (window.localStorage.getItem('isLogin') == 'failed') {
        btnRegis.innerText = '新增医生';
        btnDocManage.hidden = true;
        barTitle.innerText = '注册';
    }
});

async function isUniqueEmail(email) {
    try {
        const response = await fetch('/isUniqueEmail_doc/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                //'X-CSRFToken': getCookie('csrftoken')
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

function fillForm(data, form) {
    if (!form) {
        console.error('Form not found');
        return;
    }

    Object.keys(data).forEach(key => {
        const field = form.querySelector(`[name=${key}]`);
        if (field) {
            field.value = data[key];
        }
    });
}

function fetch_info(formFilled) {
    fetch('/doctor_info/', {
        method: 'GET'
    })
        .then(async response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();

            if (data.status === 'success') {
                const docInfo = data.data;
                console.log(docInfo.photo_url);
                fillForm(docInfo, formFilled);
            } else {
                console.error(data.error);
            }
        })
        .catch(error => {
            console.log('Error:', error);
        });
}

document.getElementById('doctorForm').addEventListener('submit', async function (event) {
    let isValid = false;
    console.log("clicked regis");
    event.preventDefault();

    fetch_element();

    if (docField.name.length > 100) {
        alert("Name cannot exceed 100 characters");
        return;
    } else {
        if (!(/^\d+$/.test(docField.phone_number))) {
            alert("Phone number can only contain digits");
            return;
        } else {
            if (docField.phone_number.length > 15) {
                alert("Phone number cannot exceed 15 digits");
                return;
            } else {
                if (!await isUniqueEmail(docField['email'])) {
                    alert("Email already registered");
                    return;
                } else {
                    isValid = true;
                }
            }
        }
    }

    if (isValid) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/add/doctor/', {
            method: 'POST',
            headers: {
                //'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: new FormData(this)
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);
                    window.location.href = '/loginP';
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

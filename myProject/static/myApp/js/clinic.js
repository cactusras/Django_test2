
var clinField = {
    email:"",
    name: "",
    phone_number: "",
    license_number: "",
    password: "",
    introduction: "",
    address: "",
    photo: null,
};

function fetch_element(){
        clinField['email'] = document.getElementById('email').value
        clinField['name'] = document.getElementById('name').value,
        clinField['phone_number'] = document.getElementById('phone_number').value,
        clinField['license_number'] = document.getElementById('license_number').value,
        clinField['password'] = document.getElementById('password').value,
        clinField['introduction'] = document.getElementById('introduction').value
        clinField['address'] = document.getElementById('address').value;
        if(window.localStorage.getItem('isLogin') == 'failed'){
            clinField['photo'] = document.getElementById('photo').files[0]
        }
        console.log('phone_number' + clinField['phone_number']);
}

document.addEventListener('DOMContentLoaded', function() {
        //頁面加載後才能把這些element load進來
        const btnRegis = document.getElementById('btnClinRegis');
        const btnDocManage = document.getElementById('btnDocManage');
        const barTitle = document.getElementById('barTitle');
        const clinForm = document.getElementById('clinicForm')
        const btnLogout = document.getElementById('logoutButton')
        const loginHide = document.querySelectorAll('.loginHide')
        const pwInput = document.getElementById('password')
        const emailShow = document.getElementById('emailShow')
        fetch_element();

        //canva11進入canva12   
        if (window.localStorage.getItem('isLogin') == 'success'){
            barTitle.innerText = '診所資料'
            btnDocManage.hidden = false;
            btnRegis.innerText = '完成'
            btnLogout.hidden = false;
            pwInput.required = false
            loginHide.forEach(element => {
                if (element.tagName.toLowerCase() === 'label') {
                    element.style.display = 'none'
                } else {
                    element.type = 'hidden'
                }
            });
            btnDocManage.addEventListener('click', function(){
                window.location.href = "/doctor/manage"
            })
            fetch_info(clinForm);
        }else if(window.localStorage.getItem('isLogin') == 'failed'){
            btnRegis.innerText = '完成'
            btnDocManage.hidden = true;
            barTitle.innerText = '註冊'
            btnLogout.hidden = true;
            pwInput.required = true;
            emailShow.style.display = 'none'
        }
})

function regis_click(event){
    event.preventDefault();
    if (window.isLogin) {
        
        window.location.href = "/clinic/home";
    } else {
        
        window.location.href = "/doctor/manage";
    }
}

async function isUniqueLicense(license_number){
    try {
        const response = await fetch('/isUniqueLicense_clin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                //'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({license_number: license_number})
        });
        const uniqueLicense = await response.json();
        return uniqueLicense.isUnique;
    } catch (error) {
        console.log('Error fetching registered license:', error);
        return false;
    }
}

async function isUniqueEmail(email){
    try {
        const response = await fetch('/isUniqueEmail_clin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                //'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({email: email})
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

function fetch_info(formFilled){
    fetch('/clinic_info/', {
        method: 'GET'
    })
    .then(async response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        //return response.json(); // 解析 JSON 响应
        if (data.status === 'success') {
            //顯示資料時不填入photo_url跟password(不影響後端)
            const clinInfo = data.data;
            if (clinInfo['password'] != ''){
                clinInfo['password'] = '';
            }
            /*clinInfo.forEach(element => {
                console.log('info = ' + element)
            });*/
            Object.keys(clinInfo).forEach(key => {
                console.log(`Key: ${key}, Value: ${clinInfo[key]}`);
            });
            
            document.getElementById('emailShow').innerText = clinInfo['email']
            document.getElementById('licenseShow').innerText = clinInfo['license_number']
            fillForm(clinInfo, formFilled);
        } else {
            console.error(data.error);
        }
    })  
    .catch(error => {
        console.log('Error:', error);
    });
}

document.getElementById('clinicForm').addEventListener('submit', async function(event){
    let isValid = false;
    console.log("clicked regis")
    event.preventDefault(); // 防止user沒填必填資料
    
    //在這裡處理這些attribute的限制(不能default vlue.length...)
    //有任一項不符合就進到return; 不會繼續往下
    fetch_element();
    //email格式在html的type = 'email'就確認了
    if (clinField.name.length > 100) {
        alert("Name cannot exceed 100 characters");
        return;
    } else {
            if (!(/^\d+$/.test(clinField.phone_number))) {
                alert("Phone number can only contain digits");
                return;
            } else {
                if (clinField.phone_number.length > 15) {
                    alert("Phone number cannot exceed 15 digits");
                    return;
                } else {
                    if(window.localStorage.getItem('isLogin') == 'failed'){
                        // 要串資料庫把所有的clinic email先找出來      
                        if (!await isUniqueEmail(clinField['email'])) {
                            alert("Email already registered");
                            return;
                        }else{
                            if (!await isUniqueLicense(clinField['license_number'])) {
                                alert("License already registered");
                                return;
                            }else{
                                isValid = true;
                            }
                        }
                    }else if(window.localStorage.getItem('isLogin') == 'success'){
                        isValid = true;
                    }
                }
            }
    }    
    if (isValid) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // 發送 AJAX 請求
        fetch('/add/clinic/', {
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
                if(window.localStorage.getItem('isLogin') == 'success'){
                    alert(data.message);
                    window.localStorage.setItem('username', clinField.name)
                    window.location.href = '/clinic/home';
                }else{
                    alert(data.message);
                    window.location.href = '/loginP';
                }
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
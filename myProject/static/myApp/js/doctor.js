
var docField = {
    email:"",
    name: "",
    phone_number: "",
    password: "",
    photo: null,
    experience: ""
};

//存已經選過的 讓他disabled
var expExist = [];

function fetch_element(){
        docField['email'] = document.getElementById('email').value
        docField['name'] = document.getElementById('name').value,
        docField['phone_number'] = document.getElementById('phone_number').value,
        docField['password'] = document.getElementById('password').value,
        docField['experience'] = document.getElementById('experience').value,
        docField['photo'] = document.getElementById('photo').files[0]
        // console.log('exoerience' + docField['exoerience']);
}

document.addEventListener('DOMContentLoaded', function() {
        //頁面加載後才能把這些element load進來
        const btnRegis = document.getElementById('btnDocRegis');
        const barTitle = document.getElementById('barTitle');
        const docForm = document.getElementById('doctorForm');
        const photoInput = document.getElementById('photo');
        const photoLabel = document.getElementById('photoLbl');
        const loginHide = document.querySelectorAll('.loginHide')
        const btnLogout = document.getElementById('logoutButton')
        fetch_element();
        fillFormFromLocalStorage(docForm);
        // 清空localstorage有關醫生註冊的東西
        // const doctorData = JSON.parse(localStorage.getItem('doctorData'));
        // const expertises = JSON.parse(localStorage.getItem('expertise_list'));
        // const working_hour_list = JSON.parse(localStorage.getItem('working_hour_list'));
        // const schedulingForm = JSON.parse(localStorage.getItem('schedulingForm'));
        // const clinicName = JSON.parse(localStorage.getItem('username'));
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            const value = localStorage.getItem(key);
            console.log(`${key}: ${value}`); // This loop iterates through all local storage, not just working hours
        }
        //canva11進入canva12   
        if (window.localStorage.getItem('user_type') == 'doctor'){
            barTitle.innerText = '醫生資料'
            btnRegis.innerText = '回到主頁'
            btnLogout.hidden = false;
            btnRegis.addEventListener('click', function(){
                window.location.href = "/clinic/home"
            })
            loginHide.forEach(element => {
                element.hidden = true;
            });
            fetch_info(docForm);
        }else if (window.localStorage.getItem('user_type') == 'clinic'){
            barTitle.innerText = '註冊'
            btnLogout.hidden = true;
            btnRegis.innerText = '完成'
            for (let i = 0; i < expExist.length; i++){
                const optionToEdit = document.querySelector(`#expertiseSelect option[value="${expertise}"]`);
                optionToEdit.disabled = true;
                optionToEdit.innerText = expertise + "(已選)";
            }
            if(window.localStorage.getItem('readyRegis') == 'yes'){
                // info_before_regis(docForm);
                photoInput.hidden = true;
                photoLabel.hidden = true;
            }
        }
})

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

// Fill form from local storage
function fillFormFromLocalStorage(form) {
    let storedData = localStorage.getItem('doctorData');
    if (storedData) {
        storedData = JSON.parse(storedData);
        fillForm(storedData, form);
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

//登入狀態從後端抓資料放到dataEdit
function fetch_info(formFilled){
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
            if (docInfo['photo'] != ''){
                docInfo['photo'] = '';
            }
            if (docInfo['password'] != ''){
                docInfo['password'] = '';
            }
            //console.log(clinInfo.photo_url)
            //console.log("info_type = " + typeof(data.data) + "  info = " + data.data)
            fillForm(docInfo, formFilled);
        } else {
            console.error(data.error);
        }
    })   
    .catch(error => {
        console.log('Error:', error);
    });
}

// //編輯完班表之後回到醫生註冊頁會出現的資料
// function info_before_regis(filledForm){
//     const doctorFormData = 
//     if (doctorFormData['photo'] != ''){
//         doctorFormData['photo'] = '';
//     }
//     doctorFormData['password'] = window.localStorage.getItem('password')
//     for (let i = 0; i < localStorage.length; i++) {
//         const key = localStorage.key(i);
//         const value = localStorage.getItem(key);
//         console.log(`${key}: ${value}`); // This loop iterates through all local storage, not just working hours
//         if(key == 'email'){
//             doctorFormData
//         }else if(key == 'name'){

//         }else if(key == 'phone_number'){

//         }else if(key =='password'){

//         }else if(key =='photo'){

//         }
//     }
//     // console.log(doctorFormData)
//     fillForm(doctorFormData, filledForm)
//     // fetch('/doc/session/', {
//     //     method: 'GET',
//     //     headers: {
//     //         'Content-Type': 'application/json',
//     //     },
//     // })
//     // .then(response => response.json())
//     // .then(data => {
//     //     //const doctorForm = document.getElementById('doctorForm');
        
//     // })
//     // .catch(error => {
//     //     console.error('Error fetching session data:', error);
//     // });
// }

document.getElementById('experForm').addEventListener('submit', async function(event){
    event.preventDefault();
    
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        const value = localStorage.getItem(key);
        if(key =='expertise_list'){
            console.log(`${key}: ${value}`);
        }
    }

    const expertise = document.getElementById('expertiseSelect').value;
    console.log("new selected exp: ", expertise)
    const newExpertise = {
        'name': expertise
    };
    let expertiseList = JSON.parse(localStorage.getItem('expertise_list')) || [];
    expertiseList.push(newExpertise);
    localStorage.setItem('expertise_list', JSON.stringify(expertiseList));

    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        const value = localStorage.getItem(key);
        if(key =='expertise_list'){
            console.log(`${key}: ${value}`);
        }
      }
    alert('Expertise added successfully!');
    expExist.push(expertise);
    const optionToEdit = document.querySelector(`#expertiseSelect option[value="${expertise}"]`);
    optionToEdit.disabled = true;
    optionToEdit.innerText = expertise + "(已選)"
})


async function isUniqueEmail(email){
    try {
        const response = await fetch('/isUniqueEmail_doc', {
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
        //alert('Error checking email availability');
        return false;
    }
}


document.getElementById('doctorForm').addEventListener('submit', async function(event){
    let isValid = false;
    // console.log("clicked regis")
    event.preventDefault(); // 防止user沒填必填資料
    
    //在這裡處理這些attribute的限制(不能default vlue.length...)
    //有任一項不符合就進到return; 不會繼續往下
    fetch_element();
    //email格式在html的type = 'email'就確認了
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
                    if(expExist.length == 0){
                        alert("Please first key in your expertise(s)")
                    }else{
                        isValid = true;
                    }
                }
            }
    }    
    if (isValid) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        window.localStorage.setItem('password', docField.password)
        // 發送 AJAX 請求
        fetch('/doc/upload/', {
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
                const localStorageData = data.localStorageData;
                // Store the JSON string in local storage
                localStorage.setItem('doctorData', localStorageData);
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    const value = localStorage.getItem(key);
                    console.log(`${key}: ${value}`);
                }
                // setTimeout(function(){console.log(data.info)}, 2000) 
                alert(data.message);
                window.localStorage.setItem('readyRegis', 'yes')
                window.location.href = '/click/schedule';
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

function clickRegis(event){
    event.preventDefault();
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
        const doctorData = JSON.parse(localStorage.getItem('doctorData'));
        const expertises = JSON.parse(localStorage.getItem('expertise_list'));
        const working_hour_list = JSON.parse(localStorage.getItem('working_hour_list'));
        const schedulingForm = JSON.parse(localStorage.getItem('schedulingForm'));
        const clinicName = JSON.parse(localStorage.getItem('username'));
        const requestData = {
            doctorData: doctorData,
            expertises: expertises,
            working_hour_list: working_hour_list,
            schedulingForm: schedulingForm,
            clinicName: clinicName
            // Add any other data you need to send in the request
        };
        console.log('requestData_doctorData:', doctorData)
        console.log('requestData_expertises: ', expertises)
        console.log('requestData_working_hour_list:', working_hour_list)
        console.log('requestData_schedulingForm: ', schedulingForm)
        console.log('requestData_clinicID: ', clinicName)

        if(window.localStorage.getItem('user_type') == 'clinic'){
            fetch('/add/doctor/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFTOKEN' : csrfToken
                },
                body: JSON.stringify({requestData}),
            })
            .then(async response => {
                if (!response.ok) {
                    throw new Error('Failed to add doctor');
                }
                const data = await response.json();
                // 处理成功响应，例如显示成功消息或重定向
                if(data.status == 'success'){
                    window.localStorage.setItem('readyRegis', 'no')
                    window.localStorage.setItem('password', '')
                    localStorage.removeItem('doctorData');
                    localStorage.removeItem('expertise_list');
                    localStorage.removeItem('working_hour_list');
                    localStorage.removeItem('schedulingForm');
                    alert('Doctor added successfully!');
                    window.location.href = '/doctor/manage';
                }else{
                    console.log('requestData:', requestData)
                    alert('Error : ' + data.message)
                }
            })
            .catch(error => {
                // 处理错误情况，例如显示错误消息给用户
                alert('Error adding doctor: ' + error.message);
            });
        }else if(window.localStorage.getItem('user_type') == 'doctor'){
            event.preventDefault()
            window.location.href = '/doctor/page'
        }
    } catch (error) {
        console.error('Error parsing JSON:', error.message);
        // Handle the parsing error gracefully (e.g., display an error message)
    }
    
}

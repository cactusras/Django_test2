
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
    docField['experience'] = document.getElementById('experience').value;
    if(window.localStorage.getItem('isLogin') == 'failed' && window.localStorage.getItem('readyRegis') == 'no'){
        docField['photo'] = document.getElementById('photo').files[0]
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
            if(key == 'password'){
                field.value = window.localStorage.getItem('password');
            }else{
                field.value = data[key];
            }
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

//登入狀態從後端抓資料放到dataEdit
async function fetch_info(formFilled) {
    try {
        const response = await fetch('/doctor_info/', {
            method: 'GET'
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        if (data.status === 'success') {
            const docInfo = data.data;
            if (docInfo['photo'] != '') {
                docInfo['photo'] = '';
            }
            // if (docInfo['password'] != ''){
            //     docInfo['password'] = '';
            // }
            const expertise_list = docInfo['expertises']; // Extract the expertises
            console.log("expertises: ", JSON.stringify(expertise_list));
            delete docInfo['expertises'];
            localStorage.setItem('expertise_list', JSON.stringify(expertise_list));
            console.log("stored: ", JSON.parse(localStorage.getItem('expertise_list')));
            localStorage.setItem('doctorData', JSON.stringify(docInfo));
            document.getElementById('emailShow').innerText = docInfo['email'];
            fillForm(docInfo, formFilled);
        } else {
            console.error(data.error);
        }
    } catch (error) {
        console.log('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', function(event) {
    event.preventDefault();
    //頁面加載後才能把這些element load進來
    const btnRegis = document.getElementById('btnClinPage');
    const barTitle = document.getElementById('barTitle');
    const docForm = document.getElementById('doctorForm');
    const photoInput = document.getElementById('photo');
    const photoLabel = document.getElementById('photoLbl');
    const loginHide = document.querySelectorAll('.loginHide');
    const btnLogout = document.getElementById('logoutButton');
    const emailShow = document.getElementById('emailShow');
    const expertiseSelect = document.getElementById('expertiseSelect');
    
    fetch_info(docForm).then(() => {
        console.log("after fetch_info");
        let expertiseList = JSON.parse(localStorage.getItem('expertise_list')) || [];
        expExist = expertiseList.map(exp => exp.name);
        console.log("localstorage_expertiseList: ", expertiseList);
        console.log("expExist", expExist);
        
        for (let i = 0; i < expertiseSelect.options.length; i++) {
            const option = expertiseSelect.options[i];
            if (expExist.includes(option.value)) {
                console.log("inner = " + option.innerText);
                option.innerText = option.innerText + " (已選)";
            }
        }
        
        if (window.localStorage.getItem('user_type') == 'doctor') {
            barTitle.innerText = '醫生資料';
            btnRegis.innerText = '回到主頁';
            btnLogout.hidden = false;
            btnRegis.addEventListener('click', function(){
                localStorage.removeItem('doctorData');
                localStorage.removeItem('expertise_list');
                localStorage.removeItem('working_hour_list');
                localStorage.removeItem('schedulingForm');
                window.location.href = "/doctor/page/";
            });
            loginHide.forEach(element => {
                if (element.tagName.toLowerCase() === 'label' || element.tagName.toLowerCase() === 'span') {
                    element.style.display = 'none';
                } else {
                    element.type = 'hidden';
                }
            });
            
        } else if (window.localStorage.getItem('user_type') == 'clinic') {
            barTitle.innerText = '註冊';
            btnLogout.hidden = true;
            btnRegis.innerText = '回管理/新增醫師';
            emailShow.style.display = 'none';
            btnRegis.addEventListener('click', function(){
                localStorage.removeItem('doctorData');
                localStorage.removeItem('expertise_list');
                localStorage.removeItem('working_hour_list');
                localStorage.removeItem('schedulingForm');
                window.location.href = "/doctor/manage/";
            });
            for (let i = 0; i < expExist.length; i++){
                const optionToEdit = document.querySelector(`#expertiseSelect option[value="${expExist[i]}"]`);
                optionToEdit.disabled = true;
                optionToEdit.innerText = expExist[i] + " (已選)";
            }
            if(window.localStorage.getItem('readyRegis') == 'yes'){
                photoInput.hidden = true;
                photoLabel.hidden = true;
                console.log('readyRegis');
            }
        }
        console.log("after second fetch");
        fillFormFromLocalStorage(docForm);
        fetch_element();
        // let expertiseList = JSON.parse(localStorage.getItem('expertise_list')) || [];
        // expExist = expertiseList.map(exp => exp.name);
        
        // for (let i = 0; i < expertiseSelect.options.length; i++) {
        //     const option = expertiseSelect.options[i];
        //     if (expExist.includes(option.value)) {
        //         // option.disabled = true;
        //         option.innerText = option.innerText + " (已選)";
        //     }
        // }
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            const value = localStorage.getItem(key);
            console.log(`${key}: ${value}`); // This loop iterates through all local storage, not just working hours
        }
    });
});



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
    const newExpertise = {
        'name': expertise
    };
    const select = document.getElementById('expertiseSelect');
    const selectedOption = select.options[select.selectedIndex];
    const text = selectedOption.text;
    console.log("text: ", text)
    let expertiseList = JSON.parse(localStorage.getItem('expertise_list')) || [];

    if (text.endsWith('(已選)')) {
        selectedOption.text = text.slice(0, -4).trim();
        console.log(text.slice(0, -5))
        expertiseList = expertiseList.filter(expertise => expertise.name !== text.slice(0, -5));
        localStorage.setItem('expertise_list', JSON.stringify(expertiseList));
        expExist = expExist.filter(name => name !== text.slice(0, -5));
    } else {
        selectedOption.text = `${text} (已選)`;
        expertiseList.push(newExpertise);
        localStorage.setItem('expertise_list', JSON.stringify(expertiseList));
        expExist.push(expertise);
        alert('Expertise added successfully!');
    }

    // selectedOption.innerText = expertise + "(已選)"

    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        const value = localStorage.getItem(key);
        if(key =='expertise_list'){
            console.log(`${key}: ${value}`);
        }
      }
})

document.getElementById('doctorForm').addEventListener('submit', async function(event){
    let isValid = false;
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
        const clinicName = localStorage.getItem('username');
        const user_type = localStorage.getItem('user_type');
        const requestData = {
            doctorData: doctorData,
            expertises: expertises,
            working_hour_list: working_hour_list,
            schedulingForm: schedulingForm,
            user_type: user_type,
            clinicName: ""
        };
        if (user_type == 'clinic'){
            requestData['clinicName'] = clinicName;
        }
        console.log('requestData_doctorData:', doctorData)
        console.log('requestData_expertises: ', expertises)
        console.log('requestData_working_hour_list:', working_hour_list)
        console.log('requestData_schedulingForm: ', schedulingForm)
        console.log('requestData_clinicID: ', clinicName)

        // if(window.localStorage.getItem('user_type') == 'clinic'){
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
                if(window.localStorage.getItem('user_type') == 'clinic'){
                    window.location.href = '/doctor/manage';
                }else if(window.localStorage.getItem('user_type') == 'doctor'){
                    window.location.href = '/doctor/page'
                }
            }else{
                console.log('requestData:', requestData)
                alert('Error : ' + data.message)
            }
        })
        .catch(error => {
            alert('Error adding doctor: ' + error.message);
        });
        // }else if(window.localStorage.getItem('user_type') == 'doctor'){
        //     event.preventDefault()
        //     window.location.href = '/doctor/page'
        // }
    } catch (error) {
        console.error('Error parsing JSON:', error.message);
    }
    
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

//這裡的fillForm有避免填入photo 且password是填入另創的localStorage(存沒有hash過的密碼)
// function fillForm(data, form) {
//     if (!form) {
//         console.error('Form not found');
//         return;
//     }

//     Object.keys(data).forEach(key => {
//         const field = form.querySelector(`[name=${key}]`);
//         if (field) {
//             if(key != 'photo'){
//                 if(key == 'password'){
//                     field.value = window.localStorage.getItem('password');
//                 }else{
//                     field.value = data[key];
//                 }
//             }    
//         }
//     });
// }

// async function isUniqueEmail(email){
//     try {
//         const response = await fetch('/isUniqueEmail_doc', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 //'X-CSRFToken': getCookie('csrftoken')
//             },
//             body: JSON.stringify({email: email})
//         });
//         const uniqueEmail = await response.json();
//         return uniqueEmail.isUnique;
//     } catch (error) {
//         console.log('Error fetching registered emails:', error);
//         //alert('Error checking email availability');
//         return false;
//     }
// }

// 清空localstorage有關醫生註冊的東西
        // const doctorData = JSON.parse(localStorage.getItem('doctorData'));
        // const expertises = JSON.parse(localStorage.getItem('expertise_list'));
        // const working_hour_list = JSON.parse(localStorage.getItem('working_hour_list'));
        // const schedulingForm = JSON.parse(localStorage.getItem('schedulingForm'));
        // const clinicName = JSON.parse(localStorage.getItem('username'));
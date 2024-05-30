
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
        clinField['address'] = document.getElementById('address').value,
        clinField['photo'] = document.getElementById('photo').files[0]
        console.log('phone_number' + clinField['phone_number']);
}

document.addEventListener('DOMContentLoaded', function() {
        //頁面加載後才能把這些element load進來
        const btnRegis = document.getElementById('btnClinRegis');
        const btnDocManage = document.getElementById('btnDocManage');
        const barTitle = document.getElementById('barTitle');
        fetch_element();

        //canva11進入canva12   
        if (window.isLogin){
            barTitle.innerText = '診所資料'
            btnDocManage.hidden = false;
            btnDocManage.addEventListener('click', function(){
                window.location.href = "doctor_management.html"
            })
            btnRegis.addEventListener('click', function(){
                window.location.href = "clinicPage.html"
            })
            fetch_info();
        }else{
            btnDocManage.hidden = true;
            barTitle.innerText = '註冊'
        }
})

/*function navBtn_listener(event){
    event.preventDefault();
    if (window.isLogin) {
        console.log("Navigating to clinic_dataEdit.html");
        window.location.href = "/clinic/data/edit";
    } else {
        console.log("login.html after 2 seconds");
        window.location.href = "/login";
    }
}*/

async function isUniqueLicense(license_number){
    try {
        const response = await fetch('/isUniqueLicense_clin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                //'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({email: email})
        });
        const uniqueLicense = await response.json();
        return uniqueLicense.isUnique;
    } catch (error) {
        console.log('Error fetching registered emails:', error);
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

function fetch_info(){
    fetch('/clinic_info/', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // 解析 JSON 响应
    })
    .then(infoDic =>{
        
        window.username = infoDic['name'];
        for (var key in infoDic) {
            if (infoDic.hasOwnProperty(key)) {
                //
                clinField[key] = infoDic[key];
            }
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
    //確認form中有必填沒被填上改成用html的required判斷
    /*if (Object.values(clinField).some(value => value == "" || value === undefined)){
        for (var [key, value] of Object.entries(clinField)) {
            //再找出沒被填到的元素
            if (value == "") {
                alert(`${key} must be filled in`);
                break;
                return;
            }else if(value === undefined){
                //只有photo可能是undefined型態
                alert(`You must add at least one photo`);
                return;
            }
        }        
    }*/
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
                alert(data.message);
                window.location.href = '/doctor/manage';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }

    /*const clinicForm = new FormData(document.getElementById("clinicForm"));

    //html元素name == elements[]中的name == model中的attribute name
    // 发送 POST 请求到 Django 后端视图
    fetch('/clinic_dataEdit/add_clinic/', {
        method: 'POST',
        body: JSON.stringify(clinField),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // 如果后端返回 JSON 数据，则解析
    })
    .then(data => {
        console.log('Success:', data);
        window.location.href = "clinic_dataEdit.html";
        // 到login之後要有一個變數辨認診所是否為第一次登入 是的話就進clinic_login_docManage
    })
    .catch(error => {
        console.log('Error:', error);
        // 处理错误情况，例如显示错误消息给用户
    });*/
});
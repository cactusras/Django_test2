var clieField = {
    email:"",
    name: "",
    phone_number: "",
    password: "",
    address: "",
    birth_date: new Date(),
    gender: "",
    occupation: "",
    notify: true,
};

function checkVlue(){
    const isNotify =  document.getElementById('notify');
    if (isNotify.checked){
        isNotify.value = true;
        return true;
    }else{
        isNotify.value = false
        return false;
    }
}

function fetch_element(){
        clieField['email'] = document.getElementById('email').value
        clieField['name'] = document.getElementById('name').value,
        clieField['phone_number'] = document.getElementById('phone_number').value,
        clieField['password'] = document.getElementById('password').value,
        clieField['address'] = document.getElementById('address').value,
        clieField['birth_date'] = document.getElementById('birth_date').value
        clieField['gender'] = document.getElementById('gender').value
        clieField['occupation'] = document.getElementById('occupation').value
        clieField['notify'] = checkVlue();
        console.log('notify' + clieField['notify']);
        console.log('gender' + clieField['gender']);
}

document.addEventListener('DOMContentLoaded', function() {
        //頁面加載後才能把這些element load進來
        const btnRegis = document.getElementById('btnClieRegis');
        const barTitle = document.getElementById('barTitle');
        fetch_element();

        //canva11進入canva12   
        if (window.isLogin){
            barTitle.innerText = '患者資料'
            btnRegis.addEventListener('click', function(){
                window.location.href = "clinicPage.html"
            })
            fetch_info();
        }else{
            barTitle.innerText = '註冊'
        }
})

/*function navBtn_listener(event){
    event.preventDefault();
    if (window.isLogin) {
        console.log("Navigating to clinic_dataEdit.html");
        window.location.href = "/client/data/edit";
    } else {
        console.log("login.html after 2 seconds");
        window.location.href = "/login";
    }
}*/

async function isUniqueEmail(email){
    try {
        const response = await fetch('/isUniqueEmail_clie/', {
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

//是抓後端存著的資料
function fetch_info(){
    fetch('/client_info/', {
        method: 'GET'
    })
    .then(async response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();

        if (data.status === 'success') {
            const doctorInfo = data.info;
            fillForm(doctorInfo);
        } else {
            console.error(data.error);
        }
    })   
    .catch(error => {
        console.log('Error:', error);
    });
}

document.getElementById('clientForm').addEventListener('submit', async function(event){
    let isValid = false;
    console.log("clicked regis")
    event.preventDefault(); // 防止user沒填必填資料
    
    //在這裡處理這些attribute的限制(不能default vlue.length...)
    //有任一項不符合就進到return; 不會繼續往下
    fetch_element();
    //email格式在html的type = 'email'就確認了
    if (clieField.name.length > 100) {
        alert("Name cannot exceed 100 characters");
        return;
    } else {
            if (!(/^\d+$/.test(clieField.phone_number))) {
                alert("Phone number can only contain digits");
                return;
            } else {
                if (clieField.phone_number.length > 15) {
                    alert("Phone number cannot exceed 15 digits");
                    return;
                } else {
                    // 要串資料庫把所有的clinic email先找出來      
                    if (!await isUniqueEmail(clieField.email)) {
                        alert("Email already registered");
                        return;
                    }else{
                        isValid = true;
                    }
                }
            }
    }  
    
    if(isValid){
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // 發送 AJAX 請求
        fetch('/add/client/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(clieField)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
                window.location.href = '/home';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }

   /* const clientForm = new FormData(document.getElementById("clientForm"));

    //html元素name == elements[]中的name == model中的attribute name
    // 发送 POST 请求到 Django 后端视图
    fetch('/client/add_client/', {
        method: 'POST',
        body: JSON.stringify(clieField),
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
        window.location.href = "client_dataEdit.html";
        // 到login之後要有一個變數辨認診所是否為第一次登入 是的話就進clinic_login_docManage
    })
    .catch(error => {
        console.log('Error:', error);
        // 处理错误情况，例如显示错误消息给用户
    });*/
});
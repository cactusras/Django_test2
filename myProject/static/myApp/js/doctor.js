    var docField = {
        email:"",
        name: "",
        phone_number: "",
        pw: "",
        photo: null,
        experience: ""
    };
    
    function fetch_element(){
            docField['email'] = document.getElementById('email').value
            docField['name'] = document.getElementById('name').value,
            docField['phone_number'] = document.getElementById('phone_number').value,
            docField['pw'] = document.getElementById('pw').value,
            docField['experience'] = document.getElementById('experience').value,
            docField['photo'] = document.getElementById('photo').files[0]
            console.log('name' + docField['name']);
    }

    /*function toSchedule(event){
        event.preventDefault();
        window.location.href = '/click/schedule'
    }*/
    
    document.addEventListener('DOMContentLoaded', function() {
            //頁面加載後才能把這些element load進來
            const btnRegis = document.getElementById('btnDocRegis');
            const barTitle = document.getElementById('barTitle');
            fetch_element();
    
            //canva11進入canva12   
            if (window.isLogin){
                barTitle.innerText = '醫生資料'
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
            window.location.href = "/doctor_dataEdit";
        } else {
            console.log("login.html after 2 seconds");
            window.location.href = "/login";
        }
    }*/
    
    async function isUniqueEmail(email){
        try {
            const response = await fetch('/clinic/isUniqueEmail_clin/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
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
    
    function fetch_info(){
        fetch('/doctor/doctor_info/', {
            method: 'GET'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // 解析 JSON 响应
        })
        .then(infoDic =>{
            username = infoDic['name'];
            for (var key in infoDic) {
                if (infoDic.hasOwnProperty(key)) {
                    //
                    docField[key] = infoDic[key];
                }
            }
        })   
        .catch(error => {
            console.log('Error:', error);
        });
    }
    
    async function clickRegis(){
        fetch('/add/doctor/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
        })
        .then(async response => {
            if (!response.ok) {
                throw new Error('Failed to add doctor');
            }
            const data = await response.json();
            // 处理成功响应，例如显示成功消息或重定向
            alert('Doctor added successfully!');
            window.location.href = '/doctor/manage';
        })
        .catch(error => {
            // 处理错误情况，例如显示错误消息给用户
            alert('Error adding doctor: ' + error.message);
        });
    }

    document.getElementById('doctorForm').addEventListener('submit', async function(event){
        let isValid = false;
        console.log("clicked regis")
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
                        // 要串資料庫把所有的clinic email先找出來      
                        if (await isUniqueEmail(email)) {
                            alert("Email already registered");
                            return;
                        }else{
                            isValid = true;
                        }
                    }
                }
        }    
        if (isValid) {
            document.getElementById('doctorForm').submit();
            window.location.href = '/click/schedule'
        }
    
        /*const doctorForm = new FormData(document.getElementById("doctorForm"));
    
        //html元素name == elements[]中的name == model中的attribute name
        // 发送 POST 请求到 Django 后端视图
        fetch('/doctor/add_doctor/', {
            method: 'POST',
            body: JSON.stringify(docField),
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
            window.location.href = "doctor_dataEdit.html";
            // 到login之後要有一個變數辨認診所是否為第一次登入 是的話就進clinic_login_docManage
        })
        .catch(error => {
            console.log('Error:', error);
            // 处理错误情况，例如显示错误消息给用户
        });*/
    });
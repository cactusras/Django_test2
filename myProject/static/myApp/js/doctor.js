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
            console.log('email' + docField['email']);
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
            if (window.localStorage.getItem('isLogin') == 'success'){
                barTitle.innerText = '醫生資料'
                btnRegis.addEventListener('click', function(){
                    window.location.href = "/clinic/home"
                })
                fetch_info();
            }else if (window.localStorage.getItem('isLogin') == 'failed'){
                barTitle.innerText = '註冊'
            }
    })
    
    /*function click_regis(event){
        event.preventDefault();
        if (window.localStorage.getItem('isLogin') == 'success') {
            window.location.href = "/doctor_dataEdit";
        } else if(window.localStorage.getItem('isLogin') == 'failed'){
            window.location.href = "/login";
        }
    }*/
    
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
   
   
    document.getElementById('experForm').addEventListener('submit', async function(event){
        event.preventDefault();
        const expertise = document.getElementById('expertiseSelect').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const data = {
            expertise: expertise
        };

        fetch(`/doc/expertise/upload/`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(async response => {
            if (!response.ok) {
                throw new Error('Failed to add doctor');
            }
            const data = await response.json();
            // 处理成功响应，例如显示成功消息或重定向
            alert('Expertise added successfully!');
            expExist.push(expertise);
            const optionToEdit = document.querySelector(`#expertiseSelect option[value="${expertise}"]`);
            optionToEdit.disabled = true;
            optionToEdit.innerText = expertise + "(已選)"

            console.log("expExist = " + expExist + expExist.length);
            console.log(data.exp)
            //window.location.href = '/doctor/data/edit';
        })
        .catch(error => {
            console.error('Error fetching expertise list:', error);
            // 处理错误情况
        });
    })

    

    //登入狀態從後端抓資料放到dataEdit
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
    
    //編輯完班表之後回到醫生註冊頁會出現的資料
    function info_before_regis(){
        fetch('/doc/session/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            const doctorForm = document.getElementById('doctorForm');
            const doctorFormData = data.doctor_form_data;
            for (const [key, value] of Object.entries(doctorFormData)) {
                const field = doctorForm.querySelector(`[name="${key}"]`);
                if (field) {
                    field.value = value;
                }
            }
        })
        .catch(error => {
            console.error('Error fetching session data:', error);
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
                        if(expExist.length == 0){
                            alert("Please first key in your expertise(s)")
                        }else{
                            isValid = true;
                        }
                        // 要串資料庫把所有的clinic email先找出來      
                        /*if (!await isUniqueEmail(docField.email)) {
                            alert("Email already registered");
                            return;
                        }else{
                            if(expExist.length == 0){
                                alert("Please first key in your expertise(s)")
                            }else{
                                isValid = true;
                            }
                        }*/
                    }
                }
        }    
        if (isValid) {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
                    setTimeout(function(){console.log(data.info)}, 2000) 
                    alert(data.message);
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

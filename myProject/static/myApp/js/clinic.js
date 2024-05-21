document.addEventListener('DOMContentLoaded', function() {

    //頁面加載後才能把這些element load進來
    btnRegis = document.getElementById('btnClinRegis');
    btnDocManage = document.getElementById('btnDocManage');
    btnNav = document.getElementById('nav_btn');
    barTitle = document.getElementById('barTitle');
    var clinField = {
        //email: document.getElementById('email').value,
        name: document.getElementById('name').value,
        phone_number: document.getElementById('phone_number').value,
        license_number: document.getElementById('license_number').value,
        pw: document.getElementById('pw').value,
        address: document.getElementById('address').value,
        photo: document.getElementById('photo').files[0]
    };
    var username = "";

    //canva11進入canva12   
    if (window.isLogin === true){
        barTitle.innerText = '診所資料'
        btnDocManage.hidden = false;
        btnDocManage.addEventListener('click', function(){
            window.location.href = "doctor_management.html"
        })
        btnRegis.innerText = '回到主頁';
        btnRegis.addEventListener('click', function(){
            window.location.href = "clinicPage.html"
        })
        fetch_info();
        nav_btn.innerText = username;
        nav_btn.addEventListener('click', function(){
            window.location.href = "clinic_dataEdit.html"
        })
    }else{
        btnDocManage.hidden = true;
        nav_btn.innerText = '登入'
        barTitle.innerText = '註冊'
    }
    

    // Register
    btnRegis.addEventListener('submit', async function(event) {
        console.log("clicked")
        event.preventDefault(); // 防止user沒填必填資料
        //將所有已註冊的clinic信箱集合起來 判斷是否為unique
        let registeredEmails = [];
        try {
            const response = await fetch('/clinic/emails/');
            if (!response.ok) {
                console.log('Network response was not ok')
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            registeredEmails = data.emails;
            console.log('emailLens =  '+ registeredEmails.length)
        } catch (error) {
            console.log('Error fetching registered emails:', error);
            alert('Error checking email availability');
            return;
        }

        //將所有已註冊的clinic license number集合起來 判斷是否為unique
        let existLicense = [];
        try {
            const response = await fetch('/clinic/licenses/');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            existLicense = data.licenses;
        } catch (error) {
            console.log('Error fetching registered licenses:', error);
            alert('Error checking license availability');
            return;
        }
        
        //在這裡處理這些attribute的限制(不能default vlue.length...)
        //有任一項不符合就進到return; 不會繼續往下

        //先確認form中有必填沒被填上
        if (Object.values(clinField).some(value => value == "" || value === undefined)){
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
        }else{
            //email格式在html的type = 'email'就確認了
            if (clinField.name.length > 100) {
                alert("Name cannot exceed 100 characters");
                return;
            } else {
                    if (/^\d+$/.test(clinField.phone_number)) {
                        alert("Phone number can only contain digits");
                        return;
                    } else {
                        if (clinField.phone_number.length > 15) {
                            alert("Phone number cannot exceed 15 digits");
                            return;
                        } else {
                            // 要串資料庫把所有的clinic email先找出來      
                            if (registeredEmails.includes(clinField.email)) {
                                alert("Email already registered");
                                return;
                            }
                        }
                    }
            }    
        }

        const clinicForm = new FormData(document.getElementById("clinicForm"));

        //html元素name == elements[]中的name == model中的attribute name
        // 发送 POST 请求到 Django 后端视图
        fetch('/clinRegis/', {
            method: 'POST',
            body: JSON.stringify(clinField),
            headers: {
                'Content-Type': 'application/json'
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
        });
    });


    function fetch_info(){
        fetch('/clinic/add_clinic/', {
            method: 'GET'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // 解析 JSON 响应
        })
        .then(infoDic =>{
            clinField['introduction'] = document.getElementById('introductioin').value;
            username = infoDic['name'];
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
})

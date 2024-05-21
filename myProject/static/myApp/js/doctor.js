// 醫生註冊eventListener
//要跟診所合併
document.getElementById('btnDocRegis').addEventListener('submit', async function(event) {
    event.preventDefault(); // 防止user沒填必填資料
    
    const docField = {
        email: document.getElementById('email').value,
        name: document.getElementById('name').value,
        phone_number: document.getElementById('phone_number').value,
        pw: document.getElementById('pw').value,

        //看expertise需不需要在這裡驗證(可能連提交都不是同一筆)
        expertise: document.getElementById('expertise').value,
    };

    let registeredEmails = [];
    try {
        const response = await fetch('/doctor/emails/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        registeredEmails = data.emails;
    } catch (error) {
        console.log('Error fetching registered emails:', error);
        alert('Error checking email availability');
        return;
    }
    
    //在這裡處理這些attribute的限制(不能default vlue.length...)要用const變數名

    //expertise要跟doctorForm中的變數分開處理不可為null嗎(要的話要從docField移掉)
    if (Object.values(docField).some(value => value == "")){
        for (const [key, value] of Object.entries(docField)) {
            if (value == "") {
                alert(`${key} must be filled in`);
                break;
                return;
            }
        }        
    }else{
        if (docField.name.length > 100) {
            alert("Name cannot exceed 100 characters");
            return;
        } else {
            if (!docField.email.includes("@")) {
                alert("Email format is incorrect");
                return;
            } else {
                if (/^\d+$/.test(docField.phone_number)) {
                   alert("Phone number can only contain digits");
                   return;
                } else {
                    if (docField.phone_number.length > 15) {
                        alert("Phone number cannot exceed 15 digits");
                        return;
                    } else {      
                        if (registeredEmails.includes(clinField.email)) {
                            // User successfully registered
                            alert("Email already registered");
                            return;
                        }
                    }
                }
            }
        }    
    }

    const doctorForm = new FormData(document.getElementById("doctorForm"));

    //html元素name == elements[]中的name == model中的attribute name

    // 发送 POST 请求到 Django 后端views.py
    fetch('/docRegis/', {
        method: 'POST',
        body: JSON.stringify(docField),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        window.location.href = "doctor_management.html";
    })
    .catch(error => {
        console.log('Error:', error);
    });
});


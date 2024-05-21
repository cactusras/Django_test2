// Register
document.getElementById('btnClieRegis').addEventListener('submit', async function(event) {
    event.preventDefault(); // 防止user沒填必填資料
    
    const occupation = document.getElementById('occupation').value
    const clieField = {
        email: document.getElementById('email').value,
        name: document.getElementById('name').value,
        phone_number: document.getElementById('phone_number').value,
        birth_date: document.getElementById('birth_date').value,
        pw: document.getElementById('pw').value,
        gender: document.getElementById('gender').value,
    };

    let registeredEmails = [];
    try {
        const response = await fetch('/client/emails/');
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
    
    //在這裡處理這些attribute的限制(不能default vlue.length...)
    //有任一項不符合就進到return; 不會繼續往下

    //先確認form中有必填沒被填上
    if (Object.values(clieField).some(value => value == "" || value === undefined)){
        for (const [key, value] of Object.entries(clieField)) {
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
        if (clieField.name.length > 100) {
            alert("Name cannot exceed 100 characters");
            return;
        } else {
                if (/^\d+$/.test(clieField.phone_number)) {
                    alert("Phone number can only contain digits");
                    return;
                } else {
                    if (clieField.phone_number.length > 15) {
                        alert("Phone number cannot exceed 15 digits");
                        return;
                    } else {
                        // 要串資料庫把所有的clinic email先找出來
                        const emailExists = false; // Replace with actual check       
                        if (emailExists) {
                            alert("Email already registered");
                            return;
                        }
                    }
                }
        }    
    }

    const clientForm = new FormData(document.getElementById("clientForm"));

    //html元素name == elements[]中的name == model中的attribute name

    // 发送 POST 请求到 Django 后端视图
    fetch('/clieRegis/', {
        method: 'POST',
        //將資料轉成json型態
        body: JSON.stringify(clieField),
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
        //data = 'Client registered successfully'
        console.log('Success:', data);
        window.location.href = "searchPage.html";
    })
    .catch(error => {
        console.log('Error:', error);
        // 处理错误情况，例如显示错误消息给用户
    });
});
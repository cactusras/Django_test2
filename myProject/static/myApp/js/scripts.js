// http://jsonblob.com/1221767613406633984
/*function displayUsers(users) {
    var usersElement = document.getElementById("users");
    var str = "";
   
    // Iterate through each user
    users.forEach((user) => (str += user.name + " : " + user.email + "<br>"));
    usersElement.innerHTML = str;
}
function getUsers() {
    axios
    .get("https://jsonblob.com/api/jsonBlob/1222775686480912384")
    .then(function (response) {
    displayUsers(response.data);
    })
    .catch(function (error) {
    console.error("Error fetching users:", error);
    });
}
// Call the getUsers function when the window loads
window.onload = getUsers;*/


/*
$('#date1').datetimepicker({
  date:null,
    format: 'YYYY-MM-DD',
    locale: moment.locale('zh-tw'),
    daysOfWeekDisabled: [0, 6],
    minDate: moment().add(1,'days'),
    maxDate: moment().add(30,'days'),
    disabledDates: [
      moment().add(1,'days'),
      moment().add(2,'days'),
      '2021-10-10',
      '2021-12-25'
    ]
});*/

  //fetch使用者是否登入了 並設window變數(整個project都可取得)
//window.isLogin = "";


document.addEventListener('DOMContentLoaded', function() {
  const btnNav = document.getElementById('nav_btn');
  const barTitle = document.getElementById('barTitle');
  //const btnDocManage = document.getElementById('btnDocManage')
  const btnLogout = document.getElementById('logoutButton')

  fetch('/check_authentication/')
  .then(response => {
      if (response.ok) {
          return response.json();
      } else {
          throw new Error('Network response was not ok');
      }
  })
  .then(data => {
      if (data.is_authenticated) {
<<<<<<< HEAD
        //console.log(data.username)
=======
>>>>>>> frontback
        window.localStorage.setItem('isLogin', 'success')
        console.log('loginYes')
        btnNav.innerText = window.localStorage.getItem('username');
        btnLogout.hidden = false;
      }else{
        window.localStorage.setItem('isLogin', 'failed')
        console.log('loginNo')
        btnNav.innerText = '登入';
        barTitle.innerText = "註冊"
        btnLogout.hidden = true;
      }
      document.dispatchEvent(new CustomEvent('authChecked', { detail: window.isLogin }));
  })
  .catch(error => {
      console.log('Error checking authentication:', error);
  });
})
  
function navBtn_listener(event){
  event.preventDefault();
<<<<<<< HEAD
  console.log("click nav_btn")
=======
>>>>>>> frontback
  if (window.localStorage.getItem('isLogin') == 'success') {
    let usertype = window.localStorage.getItem('user_type')
    if(usertype == 'client'){
      window.location.href = '/client/data/edit'
    }else if(usertype == 'clinic'){
      window.location.href = '/clinic/data/edit'
    }else if(usertype == 'doctor'){
      window.location.href = '/doctor/data/edit'
    }
  }else if(window.localStorage.getItem('isLogin') == 'failed'){
    window.location.href = '/loginP'
  }
<<<<<<< HEAD
  /*fetch('/fetch/user_type/')
  .then(response => {
      if (response.ok) {
          return response.json();
      } else {
          throw new Error('Network response was not ok');
      }
  })
  .then(data => {
      if (data.isLogin == 'success') {
        if(data.user_type == 'client'){
          window.location.href = '/client/data/edit'
        }else if(data.user_type == 'clinic'){
          window.location.href = '/clinic/data/edit'
        }else if(data.user_type == 'doctor'){
          window.location.href = '/doctor/data/edit'
        }
      }else{
        window.location.href = '/loginP'
      }
  })
  .catch(error => {
      console.log('Error checking authentication:', error);
  });*/
=======
>>>>>>> frontback
}
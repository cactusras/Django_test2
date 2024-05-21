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

function Linyi(){
    
}

function julieTest3(){
    
}

function wntng(){

}

function Linyi2(){
    
}
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
window.isLogin = false;
document.addEventListener('DOMContentLoaded', function() {
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
          isLogin = true;
          console.log("isLogin = true");
      }else{
        console.log("isLogin = false");
      }
  })
  .catch(error => {
      console.log('Error checking authentication:', error);
  });
})
  
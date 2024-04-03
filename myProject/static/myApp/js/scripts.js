// http://jsonblob.com/1221767613406633984
function displayUsers(users) {
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
window.onload = getUsers;

function jasmine(){
    
}

function wntng(){

}
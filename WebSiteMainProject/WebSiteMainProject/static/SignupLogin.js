function checkLogin() {
    alert('success!');
    if (check_username() && check_password()) {
        alert('success!');
    } else {
        alert('you stupid!');
    }
    return check_username() && check_password();
}
function checkSignup() {
    if (check_username() && check_password()) {
        document.getElementById("signupForm").submit();
    }
}

//document.getElementById("loginForm").addEventListener("submit", function (event) {
//    event.preventDefault(); // Prevent form submission
//    check_username();
//});

function check_username() {
    let username = document.getElementById("username").value;
    if ((!!username.match(/^[a-zA-Z0-9]*$/)) && username.length > 3) {
        return true;
    } else {
        let err = '';
        if (username.length < 3) {
            err = "must have more then 3 characters";
        } else {
            err = "use only leagal characters";
        }
        document.getElementById("errUsername").innerHTML = err;
        return false;
    }
}
function check_password() {
    let password = document.getElementById("password").value
    if ((!!password.match(/^[a-zA-Z0-9]*$/)) && password.length > 6
        && password.length <= 12 && password.match(/[A-Z]/i)
        && password.match(/[0-9]/i) && password.match(/[!@#$%^&*(),.?":{}|<>]/g)) {
        return true;
    }
    return false;
}
function check_password_clone() {
    return document.getElementById('password').value == document.getElementById('passwordClone').value;
}
function check_email() {

}
function check_phone() {

}
function check_first_last_names() {

}

function load_element_list(list) {
    let return_list = [];
    for (let element in list) {
        return_list.push(element);
    }
    return return_list;
}
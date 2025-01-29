function check_signin() {

}

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
    let password = document.getElementById("password").value;
    let err = '';

    if (password.length <= 6) {
        err = "Password must be longer than 6 characters.";
    } if (password.length > 12) {
        err = "Password must be 12 characters or less.";
    } if (!password.match(/[A-Z]/)) {
        err = "Password must contain at least one uppercase letter.";
    } if (!password.match(/[0-9]/)) {
        err = "Password must contain at least one digit.";
    } if (!password.match(/[!@#$%^&*(),.?":{}|<>]/)) {
        err = "Password must contain at least one special character.";
    } if (err) {
        document.getElementById("errPassword").innerText = err;
    } else {
        document.getElementById("errPassword").innerText = '';
    }
    return !err;
}

function check_password_clone() {
    if (document.getElementById("password").value === document.getElementById("passwordClone").value) {
        return true;
    }
    document.getElementById("errPasswordClone");
}

function check_email() {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (pattern.test(document.getElementById())) {
        return true;
    }

}
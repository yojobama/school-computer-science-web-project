function login_final() {
    return check_username() && check_password();
}

function check_password() {
    let password = document.getElementById("password").value;
    let error = document.getElementById("passwordErr");
    let specialCharPattern = /[^a-zA-Z0-9]/; // Any non-alphanumeric character
    let bigLetterPattern = /[A-Z]/; // Any uppercase letter
    let invalidCharPattern = /[\u0590-\u05FF\s]/; // Hebrew characters and spaces

    if (!password) {
        error.innerHTML = "Password can not be empty";
        return false;
    } else if (password.length > 12) {
        error.innerHTML = "Password must be at most 12 characters long";
        return false;
    } else if (password.length < 6) {
        error.innerHTML = "Password must be at least 6 characters long";
        return false;
    } else if (!specialCharPattern.test(password)) {
        error.innerHTML = "Password must contain at least one special character";
        return false;
    } else if (!bigLetterPattern.test(password)) {
        error.innerHTML = "Password must contain at least one uppercase letter";
        return false;
    } else if (invalidCharPattern.test(password)) {
        error.innerHTML = "Password can not contain Hebrew characters or spaces";
        return false;
    }
    error.innerHTML = "";
    return true;
}

function check_username() {
    let username = document.getElementById("username").value;
    let error = document.getElementById("usernameErr");
    let pattern = /^[a-zA-Z0-9]+$/;

    if (!username) {
        error.innerHTML = "Username cannot be empty";
        return false;
    }
    else if (username.length < 3) {
        error.innerHTML = "Username must be at least 3 characters long";
        return false;
    } else if (!pattern.test(username)) {
        error.innerHTML = "Username can only contain numbers or Latin letters";
        return false;
    } else if (username.trim() !== username) {
        error.innerHTML = "Username cannot contain spaces";
        return false;
    }
    error.innerHTML = ""; // Clear any previous error message
    return true;
}

function signup_final() {
    return check_username() &&
        check_password() &&
        check_password_copy() &&
        check_first_name() &&
        check_last_name() &&
        check_email();
}

function check_username() {
    let username = document.getElementById("username").value;
    let error = document.getElementById("usernameErr");
    let pattern = /^[a-zA-Z0-9]+$/;
    if (!username) {
        error.innerHTML = "Username can not be empty";
        return false;
    }
    else if (username.length < 3) {
        error.innerHTML = "Username must be at least 3 characters long";
        return false;
    } else if (!pattern.test(username)) {
        error.innerHTML = "Username can only contain numbers or latin letters";
        return false;
    } else if (username.trim() !== username) {
        error.innerHTML = "Username can not contain spaces";
        return false;
    }
    error.innerHTML = "";
    return true;
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

function check_password_copy() {
    let password = document.getElementById("password").value;
    let passwordCopy = document.getElementById("passwordCopy").value;
    let error = document.getElementById("passwordCopyErr");
    if (password !== passwordCopy) {
        error.innerHTML = "Passwords do not match";
        return false;
    }
    error.innerHTML = "";
    return true;
}

function check_first_name() {
    let firstName = document.getElementById("firstName").value;
    let error = document.getElementById("firstNameErr");
    if (!firstName) {
        error.innerHTML = "First name can not be empty";
        return false;
    } else if (firstName.length < 2) {
        error.innerHTML = "First name must be at least 2 characters long";
        return false;
    }
    error.innerHTML = "";
    return true;
}

function check_last_name() {
    let lastName = document.getElementById("lastName").value;
    let error = document.getElementById("lastNameErr");
    if (!lastName) {
        error.innerHTML = "Last name can not be empty";
        return false;
    } else if (lastName.length < 2) {
        error.innerHTML = "Last name must be at least 2 characters long";
        return false;
    }
    error.innerHTML = "";
    return true;
}

function check_email() {
    let email = document.getElementById("email").value;
    let error = document.getElementById("emailErr");
    let pattern = /^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$/;
    if (!email) {
        error.innerHTML = "Email can not be empty";
        return false;
    } else if (!pattern.test(email)) {
        error.innerHTML = "Email is not in the correct format (ie 'myEmail@stuff.thingy')";
        return false;
    }
    error.innerHTML = "";
    return true;
}

////////////////////SIGN_UP///////////////////////////

function signUp() {
    var Fname = document.getElementById("firstname").value;
    var Lname = document.getElementById("lastname").value;
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password").value;
    var accountType = document.querySelector('input[name="Type"]:checked').value;

    if (Fname === "" || Lname === "" || username === "" || email === "" || password === "" || confirmPassword === "" || !accountType) {
        alert("Please fill in all fields and select the account type.");
        return false;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }
    
    var users = JSON.parse(localStorage.getItem('users')) || [];
    
    // Check if username or email already exist
    var existingUser = users.find(function(user) {
        return user.un === username || user.e === email;
    });
    
    if (existingUser) {
        alert("Username or email already exists. Please choose a different username and email.");
        return false;
    }

    var user = {
        first: Fname,
        last: Lname,
        un: username,
        e: email,
        pass: password,
        type: accountType
    };

    users.push(user);
    localStorage.setItem('users', JSON.stringify(users));

    if (accountType === "User") {
        window.location.replace("User_home_page.html");
    } else if (accountType === "Admin") {
        window.location.replace("Admin_home_page.html");
    }

    return false;
}

////////////////////LOG_IN///////////////////////////

function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var remember = document.getElementById("remember").checked;

    if (username === "" || password === "") {
        alert("Please enter both username and password.");
        return;
    }

    var users = JSON.parse(localStorage.getItem('users')) || [];

    var user = users.find(function (user) {
        return user.un === username;
    });

    if (user) {
        if (user.pass === password) {
            var accountType = user.type;

            if (accountType === "User") {
                alert('Welcome back, ' + username);
                window.location.replace("User_home_page.html");
            } else if (accountType === "Admin") {
                alert('Welcome back, ' + username);
                window.location.replace("Admin_home_page.html");
            }
        } else {
            alert("Incorrect password. Please try again.");
        }
    } else {
        alert("Username is not signed up. Please sign up first.");
    }
}

// //////////////////////////////
// const logoutBtn = document.querySelector(".logout-btn")

// logoutBtn.addEventListener("click", () => {
//     window.location.replace("Home_page.html")
// })
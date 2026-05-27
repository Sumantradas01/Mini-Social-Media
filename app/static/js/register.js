const passwordInput = document.getElementById("password");
const strengthFill = document.getElementById("strengthFill");
const togglePassword = document.getElementById("togglePassword");

passwordInput.addEventListener("input", () => {

    const value = passwordInput.value;
    let strength = 0;

    if(value.length >= 8) strength += 25;
    if(/[A-Z]/.test(value)) strength += 25;
    if(/[0-9]/.test(value)) strength += 25;
    if(/[^A-Za-z0-9]/.test(value)) strength += 25;

    strengthFill.style.width = strength + "%";
});

togglePassword.addEventListener("click", () => {

    if(passwordInput.type === "password"){
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }

});
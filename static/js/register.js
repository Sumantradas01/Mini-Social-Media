
// FORM SWITCH

function showRegister() {

  document.getElementById("loginForm").style.display = "none";

  document.getElementById("registerForm").style.display = "block";
}

function showLogin() {

  document.getElementById("registerForm").style.display = "none";

  document.getElementById("loginForm").style.display = "block";
}

// PASSWORD TOGGLE

function togglePassword(id) {

  const input = document.getElementById(id);

  if(input.type === "password"){
    input.type = "text";
  }
  else{
    input.type = "password";
  }
}

// PASSWORD STRENGTH

const passwordInput = document.getElementById("password");

if(passwordInput){

  passwordInput.addEventListener("input", () => {

    const password = passwordInput.value;

    let strength = 0;

    const hasLength = password.length >= 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    updateRule("rule-length", hasLength);
    updateRule("rule-uppercase", hasUppercase);
    updateRule("rule-number", hasNumber);
    updateRule("rule-special", hasSpecial);

    if(hasLength) strength += 25;
    if(hasUppercase) strength += 25;
    if(hasNumber) strength += 25;
    if(hasSpecial) strength += 25;

    const strengthBar = document.getElementById("strength-bar");

    strengthBar.style.width = strength + "%";

    if(strength <= 25){
      strengthBar.style.background = "#ff4d4d";
    }
    else if(strength <= 50){
      strengthBar.style.background = "#ff944d";
    }
    else if(strength <= 75){
      strengthBar.style.background = "#ffd11a";
    }
    else{
      strengthBar.style.background = "#00cc66";
    }

  });

}

function updateRule(id, valid){

  const element = document.getElementById(id);

  if(valid){

    element.innerHTML =
      "✅ " + element.innerHTML.substring(2);

    element.style.color = "#00cc66";
  }
  else{

    element.innerHTML =
      "❌ " + element.innerHTML.substring(2);

    element.style.color = "#ff4d4d";
  }
}


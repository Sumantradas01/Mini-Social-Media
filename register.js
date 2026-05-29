
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

// PHONE VALIDATION

const phoneInput =
document.getElementById("phone");

if(phoneInput){

phoneInput.addEventListener(
"input",
function(){

this.value =
this.value.replace(/\D/g,'');

if(this.value.length > 10){
this.value =
this.value.slice(0,10);
}

});
}


// AGE CALCULATOR

const dobInput =
document.getElementById("dob");

if(dobInput){

dobInput.addEventListener(
"change",
function(){

const dob =
new Date(this.value);

const today =
new Date();

let age =
today.getFullYear()
-
dob.getFullYear();

const monthDiff =
today.getMonth()
-
dob.getMonth();

if(
monthDiff < 0 ||
(
monthDiff === 0 &&
today.getDate()
<
dob.getDate()
)
){
age--;
}

document.getElementById("age").value =
age;

if(age < 18){

alert(
"Age must be at least 18 years."
);

this.value = "";

document.getElementById("age").value = "";
}

});
}

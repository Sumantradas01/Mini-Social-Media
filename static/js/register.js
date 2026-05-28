const passwordInput = document.getElementById("password");
const strengthBar = document.getElementById("strength-bar");

passwordInput.addEventListener("input", () => {

  const password = passwordInput.value;

  let strength = 0;

  // RULES
  const hasLength = password.length >= 8;
  const hasUppercase = /[A-Z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

  // UPDATE UI
  updateRule("rule-length", hasLength);
  updateRule("rule-uppercase", hasUppercase);
  updateRule("rule-number", hasNumber);
  updateRule("rule-special", hasSpecial);

  if (hasLength) strength += 25;
  if (hasUppercase) strength += 25;
  if (hasNumber) strength += 25;
  if (hasSpecial) strength += 25;

  strengthBar.style.width = strength + "%";

  // COLORS
  if (strength <= 25) {
    strengthBar.style.background = "#ff4d4d";
  }
  else if (strength <= 50) {
    strengthBar.style.background = "#ff944d";
  }
  else if (strength <= 75) {
    strengthBar.style.background = "#ffd11a";
  }
  else {
    strengthBar.style.background = "#00cc66";
  }

});

function updateRule(id, valid) {

  const element = document.getElementById(id);

  if (valid) {
    element.innerHTML = "✅ " + element.innerHTML.substring(2);
    element.style.color = "#00cc66";
  }
  else {
    element.innerHTML = "❌ " + element.innerHTML.substring(2);
    element.style.color = "#ff4d4d";
  }

}

// SHOW / HIDE PASSWORD
function togglePassword(id) {

  const input = document.getElementById(id);

  if (input.type === "password") {
    input.type = "text";
  }
  else {
    input.type = "password";
  }

}
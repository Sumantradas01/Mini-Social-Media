const password = document.getElementById("password");
const strengthBar = document.getElementById("strength-bar");

password.addEventListener("input", () => {

  let val = password.value;
  let strength = 0;

  if(val.length >= 6) strength += 25;
  if(val.match(/[A-Z]/)) strength += 25;
  if(val.match(/[0-9]/)) strength += 25;
  if(val.match(/[^A-Za-z0-9]/)) strength += 25;

  strengthBar.style.width = strength + "%";
});

function togglePassword(id){

  const input = document.getElementById(id);

  if(input.type === "password"){
    input.type = "text";
  } else {
    input.type = "password";
  }
}
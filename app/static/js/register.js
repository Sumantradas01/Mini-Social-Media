/* ======================================
   NOVA AUTH SYSTEM
====================================== */

document.addEventListener("DOMContentLoaded", () => {

  // ======================================
  // ELEMENTS
  // ======================================

  const loginTab = document.getElementById("loginTab");
  const registerTab = document.getElementById("registerTab");

  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  // ======================================
  // PASSWORD TOGGLE
  // ======================================

  document.querySelectorAll(".toggle-pass").forEach(btn => {

    btn.addEventListener("click", () => {

      const target =
        document.getElementById(btn.dataset.target);

      target.type =
        target.type === "password"
          ? "text"
          : "password";

    });

  });

  // ======================================
  // LOGIN / REGISTER SWITCH
  // ======================================

  loginTab.addEventListener("click", () => {

    loginTab.classList.add("active");
    registerTab.classList.remove("active");

    loginForm.classList.add("active");
    registerForm.classList.remove("active");

  });

  registerTab.addEventListener("click", () => {

    registerTab.classList.add("active");
    loginTab.classList.remove("active");

    registerForm.classList.add("active");
    loginForm.classList.remove("active");

  });

  // ======================================
  // REGISTER USER
  // ======================================

  registerForm.addEventListener("submit", (e) => {

    e.preventDefault();

    const fullName =
      document.getElementById("full_name").value;

    const username =
      document.getElementById("username").value;

    const email =
      document.getElementById("email").value;

    const password =
      document.getElementById("password").value;

    const phone =
      document.getElementById("phone").value;

    // USER OBJECT
    const user = {

      id: Date.now(),

      fullName,
      username,
      email,
      password,
      phone

    };

    // GET USERS
    let users =
      JSON.parse(localStorage.getItem("novaUsers"))
      || [];

    // CHECK EXISTING EMAIL
    const existingUser = users.find(
      u => u.email === email
    );

    if (existingUser) {

      alert("Email already registered");
      return;

    }

    // SAVE USER
    users.push(user);

    localStorage.setItem(
      "novaUsers",
      JSON.stringify(users)
    );

    // AUTO LOGIN
    localStorage.setItem(
      "currentNovaUser",
      JSON.stringify(user)
    );

    // SUCCESS
    alert("Registration Successful");

    // REDIRECT
    window.location.href = "dashboard.html";

  });

  // ======================================
  // LOGIN USER
  // ======================================

  loginForm.addEventListener("submit", (e) => {

    e.preventDefault();

    const email =
      loginForm.querySelector(
        'input[type="email"]'
      ).value;

    const password =
      document.getElementById("loginPassword").value;

    // GET USERS
    const users =
      JSON.parse(localStorage.getItem("novaUsers"))
      || [];

    // FIND USER
    const user = users.find(
      u =>
        u.email === email &&
        u.password === password
    );

    // LOGIN SUCCESS
    if (user) {

      localStorage.setItem(
        "currentNovaUser",
        JSON.stringify(user)
      );

      alert("Login Successful");

      window.location.href =
        "dashboard.html";

    } else {

      alert("Invalid email or password");

    }

  });

});
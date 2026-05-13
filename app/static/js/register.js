/* ===========================
   Nova – register.js
   =========================== */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Elements ── */
  const form     = document.getElementById('registerForm');
  const submitBtn = document.getElementById('submitBtn');
  const strengthFill = document.getElementById('strengthFill');

  /* ── Password toggle ── */
  document.querySelectorAll('.toggle-pass').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = document.getElementById(btn.dataset.target);
      target.type = target.type === 'password' ? 'text' : 'password';
      btn.style.color = target.type === 'text' ? '#5b6af5' : '';
    });
  });

  /* ── Password strength ── */
  const pwInput = document.getElementById('password');
  pwInput.addEventListener('input', () => {
    const val = pwInput.value;
    let score = 0;
    if (val.length >= 8)              score++;
    if (/[A-Z]/.test(val))            score++;
    if (/[0-9]/.test(val))            score++;
    if (/[^A-Za-z0-9]/.test(val))    score++;

    const pct = (score / 4) * 100;
    strengthFill.style.width = pct + '%';
    const colors = ['', '#f87171', '#fbbf24', '#60a5fa', '#34d399'];
    strengthFill.style.background = colors[score] || '#f87171';
  });

  /* ── Real-time username lowercase ── */
  const usernameInput = document.getElementById('username');
  usernameInput.addEventListener('input', () => {
    usernameInput.value = usernameInput.value.toLowerCase().replace(/[^a-z0-9_.]/g, '');
  });

  /* ── Phone: digits only ── */
  const phoneInput = document.getElementById('phone');
  phoneInput.addEventListener('input', () => {
    phoneInput.value = phoneInput.value.replace(/\D/g, '').slice(0, 10);
  });

  /* ── Helpers ── */
  function showError(fieldId, msg) {
    const el = document.getElementById('err-' + fieldId);
    const inp = document.getElementById(fieldId);
    if (el) el.textContent = msg;
    if (inp) { inp.classList.add('error'); inp.classList.remove('valid'); }
  }

  function clearError(fieldId) {
    const el = document.getElementById('err-' + fieldId);
    const inp = document.getElementById(fieldId);
    if (el) el.textContent = '';
    if (inp) { inp.classList.remove('error'); inp.classList.add('valid'); }
  }

  function validateForm() {
    let valid = true;

    // Full name
    const fullName = document.getElementById('full_name').value.trim();
    if (!fullName || fullName.length < 2) {
      showError('full_name', 'Please enter your full name.'); valid = false;
    } else { clearError('full_name'); }

    // Username
    const username = usernameInput.value.trim();
    if (!username || username.length < 3) {
      showError('username', 'At least 3 characters.'); valid = false;
    } else if (!/^[a-z0-9_.]+$/.test(username)) {
      showError('username', 'Only letters, numbers, _ and . allowed.'); valid = false;
    } else { clearError('username'); }

    // Email
    const email = document.getElementById('email').value.trim();
    const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRe.test(email)) {
      showError('email', 'Enter a valid email address.'); valid = false;
    } else { clearError('email'); }

    // Phone (optional but if filled must be 10 digits)
    const phone = phoneInput.value.trim();
    if (phone && phone.length !== 10) {
      showError('phone', 'Enter a valid 10-digit number.'); valid = false;
    } else { clearError('phone'); }

    // Password
    const password = pwInput.value;
    if (password.length < 8) {
      showError('password', 'At least 8 characters required.'); valid = false;
    } else { clearError('password'); }

    // Confirm password
    const confirm = document.getElementById('confirm_password').value;
    if (confirm !== password) {
      showError('confirm_password', 'Passwords do not match.'); valid = false;
    } else { clearError('confirm_password'); }

    // Agreement
    const agree = document.getElementById('agree').checked;
    if (!agree) {
      document.getElementById('err-agree').textContent = 'You must accept the terms.';
      valid = false;
    } else {
      document.getElementById('err-agree').textContent = '';
    }

    return valid;
  }

  /* ── Live blur validation ── */
  ['full_name', 'username', 'email', 'phone', 'password', 'confirm_password'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('blur', validateForm);
  });

  /* ── Submit ── */
  form.addEventListener('submit', (e) => {
    if (!validateForm()) {
      e.preventDefault();
      // Shake the card
      const card = document.getElementById('formCard');
      card.style.animation = 'none';
      card.offsetHeight; // reflow
      card.style.animation = 'shake 0.4s ease';
      return;
    }
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
  });

});

/* Shake keyframe injected via JS for the error state */
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
@keyframes shake {
  0%,100% { transform: translateX(0); }
  20%      { transform: translateX(-8px); }
  40%      { transform: translateX(8px); }
  60%      { transform: translateX(-5px); }
  80%      { transform: translateX(5px); }
}
`;
document.head.appendChild(shakeStyle);
/* ===========================
   LOGIN / REGISTER SWITCH
=========================== */

const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

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
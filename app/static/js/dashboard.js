/* ======================================
   NOVA DASHBOARD
====================================== */

document.addEventListener("DOMContentLoaded", () => {

  // ======================================
  // GET CURRENT USER
  // ======================================

  const currentUser =
    JSON.parse(
      localStorage.getItem("currentNovaUser")
    );

  // NO LOGIN
  if (!currentUser) {

    window.location.href = "register.html";
    return;

  }

  // ======================================
  // PROFILE ELEMENTS
  // ======================================

  const profileName =
    document.getElementById("profileName");

  const profileUsername =
    document.getElementById("profileUsername");

  const userAvatar =
    document.getElementById("userAvatar");

  const composeName =
    document.getElementById("composeName");

  const composeAvatar =
    document.getElementById("composeAvatar");

  // ======================================
  // LOAD PROFILE
  // ======================================

  profileName.textContent =
    currentUser.fullName;

  profileUsername.textContent =
    "@" + currentUser.username;

  // INITIALS
  const initials =
    currentUser.fullName
      .split(" ")
      .map(word => word[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);

  userAvatar.textContent = initials;

  // COMPOSE
  if (composeName) {

    composeName.textContent =
      currentUser.fullName.split(" ")[0];

  }

  if (composeAvatar) {

    composeAvatar.textContent =
      initials;

  }

  // ======================================
  // NAV ACTIVE
  // ======================================

  document.querySelectorAll(".nav-item")
    .forEach(item => {

      item.addEventListener("click", () => {

        document.querySelectorAll(".nav-item")
          .forEach(i =>
            i.classList.remove("active")
          );

        item.classList.add("active");

      });

    });

  // ======================================
  // LIKE BUTTONS
  // ======================================

  window.toggleLike = function(btn) {

    btn.classList.toggle("liked");

    const countEl =
      btn.querySelector("span");

    let count =
      parseInt(countEl.textContent);

    const svg =
      btn.querySelector("svg");

    if (btn.classList.contains("liked")) {

      countEl.textContent = count + 1;

      svg.setAttribute(
        "fill",
        "currentColor"
      );

      svg.setAttribute(
        "stroke",
        "none"
      );

    } else {

      countEl.textContent = count - 1;

      svg.setAttribute(
        "fill",
        "none"
      );

      svg.setAttribute(
        "stroke",
        "currentColor"
      );

    }

  };

  // ======================================
  // FOLLOW BUTTONS
  // ======================================

  window.toggleFollow = function(btn) {

    btn.classList.toggle("following");

    btn.textContent =
      btn.classList.contains("following")
        ? "Following"
        : "Follow";

  };

  // ======================================
  // LOGOUT
  // ======================================

  const logoutBtn =
    document.getElementById("logoutBtn");

  if (logoutBtn) {

    logoutBtn.addEventListener("click", () => {

      localStorage.removeItem(
        "currentNovaUser"
      );

      window.location.href =
        "register.html";

    });

  }

});
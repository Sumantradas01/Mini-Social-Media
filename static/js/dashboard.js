document.addEventListener("DOMContentLoaded", () => {

    const menuItems =
    document.querySelectorAll(".sidebar nav a");

    menuItems.forEach(item => {

        item.addEventListener("click", () => {

            menuItems.forEach(i =>
                i.classList.remove("active")
            );

            item.classList.add("active");

        });

    });

});
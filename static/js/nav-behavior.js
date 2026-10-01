document.addEventListener("click", function (e) {
    const tabMenu = document.getElementById("tabMenu");
    const bsCollapse = bootstrap.Collapse.getInstance(tabMenu);

    // If hamburger menu is open AND click is outside it AND click opens user menu
    if (bsCollapse && tabMenu.classList.contains("show")) {

        // If the click is on the user dropdown toggle
        if (e.target.closest('.nav-item.dropdown')) {
            bsCollapse.hide();
        }
    }
});
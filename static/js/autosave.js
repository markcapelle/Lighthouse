let autosaveTimer = null;

function scheduleAutosave() {
    clearTimeout(autosaveTimer);
    autosaveTimer = setTimeout(runAutosave, 10000); // 10 seconds
}

function runAutosave() {
    const form = document.getElementById("edit-form");
    if (!form) return;

    const url = form.getAttribute("action") || window.location.href;

    const formData = new FormData(form);

    fetch(url, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        },
        body: formData
    })
    .then(response => {
        document.getElementById("autosave-status").style.display = "block";
        setTimeout(() => {
            document.getElementById("autosave-status").style.display = "none";
        }, 2000);
    });
}

document.addEventListener("input", scheduleAutosave);

document.addEventListener("DOMContentLoaded", function () {

    const tocContainer = document.getElementById("toc");

    // Headings to include
    const headings = document.querySelectorAll("h1, h2, h3");

    // Headings to ignore
    const ignoreList = [
        "help",
        "contents"
    ];

    const list = document.createElement("ul");
    list.className = "list-group";

    headings.forEach(h => {

        // Normalize heading text for comparison
        const text = h.textContent.trim().toLowerCase();

        // Skip ignored headings
        if (ignoreList.includes(text)) return;

        // Auto‑assign ID if missing
        if (!h.id) {
            h.id = text.replace(/\s+/g, "-");
        }

        const li = document.createElement("li");
        li.className = "list-group-item";

        // Indent based on heading level
        if (h.tagName === "H2") li.classList.add("ps-4");
        if (h.tagName === "H3") li.classList.add("ps-5");

        const a = document.createElement("a");
        a.href = "#" + h.id;
        a.textContent = h.textContent;

        li.appendChild(a);
        list.appendChild(li);
    });

    tocContainer.appendChild(list);
});
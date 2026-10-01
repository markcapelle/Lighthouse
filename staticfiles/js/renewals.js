// HIGHLIGHT ROWS WITH APPROACHING/OVERDUE RENEWAL DATES
document.addEventListener("DOMContentLoaded", function () {
    const now = new Date();
    const DAY = 24 * 60 * 60 * 1000;

    document.querySelectorAll("td.renewal-date").forEach(function (cell) {
        const raw = cell.dataset.date;
        if (!raw) return;

        let due;

        // If date-only (YYYY-MM-DD), parse manually as local midnight
        if (raw.length === 10) {
            const [y, m, d] = raw.split("-").map(Number);
            due = new Date(y, m - 1, d);
        } else {
            due = new Date(raw);
        }

        if (isNaN(due)) return;

        const diff = due - now;
        const row = cell.closest("tr");

        if (diff <= DAY) {
            row.classList.add("renewal-danger");
        } else if (diff <= 7 * DAY) {
            row.classList.add("renewal-warning");
        }
    });
});


// SORT BY COLUMN
document.addEventListener("DOMContentLoaded", function () {
    const tables = document.querySelectorAll("table[data-sortable]");

    tables.forEach(table => {
        const headers = table.querySelectorAll("th[data-sort]");

        headers.forEach((header, index) => {
            header.style.cursor = "pointer";

            header.addEventListener("click", () => {
                const type = header.getAttribute("data-sort");
                const tbody = table.querySelector("tbody");
                const rows = Array.from(tbody.querySelectorAll("tr"));

                const sorted = rows.sort((a, b) => {
                    const cellA = a.children[index].innerText.trim();
                    const cellB = b.children[index].innerText.trim();

                    switch (type) {
                        case "number":
                            return parseFloat(cellA) - parseFloat(cellB);

                        case "date":
                            return new Date(cellA) - new Date(cellB);

                        default: // string
                            return cellA.localeCompare(cellB);
                    }
                });

                // Toggle ascending/descending
                if (header.classList.contains("sorted-asc")) {
                    sorted.reverse();
                    header.classList.remove("sorted-asc");
                    header.classList.add("sorted-desc");
                } else {
                    header.classList.remove("sorted-desc");
                    header.classList.add("sorted-asc");
                }

                // Rebuild table
                tbody.innerHTML = "";
                sorted.forEach(row => tbody.appendChild(row));
            });
        });
    });
});

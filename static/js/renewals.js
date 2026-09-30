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

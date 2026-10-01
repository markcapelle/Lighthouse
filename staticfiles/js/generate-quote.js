document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("copy-quote");
    if (!btn) return;

    const dataEl = document.getElementById("quote-data");
    if (!dataEl) return;

    const renewal = JSON.parse(dataEl.textContent);

    btn.addEventListener("click", function () {

        const quote = `
${renewal.product} = €${renewal.price} ex VAT
Count: ${renewal.count}

Description:
${renewal.description}
        `.trim();

        navigator.clipboard.writeText(quote).then(() => {
            alert("Copied quote to clipboard");
        });
    });
});

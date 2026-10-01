// Renewal new/edit form behaviour:
//  1. Show product description / cost price / RRP once a product is selected
//  2. Show the renewal date field only when frequency = "custom"

document.addEventListener("DOMContentLoaded", function () {
    const productSelect = document.getElementById("id_product");
    const frequencySelect = document.getElementById("id_frequency");
    const dataEl = document.getElementById("product-data");

    if (!productSelect || !frequencySelect || !dataEl) return;

    const products = JSON.parse(dataEl.textContent);

    const detailsBox = document.getElementById("product-details");
    const descEl = document.getElementById("product-description");
    const costEl = document.getElementById("product-costprice");
    const rrpEl = document.getElementById("product-rrp");

    const dateGroup = document.getElementById("custom-renewal-date-group");

    function updateProductDetails() {
        const p = products[productSelect.value];
        if (!p) {
            detailsBox.style.display = "none";
            return;
        }

        descEl.textContent = p.description || "—";
        costEl.textContent = p.costprice;
        rrpEl.textContent = p.rrp;

        detailsBox.style.display = "block";
    }

    function updateRenewalDate() {
        dateGroup.style.display = frequencySelect.value === "custom" ? "block" : "none";
    }

    productSelect.addEventListener("change", updateProductDetails);
    frequencySelect.addEventListener("change", updateRenewalDate);

    // Initial state (edit form or re-rendered form with errors)
    updateProductDetails();
    updateRenewalDate();
});

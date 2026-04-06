function toggleEdit(id) {
    const row = document.getElementById(`row-${id}`);
    const viewElements = row.querySelectorAll('.view-mode-edit');
    const editElements = row.querySelectorAll('.edit-mode');

    viewElements.forEach(el => el.classList.toggle('d-none'));
    editElements.forEach(el => el.classList.toggle('d-none'));
}

async function saveEdit(id) {
    const row = document.getElementById(`row-${id}`);
    
    // Collect data from the input boxes in that specific row
    const data = {
        id: id,
        product: row.querySelector('input[name="product"]').value,
        cost_price: row.querySelector('input[name="cost_price"]').value,
        selling_price: row.querySelector('input[name="selling_price"]').value,
        units: row.querySelector('input[name="units"]').value,
        category: row.querySelector('input[name="category"]').value
    };

    // Send to Flask
    const response = await fetch('/edit_inplace', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        window.location.reload(); // Refresh to show new formatted data
    } else {
        alert("Failed to save changes.");
    }
}

function toggleSell(id) {
    const row = document.getElementById(`row-${id}`);
    const viewElements = row.querySelectorAll('.view-mode-sell');
    const editElements = row.querySelectorAll('.sell-mode');

    viewElements.forEach(el => el.classList.toggle('d-none'));
    editElements.forEach(el => el.classList.toggle('d-none'));
}

async function confirmSell(id) {
    const row = document.getElementById(`row-${id}`);
    
    const data = {
        item_id: id,
        sell_price: row.querySelector('input[name="selling_price"]').value,
        units_sold: row.querySelector('input[name="units"]').value
    };

    const response = await fetch('/sell_custom', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        window.location.reload();
    } else {
        const error = await response.json();
        alert(error.message || "Sale failed.");
    }
}
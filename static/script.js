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

function filterTable() {
    // Get the search input and the table rows
    const input = document.getElementById("tableSearch");
    const filter = input.value.toUpperCase();
    const table = document.querySelector(".table tbody");
    const tr = table.getElementsByTagName("tr");

    // Loop through all table rows and hide those that don't match the search query
    for (let i = 0; i < tr.length; i++) {
        // Look at the Product Name (column 2) and Category (column 6)
        const productName = tr[i].getElementsByTagName("td")[0];
        const category = tr[i].getElementsByTagName("td")[4];
        
        if (productName || category) {
            const txtValue = (productName.textContent || productName.innerText) + 
                             (category.textContent || category.innerText);
            
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function changeDate(days) {
    const datePicker = document.getElementById('datePicker');
    let currentDate = new Date(datePicker.value);
    
    // Add or subtract the days
    currentDate.setDate(currentDate.getDate() + days);
    
    // Format back to YYYY-MM-DD for the input
    const newDate = currentDate.toISOString().split('T')[0];
    
    // Redirect to the new filtered URL
    window.location.href = "/sales?date=" + newDate;
}
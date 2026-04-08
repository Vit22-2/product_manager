# PRODUCT MANAGER

## Features

- Dynamic Inventory Management: Add, edit, and delete products with a clean, responsive interface.
  
- In-Place Editing: Update product details (Price, Name, Units) directly within the table without page reloads using asynchronous JavaScript (fetch API).
  
- Sales Dashboard: Track total revenue and net profit at a glance with high-visibility summary cards.
  
- User Authentication: Secure login and registration to ensure each user manages their own private inventory.
  
- Persistent Storage: Powered by an SQLite database to ensure data is saved between sessions.

## Installation/Setup

### Clone repository

```
git clone https://github.com/Vit22-2/product_manager.git
cd product_manager
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run application
```
flask run
```

## Usage

- Register/Login: create an account to start your session.
  
- Add Items: use the input bar to add your initial stock.
  
- Edit In-Place: edit to change details instantly.
  
- Make a Sale: sell and adjust the price if you gave the customer a discount, and hit confirm.
  
- View Profits: navigate to the Sales tab to see your total earnings and a breakdown of every transaction.

# PRODUCT MANAGER

#### Video Demo:  https://youtu.be/FvyCWQnAhQE

#### Project Description

The Product Manager is a full-stack web application designed to help small business owners and garage sale organizers track their inventory and daily sales with minimal friction. Unlike traditional inventory systems that require navigating through multiple menus to update a single item. Most interactions, including inventory updates and sales recording, happen directly on the main dashboard using asynchronous updates.

## Technical Implementation
### The Backend (Flask & SQL)

The core of the application is built using the Flask framework. I utilized the cs50 SQL library to interact with an SQLite database (finance.db). The database is structured with three primary tables: users, inventory, and sales.

- Users Table: Handles authentication and password hashing using werkzeug.security.
- Inventory Table: Stores product details including cost, selling price, and stock levels. It uses a user_id foreign key to ensure data privacy.
- Sales Table: Records every transaction. A key technical challenge was handling Foreign Key constraints. If a user tries to delete an inventory item that is linked to a sale, the system catches the ValueError and prevents the deletion, ensuring the financial history remains accurate.
  
### The Frontend (JavaScript & Bootstrap)
- To provide a modern user experience, I implemented an in-place editing button. When a user clicks "Edit," the table row transforms into input fields. Upon saving, a JavaScript fetch() request sends the data to a Flask API route. This allows the UI to update without a full page refresh.
- I also added a Dynamic Search Filter in the table header. This script scans the "Product" and "Category" columns in real-time as the user types, hiding rows that don't match the query. This is particularly useful for users with large inventories.

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


import os
from datetime import datetime, date
from cs50 import SQL
from flask import Flask, flash, render_template, redirect, session, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import usd, login_required

#Configure application
app = Flask(__name__)

#Configure database to use CS50' SQLite
db = SQL("sqlite:///finance.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Custom filter
app.jinja_env.filters["usd"] = usd

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
    #Insert product information
    if request.method == "POST":
        product = request.form.get("product").strip().title()
        cost = request.form.get("cost_price")
        sell = request.form.get("selling_price")
        units = request.form.get("units")
        category = request.form.get("category") or "None"
        
        for val in [product, cost, sell, units]:
            if not val:
                flash("Please fill out all required fields.", "danger")
                return redirect("/")

        existing_item = db.execute(
            "SELECT id, units FROM inventory WHERE user_id = ? AND product_name = ? AND cost_price = ?", user_id, product, cost
        )
        if existing_item:
            # 2. Update existing row
            new_total = existing_item[0]["units"] + int(units)
            db.execute(
                "UPDATE inventory SET units = ? WHERE id = ?",
                new_total, existing_item[0]["id"]
            )
            flash(f"Added {product} to inventory!", "success")

        else:
            # 3. Insert as new row (your existing code)
            db.execute(
                "INSERT INTO inventory (user_id, product_name, cost_price, selling_price, units, category) VALUES (?, ?, ?, ?, ?, ?)",
                user_id, product, cost, sell, units, category
            )
            flash(f"Added {product} to inventory!", "success")
        return redirect("/")
    
    # Render inventory table
    inventory = []
    inv = db.execute(
        "SELECT * FROM inventory WHERE user_id = ?", user_id
    )
    for item in inv:
        inventory.append({
            "id": item["id"],
            "product": item["product_name"],
            "cost": usd(item["cost_price"]),
            "sell": usd(item["selling_price"]),
            "cost_raw": item["cost_price"],
            "sell_raw": item["selling_price"],
            "units": item["units"],
            "category": item["category"]
        })
    return render_template("layout.html", inventory=inventory)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 1. Ensure username and password were submitted
        if not username:
            flash("Must provide username")
            return render_template("login.html", "danger")

        if not password:
            flash("Must provide password", "danger")
            return render_template("login.html")

        # 2. Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # 3. Ensure username exists AND password is correct
        # This check prevents the IndexError because we return before accessing rows[0]
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password", "danger")
            return render_template("login.html")

        # 4. Success: Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash(f"Welcome back, {username}!", "success")
        return redirect("/")

    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # 1. Basic validation
        if not username:
            flash("Must provide username", "danger")
            return render_template("register.html")
            
        if not password or not confirmation:
            flash("Must provide password and confirmation", "danger")
            return render_template("register.html")

        if password != confirmation:
            flash("Passwords do not match", "danger")
            return render_template("register.html")

        # 2. Check if username exists (using the CS50 library style)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            flash("Username already exists", "danger")
            return render_template("register.html")

        # 3. Insert new user
        # Always hash the password before it touches the database!
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        flash("Registered successfully! Please log in.", "success")
        return render_template("login.html")
    else:
        return render_template("register.html")
    
@app.route("/logout")
def logout():
    #Forget user_id
    session.clear()

    #Redirect to log in page
    return redirect("/")

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    item_id = request.form.get("item_id")
    user_id = session["user_id"]
    try:
        # Attempt to delete the item
        db.execute("DELETE FROM inventory WHERE id = ? AND user_id = ?", item_id, user_id)
        flash("Item deleted successfully!", "success")
        
    except ValueError:
        # This block runs ONLY if the 'FOREIGN KEY constraint failed' error occurs
        flash("Cannot delete this item because it has associated sales records.", "danger")
    return redirect("/")
    
@app.route("/edit_inplace", methods=["POST"])
@login_required
def edit_inplace():
    data = request.get_json()
    
    db.execute(
        "UPDATE inventory SET product_name = ?, cost_price = ?, selling_price = ?, units = ?, category = ? WHERE id = ? AND user_id = ?",
        data['product'], data['cost_price'], data['selling_price'], data['units'], data['category'], data['id'], session["user_id"]
    )
    
    return {"success": True}, 200

@app.route("/sell_custom", methods=["POST"])
@login_required
def sell_custom():
    data = request.get_json()
    user_id = session["user_id"]
    dnt = datetime.now()
    
    # Fetch original item to get cost_price and check stock
    item = db.execute("SELECT * FROM inventory WHERE id = ? AND user_id = ?", data['item_id'], user_id)
    
    if not item or item[0]['units'] < int(data['units_sold']):
        return {"success": False, "message": "Not enough stock!"}, 400

    # 1. Update Inventory (Decrement units)
    db.execute(
        "UPDATE inventory SET units = units - ? WHERE id = ?",
        data['units_sold'], data['item_id']
    )

    # 2. Record the specific sale (using the custom price!)
    db.execute(
        "INSERT INTO sales (user_id, product_id, product_name, sell_price, cost_price, units_sold, datetime) VALUES (?, ?, ?, ?, ?, ?, ?)",
        user_id, data["item_id"], item[0]["product_name"], data['sell_price'], item[0]["cost_price"], data['units_sold'], dnt.strftime("%d-%b-%Y %I:%M%p")
    )

    return {"success": True}, 200

@app.route("/sales")
@login_required
def sales():
    user_id = session["user_id"]
    selected_date = request.args.get("date") or date.today().isoformat()
    date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    formatted_date_query = date_obj.strftime("%d-%b-%Y") + "%"
    rows = db.execute(
        "SELECT * FROM sales WHERE user_id = ? AND datetime LIKE ? ORDER BY datetime DESC", user_id, formatted_date_query
    )
    
    total_revenue = 0
    total_profit = 0
    
    sales_list = []
    for row in rows:
        profit = (row["sell_price"] - row["cost_price"]) * row["units_sold"]
        total_revenue += row["sell_price"] * row["units_sold"]
        total_profit += profit
        
        sales_list.append({
            "product": row["product_name"],
            "sell_price": usd(row["sell_price"]),
            "profit": usd(profit),
            "units": row["units_sold"],
            "date": row["datetime"]
        })
    return render_template("sales.html", sales=sales_list, revenue=usd(total_revenue), profit=usd(total_profit), current_date=selected_date)
import os
import datetime
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

@app.route("/")
@login_required
def index():
    return render_template("index.html")

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
            return render_template("login.html")

        if not password:
            flash("Must provide password")
            return render_template("login.html")

        # 2. Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # 3. Ensure username exists AND password is correct
        # This check prevents the IndexError because we return before accessing rows[0]
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # 4. Success: Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash(f"Welcome back, {username}!")
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
            flash("Must provide username")
            return render_template("register.html")
            
        if not password or not confirmation:
            flash("Must provide password and confirmation")
            return render_template("register.html")

        if password != confirmation:
            flash("Passwords do not match")
            return render_template("register.html")

        # 2. Check if username exists (using the CS50 library style)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            flash("Username already exists")
            return render_template("register.html")

        # 3. Insert new user
        # Always hash the password before it touches the database!
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        flash("Registered successfully! Please log in.")
        return render_template("login.html")
    else:
        return render_template("register.html")
    
@app.route("/logout")
def logout():
    #Forget user_id
    session.clear()

    #Redirect to log in page
    return redirect("/")
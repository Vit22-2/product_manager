import os
import datetime
from cs50 import SQL
from flask import Flask, render_template, redirect, session, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

db = SQL("sqlite:///finance.db")
@app.route("/")
def index():

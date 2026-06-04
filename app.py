import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #


@app.route("/")
def landing():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("register.html")

    name             = request.form.get("name", "").strip()
    email            = request.form.get("email", "").strip()
    password         = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not all([name, email, password, confirm_password]):
        flash("All fields are required.", "error")
        return render_template("register.html")

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return render_template("register.html")

    try:
        create_user(name, email, password)
    except sqlite3.IntegrityError:
        flash("Email already registered.", "error")
        return render_template("register.html")

    flash("Account created! Please sign in.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not all([email, password]):
        flash("All fields are required.", "error")
        return render_template("login.html")

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        flash("Invalid email or password.", "error")
        return render_template("login.html")

    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Aakash Jha",
        "email": "aakash@spendly.com",
        "member_since": "January 2026",
    }
    stats = {
        "total_spent": "₹271.50",
        "transaction_count": 8,
        "top_category": "Bills",
    }
    transactions = [
        {"date": "22 May 2026", "description": "Grocery run",      "category": "Food",          "amount": "₹22.00"},
        {"date": "18 May 2026", "description": "Miscellaneous",     "category": "Other",         "amount": "₹8.90"},
        {"date": "15 May 2026", "description": "New shirt",         "category": "Shopping",      "amount": "₹67.30"},
        {"date": "12 May 2026", "description": "Cinema ticket",     "category": "Entertainment", "amount": "₹18.00"},
        {"date": "08 May 2026", "description": "Pharmacy",          "category": "Health",        "amount": "₹45.00"},
    ]
    categories = [
        {"name": "Bills",         "total": "₹95.00", "pct": 35},
        {"name": "Shopping",      "total": "₹67.30", "pct": 25},
        {"name": "Health",        "total": "₹45.00", "pct": 17},
        {"name": "Food",          "total": "₹34.50", "pct": 13},
        {"name": "Entertainment", "total": "₹18.00", "pct":  7},
        {"name": "Other",         "total":  "₹8.90", "pct":  3},
        {"name": "Transport",     "total":  "₹2.80", "pct":  1},
    ]
    return render_template("profile.html",
        user=user, stats=stats,
        transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)

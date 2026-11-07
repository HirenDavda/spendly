from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from database.db import init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not password or len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters long")

        if get_user_by_email(email):
            return render_template("register.html", error="Email already registered")

        hashed_password = generate_password_hash(password)
        if create_user(name, email, hashed_password):
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error="An error occurred during registration. Please try again.")

    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)

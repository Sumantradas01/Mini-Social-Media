from flask import Flask, render_template, request, redirect, flash, session
from supabase import create_client
from dotenv import load_dotenv
import os
import re

# =====================================
# LOAD ENV
# =====================================

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret123"

# =====================================
# SUPABASE
# =====================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =====================================
# HOME PAGE
# =====================================

@app.route("/")
def home():
    return render_template("register.html")


# =====================================
# REGISTER USER
# =====================================

@app.route("/register", methods=["POST"])
def register():

    try:

        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # PASSWORD MATCH
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect("/")

        # PASSWORD VALIDATION
        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return redirect("/")

        if not re.search(r"[A-Z]", password):
            flash("Password must contain uppercase letter.", "danger")
            return redirect("/")

        if not re.search(r"[0-9]", password):
            flash("Password must contain number.", "danger")
            return redirect("/")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            flash("Password must contain special character.", "danger")
            return redirect("/")

        # CHECK EMAIL
        check_email = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )

        if check_email.data:
            flash("Email already registered.", "danger")
            return redirect("/")

        # CHECK USERNAME
        check_username = (
            supabase.table("users")
            .select("*")
            .eq("username", username)
            .execute()
        )

        if check_username.data:
            flash("Username already exists.", "danger")
            return redirect("/")

        # INSERT USER
        user_data = {
            "full_name": full_name,
            "username": username,
            "email": email,
            "phone": phone,
            "password": password
        }

        supabase.table("users").insert(user_data).execute()

        flash(
            "Registration Successful! Please Login.",
            "success"
        )

        return redirect("/")

    except Exception as e:

        print("REGISTER ERROR:", e)

        flash(str(e), "danger")

        return redirect("/")


# =====================================
# LOGIN USER
# =====================================

@app.route("/login", methods=["POST"])
def login():

    try:

        email = request.form.get("email")
        password = request.form.get("password")

        response = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .eq("password", password)
            .execute()
        )

        if not response.data:

            flash("Invalid Email or Password.", "danger")
            return redirect("/")

        user = response.data[0]

        # SAVE SESSION
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]

        # SAVE LOGIN HISTORY
        login_data = {
            "user_id": user["id"],
            "email": user["email"]
        }

        supabase.table("login_history") \
            .insert(login_data) \
            .execute()

        return redirect("/dashboard")

    except Exception as e:

        print("LOGIN ERROR:", e)

        flash(str(e), "danger")

        return redirect("/")


# =====================================
# DASHBOARD
# =====================================

@app.route("/dashboard")
def dashboard():

    # USER NOT LOGGED IN
    if "user_id" not in session:

        flash(
            "Please login first.",
            "danger"
        )

        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session["username"],
        email=session["email"]
    )


# =====================================
# LOGOUT
# =====================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect("/")


# =====================================
# RUN
# =====================================

if __name__ == "__main__":
    app.run(
        debug=True
    )
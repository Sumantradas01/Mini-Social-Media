from flask import Flask, render_template, request, redirect, flash, session
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, date
import pytz
import os
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret123"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


@app.route("/")
def home():
    return render_template("register.html")


# ==================================
# REGISTER
# ==================================

@app.route("/register", methods=["POST"])
def register():

    try:

        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        dob = request.form.get("DOB")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # PASSWORD MATCH

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect("/")

        # PHONE VALIDATION

        if not re.match(r"^[6-9]\d{9}$", phone):
            flash(
                "Phone number must be valid Indian 10 digit mobile number.",
                "danger"
            )
            return redirect("/")

        # AGE VALIDATION

        dob_date = datetime.strptime(
            dob,
            "%Y-%m-%d"
        ).date()

        today = date.today()

        age = (
            today.year -
            dob_date.year
        ) - (
            (
                today.month,
                today.day
            ) <
            (
                dob_date.month,
                dob_date.day
            )
        )

        if age < 18:
            flash(
                "Age must be 18 or above.",
                "danger"
            )
            return redirect("/")

        # PASSWORD VALIDATION

        if len(password) < 8:
            flash(
                "Minimum 8 characters required.",
                "danger"
            )
            return redirect("/")

        if not re.search(r"[A-Z]", password):
            flash(
                "One uppercase letter required.",
                "danger"
            )
            return redirect("/")

        if not re.search(r"[0-9]", password):
            flash(
                "One number required.",
                "danger"
            )
            return redirect("/")

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            password
        ):
            flash(
                "One special character required.",
                "danger"
            )
            return redirect("/")

        # EMAIL EXISTS

        email_check = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )

        if email_check.data:
            flash(
                "Email already exists.",
                "danger"
            )
            return redirect("/")

        # USERNAME EXISTS

        username_check = (
            supabase.table("users")
            .select("*")
            .eq("username", username)
            .execute()
        )

        if username_check.data:
            flash(
                "Username already exists.",
                "danger"
            )
            return redirect("/")

        # INDIA TIMEZONE

        india_time = datetime.now(
            pytz.timezone("Asia/Kolkata")
        )

        # USER DATA

        user_data = {
            "full_name": full_name,
            "username": username,
            "email": email,
            "phone": phone,
            "password": password,
            "DOB": dob,
            "time": india_time.isoformat()
        }

        response = (
            supabase.table("users")
            .insert(user_data)
            .execute()
        )

        print("REGISTER RESPONSE =", response)

        flash(
            "Registration Successful! Please Login.",
            "success"
        )

        return redirect("/")

    except Exception as e:

        print("REGISTER ERROR =", e)

        flash(
            str(e),
            "danger"
        )

        return redirect("/")

# ==================================
# LOGIN
# ==================================

@app.route("/login", methods=["POST"])
def login():

    try:

        email = request.form.get("email")
        password = request.form.get("password")

        # CHECK USER

        response = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .eq("password", password)
            .execute()
        )

        if not response.data:

            flash(
                "Invalid Email or Password",
                "danger"
            )

            return redirect("/")

        user = response.data[0]

        # SAVE SESSION

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]
        session["phone"] = user["phone"]
        session["dob"] = user["DOB"]

        # INDIA TIMEZONE

        india_time = datetime.now(
            pytz.timezone("Asia/Kolkata")
        )

        # SAVE LOGIN HISTORY

        history = (
            supabase.table("login_history")
            .insert({
                "user_id": int(user["id"]),
                "email": user["email"],
                "login_time": india_time.isoformat()
            })
            .execute()
        )

        print("LOGIN HISTORY =", history)

        # SAVE LOGIN HISTORY ID

        if history.data:

            session["login_history_id"] = (
                history.data[0]["id"]
            )

        flash(
            "Login Successful!",
            "success"
        )

        return redirect("/dashboard")

    except Exception as e:

        print("LOGIN ERROR =", e)

        flash(
            str(e),
            "danger"
        )

        return redirect("/")

# ==================================
# DASHBOARD
# ==================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session["username"],
        email=session["email"],
        phone=session["phone"],
        dob=session["dob"]
    )


# ==================================
# LOGOUT
# ==================================

@app.route("/logout")
def logout():

    try:

        if "login_history_id" in session:

            india_time = datetime.now(
                pytz.timezone("Asia/Kolkata")
            )

            supabase.table("login_history")\
                .update({
                    "logout_time": india_time.isoformat()
                })\
                .eq(
                    "id",
                    session["login_history_id"]
                )\
                .execute()

        session.clear()

        flash(
            "Logged out successfully.",
            "success"
        )

        return redirect("/")

    except Exception as e:

        print("LOGOUT ERROR =", e)

        flash(str(e), "danger")

        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
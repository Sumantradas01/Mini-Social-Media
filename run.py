from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session,
    jsonify
)

from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, date

import pytz
import os
import re

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

app = Flask(__name__)

app.secret_key = "secret123"

# =========================================
# SUPABASE
# =========================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template(
        "register.html"
    )

# =========================================
# REGISTER
# =========================================

@app.route("/register", methods=["POST"])
def register():

    try:

        full_name = request.form.get(
            "full_name"
        )

        username = request.form.get(
            "username"
        )

        email = request.form.get(
            "email"
        )

        phone = request.form.get(
            "phone"
        )

        dob = request.form.get(
            "DOB"
        )

        password = request.form.get(
            "password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )

        # PASSWORD MATCH

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect("/")

        # PHONE VALIDATION

        if not re.match(
            r"^[6-9]\d{9}$",
            phone
        ):

            flash(
                "Enter valid Indian mobile number.",
                "danger"
            )

            return redirect("/")

        # PASSWORD LENGTH

        if len(password) < 8:

            flash(
                "Password must be minimum 8 characters.",
                "danger"
            )

            return redirect("/")

        # UPPERCASE

        if not re.search(r"[A-Z]", password):

            flash(
                "Password needs one uppercase letter.",
                "danger"
            )

            return redirect("/")

        # NUMBER

        if not re.search(r"[0-9]", password):

            flash(
                "Password needs one number.",
                "danger"
            )

            return redirect("/")

        # SPECIAL CHARACTER

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            password
        ):

            flash(
                "Password needs one special character.",
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
                "Age must be 18+",
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

        # INDIA TIME

        india_time = datetime.now(
            pytz.timezone("Asia/Kolkata")
        )

        # SAVE USER

        user_data = {

            "full_name": full_name,

            "username": username,

            "email": email,

            "phone": phone,

            "password": password,

            "DOB": dob,

            "created_at":
                india_time.isoformat()

        }

        supabase.table(
            "users"
        ).insert(
            user_data
        ).execute()

        flash(
            "Registration Successful!",
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

# =========================================
# LOGIN
# =========================================

@app.route("/login", methods=["POST"])
def login():

    try:

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

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

        # SESSION

        session["user_id"] = user["id"]

        session["username"] = user["username"]

        session["email"] = user["email"]

        session["phone"] = user["phone"]

        session["dob"] = user["DOB"]

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

# =========================================
# DASHBOARD
# =========================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        flash(
            "Please login first.",
            "danger"
        )

        return redirect("/")

    return render_template(

        "dashboard.html",

        username=session.get(
            "username"
        ),

        email=session.get(
            "email"
        )

    )

# =========================================
# GET USERS
# =========================================

@app.route("/get_users")
def get_users():

    current_user = session.get(
        "user_id"
    )

    response = (
        supabase.table("users")
        .select("*")
        .neq("id", current_user)
        .execute()
    )

    return jsonify(
        response.data
    )

# =========================================
# GET MESSAGES
# =========================================

@app.route("/get_messages/<receiver_id>")
def get_messages(receiver_id):

    current_user = session.get(
        "user_id"
    )

    response = (
        supabase.table("messages")
        .select("*")
        .or_(

            f"""
            and(sender_id.eq.{current_user},
            receiver_id.eq.{receiver_id}),

            and(sender_id.eq.{receiver_id},
            receiver_id.eq.{current_user})
            """

        )
        .order(
            "created_at"
        )
        .execute()
    )

    messages = []

    for msg in response.data:

        sender = (
            supabase.table("users")
            .select("username")
            .eq(
                "id",
                msg["sender_id"]
            )
            .execute()
        )

        msg["sender_username"] = (
            sender.data[0]["username"]
        )

        messages.append(msg)

    return jsonify(messages)

# =========================================
# SEND MESSAGE
# =========================================

@app.route(
    "/send_message",
    methods=["POST"]
)

def send_message():

    data = request.get_json()

    current_user = session.get(
        "user_id"
    )

    india_time = datetime.now(
        pytz.timezone("Asia/Kolkata")
    )

    supabase.table(
        "messages"
    ).insert({

        "sender_id":
            current_user,

        "receiver_id":
            data["receiver_id"],

        "message":
            data["message"],

        "created_at":
            india_time.isoformat()

    }).execute()

    return jsonify({

        "success": True

    })

# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect("/")

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
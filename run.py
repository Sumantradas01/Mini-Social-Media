from flask import Flask, render_template, request, redirect, flash
from supabase import create_client
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "secret123"

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# REGISTER PAGE
@app.route("/")
def home():
    return render_template("register.html")

# REGISTER USER
@app.route("/register", methods=["POST"])
def register():

    try:

        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        data = {
            "full_name": full_name,
            "username": username,
            "email": email,
            "phone": phone,
            "password": password
        }

        response = supabase.table("users").insert(data).execute()

        flash("Account created successfully!", "success")

        print(response)

        return redirect("/")

    except Exception as e:

        print(e)
        flash(f"Error: {str(e)}", "danger")

        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
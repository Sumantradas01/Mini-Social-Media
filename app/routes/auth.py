from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.supabase_config import supabase

auth_bp = Blueprint("auth", __name__)

# =========================
# REGISTER PAGE
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        try:

            # CREATE USER IN SUPABASE AUTH
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            user = auth_response.user

            if user:

                # STORE EXTRA USER DATA
                supabase.table("profiles").insert({
                    "id": user.id,
                    "full_name": full_name,
                    "username": username,
                    "email": email,
                    "phone": phone
                }).execute()

                flash("Account created successfully!", "success")
                return redirect(url_for("auth.register"))

            else:
                flash("Registration failed.", "error")

        except Exception as e:
            flash(str(e), "error")

    return render_template("register.html")
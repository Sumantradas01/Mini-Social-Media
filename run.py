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
import base64
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


## SEARCH USER

@app.route("/search_user")
def search_user():

    query = request.args.get("query")

    if not query:
        return jsonify([])

    response = (
        supabase.table("users")
        .select("id,username,email")
        .ilike("username", f"%{query}%")
        .execute()
    )

    return jsonify(response.data)


## send_chat_request

@app.route("/send_chat_request", methods=["POST"])
def send_chat_request():

    current_user = session.get("user_id")

    data = request.get_json()

    receiver_id = data.get("receiver_id")

    # Check duplicate request

    existing = (
        supabase.table("chat_requests")
        .select("*")
        .eq("sender_id", current_user)
        .eq("receiver_id", receiver_id)
        .execute()
    )

    if existing.data:

        return jsonify({
            "success": False,
            "message": "Request already sent"
        })

    supabase.table("chat_requests").insert({

        "sender_id": current_user,
        "receiver_id": receiver_id,
        "status": "pending"

    }).execute()

    return jsonify({
        "success": True
    })


##chat_requests

@app.route("/chat_requests")
def chat_requests():

    current_user = session.get("user_id")

    requests = (
        supabase.table("chat_requests")
        .select("*")
        .eq("receiver_id", current_user)
        .eq("status", "pending")
        .execute()
    )

    result = []

    for req in requests.data:

        sender = (
            supabase.table("users")
            .select("username")
            .eq("id", req["sender_id"])
            .execute()
        )

        result.append({

            "request_id": req["id"],
            "sender_id": req["sender_id"],
            "sender_username":
            sender.data[0]["username"]

        })

    return jsonify(result)


## accept_request


@app.route("/accept_request", methods=["POST"])
def accept_request():

    data = request.get_json()

    request_id = data.get("request_id")

    supabase.table("chat_requests").update({

        "status": "accepted"

    }).eq(

        "id",
        request_id

    ).execute()

    return jsonify({
        "success": True
    })


## reject_request


@app.route("/reject_request", methods=["POST"])
def reject_request():

    data = request.get_json()

    request_id = data.get("request_id")

    supabase.table("chat_requests").update({

        "status": "rejected"

    }).eq(

        "id",
        request_id

    ).execute()

    return jsonify({
        "success": True
    })


## get_users

@app.route("/get_users")
def get_users():

    current_user = session.get("user_id")

    accepted = (
        supabase.table("chat_requests")
        .select("*")
        .eq("status", "accepted")
        .execute()
    )

    users = []

    for row in accepted.data:

        other_user = None

        if row["sender_id"] == current_user:

            other_user = row["receiver_id"]

        elif row["receiver_id"] == current_user:

            other_user = row["sender_id"]

        if other_user:

            user = (
                supabase.table("users")
                .select("*")
                .eq("id", other_user)
                .execute()
            )

            if user.data:
                users.append(user.data[0])

    return jsonify(users)

## send_message

@app.route("/send_message", methods=["POST"])
def send_message():

    data = request.get_json()

    current_user = session.get("user_id")

    receiver_id = data["receiver_id"]

    allowed = (
        supabase.table("chat_requests")
        .select("*")
        .eq("status", "accepted")
        .execute()
    )

    can_chat = False

    for req in allowed.data:

        if (

            req["sender_id"] == current_user
            and
            req["receiver_id"] == receiver_id

        ) or (

            req["sender_id"] == receiver_id
            and
            req["receiver_id"] == current_user

        ):

            can_chat = True
            break

    if not can_chat:

        return jsonify({

            "success": False,
            "message": "Chat request not accepted"

        })

    india_time = datetime.now(
        pytz.timezone("Asia/Kolkata")
    )

    supabase.table("messages").insert({

        "sender_id": current_user,
        "receiver_id": receiver_id,
        "message": data["message"],
        "created_at": india_time.isoformat()

    }).execute()

    return jsonify({
        "success": True
    })

## search_people


@app.route("/search_people")
def search_people():

    current_user = session.get("user_id")

    query = request.args.get("query")

    response = (
        supabase.table("users")
        .select("*")
        .neq("id", current_user)
        .ilike("username", f"%{query}%")
        .execute()
    )

    print("SEARCH QUERY =", query)
    print("RESULT =", response.data)

    return jsonify(response.data)


##  send_connection


@app.route("/send_connection", methods=["POST"])
def send_connection():

    current_user = session.get("user_id")

    data = request.get_json()

    receiver_id = data["receiver_id"]

    existing = (
        supabase.table("connections")
        .select("*")
        .or_(
            f"and(sender_id.eq.{current_user},receiver_id.eq.{receiver_id}),and(sender_id.eq.{receiver_id},receiver_id.eq.{current_user})"
        )
        .execute()
    )

    if existing.data:

        return jsonify({
            "success": False,
            "message": "Request already exists"
        })

    response = (
        supabase.table("connections")
        .insert({
            "sender_id": current_user,
            "receiver_id": receiver_id,
            "accepted": False,
            "status": "pending"
        })
        .execute()
    )

    print("CONNECTION INSERT =", response.data)

    return jsonify({
        "success": True
    })
## connection_requests


@app.route("/connection_requests")
@app.route("/connection_requests")
def connection_requests():

    current_user = session.get("user_id")

    requests = (
        supabase.table("connections")
        .select("*")
        .eq("receiver_id", current_user)
        .eq("status", "pending")
        .execute()
    )

    result = []

    for req in requests.data:

        sender = (
            supabase.table("users")
            .select("username")
            .eq("id", req["sender_id"])
            .execute()
        )

        result.append({

            "request_id": req["id"],
            "sender_id": req["sender_id"],
            "username": sender.data[0]["username"]

        })

    return jsonify(result)


##  accept_connection


@app.route("/accept_connection", methods=["POST"])
def accept_connection():

    data = request.get_json()

    request_id = data["request_id"]

    supabase.table("connections").update({

        "accepted": True,
        "status": "accepted"

    }).eq(
        "id",
        request_id
    ).execute()

    return jsonify({
        "success": True
    })


##  profile

@app.route("/profile/<int:user_id>")
def profile(user_id):

    if "user_id" not in session:
        return redirect("/")

    user = (
        supabase.table("users")
        .select("*")
        .eq("id", user_id)
        .execute()
    )

    if not user.data:
        return "User Not Found"

    user = user.data[0]

    return render_template(
        "profile.html",
        user=user
    )

@app.route("/create_post", methods=["POST"])
def create_post():

    if "user_id" not in session:

        return jsonify({
            "success": False
        })

    try:

        caption = request.form.get(
            "caption"
        )

        user_id = session["user_id"]

        india_time = datetime.now(
            pytz.timezone("Asia/Kolkata")
        )

        post = (
            supabase.table("posts")
            .insert({
                "user_id": user_id,
                "caption": caption,
                "created_at": india_time.isoformat()
            })
            .execute()
        )

        post_id = post.data[0]["id"]

        file = request.files.get("media")

        if file:

            media_bytes = file.read()

            media_data = media_bytes

            supabase.table(
                "post_media"
            ).insert({

                "post_id": post_id,

                "media_data": media_data,

                "media_name": file.filename,

                "media_type": file.content_type,

                "file_size": len(media_bytes)

            }).execute()

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("POST ERROR =", e)

        return jsonify({
            "success": False,
            "message": str(e)
        })


@app.route("/posts")
def get_posts():

    try:

        posts = (
            supabase.table("posts")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        result = []

        for post in posts.data:

            user = (
                supabase.table("users")
                .select("username")
                .eq(
                    "id",
                    post["user_id"]
                )
                .execute()
            )

            media = (
                supabase.table("post_media")
                .select("*")
                .eq(
                    "post_id",
                    post["id"]
                )
                .execute()
            )

            media_url = None
            media_type = None

            if media.data:

                media_url = (
                    "data:"
                    + media.data[0]["media_type"]
                    + ";base64,"
                    + base64.b64encode(
                        bytes.fromhex(
                            media.data[0]["media_data"]
                        )
                    ).decode()
                )

                media_type = (
                    media.data[0]["media_type"]
                )

            result.append({

                "id": post["id"],

                "username":
                user.data[0]["username"],

                "caption":
                post["caption"],

                "created_at":
                post["created_at"],

                "media_url":
                media_url,

                "media_type":
                media_type

            })

        return jsonify(result)

    except Exception as e:

        print("LOAD POSTS ERROR =", e)

        return jsonify([])
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
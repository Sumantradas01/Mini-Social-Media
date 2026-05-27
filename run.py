from flask import Flask
from supabase import create_client
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
..............
app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL =", SUPABASE_URL)
print("KEY =", SUPABASE_KEY)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



@app.route("/register", methods=["POST"])
def register():

    data = {
        "full_name": "Test User",
        "username": "testuser",
        "email": "test@example.com",
        "phone": "9876543210",
        "password": "12345678"
    }

    response = supabase.table("users").insert(data).execute()

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)

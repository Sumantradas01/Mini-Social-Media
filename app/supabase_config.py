import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("https://ysxbzhgnvoftcphkppbd.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_nFa3xexyQwVXtZ2v57AVpQ_LexlSCYh")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("Fatal Eror! Supabase URL is missing.")

if not SUPABASE_PUBLISHABLE_KEY:
    raise RuntimeError("Fatal Eror! Supabase publishable key is missing.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)

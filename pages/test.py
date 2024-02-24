from supabase import create_client, Client
import streamlit as st


SUPABASE_URL = "https://xgubbnhhcfosnylqhlfk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhndWJibmhoY2Zvc255bHFobGZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg3OTcyMzMsImV4cCI6MjAyNDM3MzIzM30.esJn6d1Frk9myp-11ZTjigfAPk5cuwF6l7m1o14Ly58"

url= SUPABASE_URL
key= SUPABASE_KEY
supabase: Client = create_client(url, key)


response = supabase.table('race_info').select("*").execute()
response
data = response.data
data
st.dataframe(data)
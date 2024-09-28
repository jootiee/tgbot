from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("TG_TOKEN")
API_URL = getenv("API_URL")
ADMIN_ID = getenv("ADMIN_ID")
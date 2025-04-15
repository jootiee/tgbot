from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
AWG_API = getenv("AWG_API")
DB_API = getenv("DB_API")
ADMIN_ID = getenv("ADMIN_ID")

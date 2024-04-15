import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

EX_DIR = os.getenv('EX_DIR')
EX_PATH = os.getenv('EX_PATH')
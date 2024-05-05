import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
ID_ADMIN = int(os.getenv('ID_ADMIN'))

DIR_EX = os.getenv('DIR_EX')
PATH_EX = os.getenv('PATH_EX')

PATH_DATABASE = os.getenv('PATH_DATABASE')
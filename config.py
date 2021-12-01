import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
admin_id = os.getenv("ADMIN_ID")

NAME_DB = os.getenv("NAME_DB")
USER_NAME_DB = os.getenv("USER_NAME_DB")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

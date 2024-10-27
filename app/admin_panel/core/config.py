import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_URL = os.getenv('DB_URL', default='mongodb://localhost:27017/test_db')
APP_AUTHOR = os.getenv('APP_AUTHOR')
APP_TITLE = os.getenv('APP_TITLE', default='MelnikovKnifeConcept')
APP_DOC_URL = os.getenv('APP_DOC_URL', default='/documentations')
SECRET = os.getenv('SECRET')
ADMIN = os.getenv('ADMIN')
PASSWORD = os.getenv('PASSWORD')
APP_ADMIN_PANEL_URL = os.getenv('APP_ADMIN_PANEL_URL', default='/admin')
HELP_TEXT_FOR_IMAGE = os.getenv('HELP_TEXT_FOR_IMAGE', default='Oops')
MAX_LEN_NICKNAME = os.getenv('MAX_LEN_NICKNAME', default=100)
MAX_LEN_KNIFENAME = os.getenv('MAX_LEN_KNIFENAME', default=100)
TIMEZONE = os.getenv('TIMEZONE', default='Europe/Moscow')
API_VERSION = os.getenv('API_VERSION')
PATTERN: str = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{8,}$'  # noqa

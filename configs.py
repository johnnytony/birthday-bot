import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get('BASE_URL')
CLIENT_ID = os.environ.get('CLIENT_ID')
API_KEY = os.environ.get('API_KEY')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
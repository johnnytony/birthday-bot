import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get('BASE_URL')
API_KEY = os.environ.get('API_KEY')

CLIENT_ID = os.environ.get('CLIENT_ID')

CHANNEL_ID = os.environ.get('CHANNEL_ID')
SERVER_ID = os.environ.get('SERVER_ID')
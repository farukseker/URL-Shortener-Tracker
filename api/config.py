from dotenv import load_dotenv
import os
import re

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
API_QUERY_HOST = os.getenv("API_QUERY_HOST")
API_QUERY_PATH = os.getenv("API_QUERY_PATH")


BOT_UA_REGEX = re.compile(
    r"bot|crawler|spider|crawling|slurp|bingpreview|facebookexternalhit|github",
    re.IGNORECASE,
)
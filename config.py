import os


# ================= TELEGRAM ================= #

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")


# ================= OWNER ================= #

OWNER_ID = int(os.getenv("OWNER_ID", 0))


# ================= LOG GROUP ================= #

LOG_GROUP = int(os.getenv("LOG_GROUP", 0))


# ================= DATABASE ================= #

MONGO_URL = os.getenv("MONGO_URL", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Mitsuri")

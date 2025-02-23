from .base import env


with env.prefixed("TELEGRAM_"):
    TELETHON = {
        "API_ID": env.int("API_ID"),
        "API_HASH": env.str("API_HASH"),
    }

from .base import env


TELETHON = {
    "API_ID": env.str("TELEGRAM_API_ID"),
    "API_HASH": env.str("TELEGRAM_API_HASH"),
    "DEFAULT_PHONE_NUMBER": env.str("TELEGRAM_DEFAULT_PHONE_NUMBER"),
}

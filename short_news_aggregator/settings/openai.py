import openai

from .base import env


openai.my_api_key = env.str("OPENAI_API_KEY")

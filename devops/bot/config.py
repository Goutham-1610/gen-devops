import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in environment")

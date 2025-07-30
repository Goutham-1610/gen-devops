import os
import discord
from discord.ext import commands

# Import configuration (use package-relative import if running as a package)
try:
    from config import DISCORD_TOKEN
except ImportError:
    from bot.config import DISCORD_TOKEN  # For 'python -m bot.main' execution

# Enable all required intents (including message content for command parsing)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Import command with correct package-relative path
try:
    from commands.dockerize import dockerize_cmd
except ImportError:
    from bot.commands.dockerize import dockerize_cmd  # For 'python -m bot.main'

bot.add_command(dockerize_cmd)

if __name__ == "__main__":
    # Print a helpful message if the token is missing
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN missing! Did you set up your .env file?")
    bot.run(DISCORD_TOKEN)

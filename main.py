import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def load_cogs():
    for ext in ["cogs.moderation", "cogs.tickets", "cogs.giveaways", "cogs.echo"]:
        await bot.load_extension(ext)

@bot.event
async def setup_hook():
    await load_cogs()

bot.run(TOKEN)
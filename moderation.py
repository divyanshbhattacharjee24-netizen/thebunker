import discord
from discord.ext import commands
import json
import os
from datetime import timedelta

WARN_FILE = "data/warns.json"

def load_warns():
    if not os.path.exists(WARN_FILE):
        return {}
    with open(WARN_FILE, "r") as f:
        return json.load(f)

def save_warns(data):
    os.makedirs("data", exist_ok=True)
    with open(WARN_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member} | Reason: {reason}")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member} | Reason: {reason}")

    @commands.command()
    async def mute(self, ctx, member: discord.Member, minutes: int):
        duration = discord.utils.utcnow() + timedelta(minutes=minutes)
        await member.edit(timed_out_until=duration)
        await ctx.send(f"Muted {member} for {minutes} minutes")

    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason="No reason"):
        warns = load_warns()
        uid = str(member.id)

        warns.setdefault(uid, []).append(reason)
        save_warns(warns)

        await ctx.send(f"{member} warned | Reason: {reason}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
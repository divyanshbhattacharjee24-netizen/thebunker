import discord
from discord.ext import commands
import asyncio
import random

active = {}

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def giveaway(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Use start or end")

    @giveaway.command()
    async def start(self, ctx, duration: int, *, prize: str):
        msg = await ctx.send(f"🎉 GIVEAWAY: {prize}\nReact 🎉")

        await msg.add_reaction("🎉")
        active[msg.id] = True

        await asyncio.sleep(duration)

        msg = await ctx.channel.fetch_message(msg.id)
        users = [u async for u in msg.reactions[0].users() if not u.bot]

        if users:
            winner = random.choice(users)
            await ctx.send(f"🏆 Winner: {winner.mention}")
        else:
            await ctx.send("No participants")

        active.pop(msg.id, None)

    @giveaway.command()
    async def end(self, ctx, message_id: int):
        active.pop(message_id, None)
        await ctx.send("Giveaway ended.")

async def setup(bot):
    await bot.add_cog(Giveaways(bot))
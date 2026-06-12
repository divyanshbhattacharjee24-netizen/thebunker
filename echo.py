from discord.ext import commands

class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="echo")
    async def echo(self, ctx, *, message: str):
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Echo(bot))
import discord
from discord.ext import commands

class TicketView(discord.ui.View):
    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.green)
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites=overwrites
        )

        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ticket_setup")
    async def ticket_setup(self, ctx):
        embed = discord.Embed(
            title="Support Tickets",
            description="Click below to create a ticket",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed, view=TicketView())

async def setup(bot):
    await bot.add_cog(Tickets(bot))
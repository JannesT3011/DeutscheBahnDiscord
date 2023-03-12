import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description="View all commands")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Deutsche Bahn Discord Bot - Help",
            color=self.bot.embed_color,
            description=f"**/route**\n**/traininfo**\n**/departures**"
        )

        return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
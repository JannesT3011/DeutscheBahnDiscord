import discord
from discord.ext import commands
from discord import app_commands
  


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot

    @app_commands.command(name='help', description="View all commands")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="ℹ️ DBot - Help ℹ️",
            description="""
            </help:1081581674724335709>
            ↪️ View all commands
            </route:1081581674724335706>
            ↪️ Plan your DB route ||(e.g Hamburg to München)||
            </departures:1081581674724335708>
            ↪️ View the departure of given Station ||(e.g Hamburg Hbf)||
            </traininfo:1081581674724335707>
            ↪️ See infos about a given train ||(e.g ICE72)||
            """,
            color=self.bot.embed_color,
            url="https://github.com/JannesT3011/DeutscheBahnDiscord"
        )
        embed.set_footer(text="DBot", icon_url=self.bot.user.display_avatar.url)

        
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    

async def setup(bot):
    await bot.add_cog(Help(bot))
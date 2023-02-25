import discord
from discord.ext import commands
from discord import app_commands
from utils import get_train_info, get_train_stopovers

class Traininfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="zuginfo", description="Siehe Infos über einen Zug")
    @app_commands.describe(zugnummer="Die Nummer des Zuges")
    async def zuginfo_command(self, interaction: discord.Interaction, zugnummer: str):
        await interaction.response.defer(thinking=True)

        data = await get_train_info(zugnummer)
        if data == 0:
            return await interaction.followup.send("No Train found!", ephemeral=True)
        
        stops = await get_train_stopovers(data["id"])
        
        embed = discord.Embed(
            title=f"{zugnummer} - Info",
            description=f"{data['origin']['name']} ➡️ {data['destination']['name']}"
        )

        embed.add_field( #Stops doesnt show up!
            name="Stops:",
            value=", \n".join(stop["stop"]["name"] for stop in stops)
        )

        return await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Traininfo(bot))
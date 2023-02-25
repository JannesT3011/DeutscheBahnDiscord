import discord
from discord.ext import commands
from discord import app_commands
from utils import get_trip_id, get_trip_info, format_dt

class Traininfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="zuginfo", description="Siehe Infos über einen Zug")
    @app_commands.describe(zugnummer="Die Nummer des Zuges")
    async def zuginfo_command(self, interaction: discord.Interaction, zugnummer: str):
        await interaction.response.defer(thinking=True)

        id = await get_trip_id(zugnummer)
        if id == (0):
            return await interaction.followup.send("No Train found!", ephemeral=True)
        
        info = await get_trip_info(id)
        
        embed = discord.Embed(
            title=f"{zugnummer.upper()} - Info",
            description=f"**{info[0]}** ➡️ **{info[1]}**",
            color=self.bot.embed_color
        )

        embed.add_field( # TODO planed times daneben (+verspätung)
            name="Stops:",
            value=", \n".join('**'+stop["stop"]["name"]+'**' f' ({format_dt(stop["departure"]).split(" ")[1] if stop["arrival"] is None else format_dt(stop["arrival"]).split(" ")[1]})' for stop in info[2])
        )

        return await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Traininfo(bot))
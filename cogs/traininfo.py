import discord
from discord.ext import commands
from discord import app_commands
from utils import get_trip_id, get_trip_info, format_dt, NoTrainFound

class Traininfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="traininfo", description="See infos about a given train")
    @app_commands.describe(zugnummer="Number of train e.g ICE72")
    async def zuginfo_command(self, interaction: discord.Interaction, zugnummer: str):
        """GET INFORMATION ABOUT THE GIVEN TRAIN: start, end, stops+departure"""
        await interaction.response.defer(thinking=True, ephemeral=True)

        id = await get_trip_id(zugnummer)
        
        if id == (0):
            raise NoTrainFound
        
        info = await get_trip_info(id)
        
        embed = discord.Embed(
            title=f"{info[3]} - Info",
            description=f"**{info[0]}** ➡️ **{info[1]}**",
            color=self.bot.embed_color
        )
        embed.set_footer(text="All data without guarantee")

        try:
            embed.add_field(
                name="Stops:",
                value=", \n".join('**'+stop["stop"]["name"]+'**' f' ({format_dt(stop["departure"]).split(" ")[1] if stop["arrival"] is None else format_dt(stop["arrival"]).split(" ")[1]})' for stop in info[2])
            )
        except:
            embed.add_field(
                name="Stops:",
                value=", \n".join('**'+stop["stop"]["name"]+'**'for stop in info[2])
            )
        finally:
            pass # Cant load stops!

        return await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Traininfo(bot))
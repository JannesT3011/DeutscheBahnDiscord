import discord
from discord.ext import commands
from discord import app_commands
from utils import get_station_info, get_departure_data, format_dt, calc_delay
from typing import Optional, Literal

class Departures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='departures', description="Departure of given Station")
    @app_commands.describe(station="The Station you want to get the departures", longdistance="Only show long distance Trains", duration="Period of time (minutes)")
    async def departures_command(self, interaction: discord.Interaction, station: str, longdistance: Optional[Literal["Yes", "No"]]):
        # TODO, duration: Optional[app_commands.Range[int, 24]]

        await interaction.response.defer(thinking=True)
        longdistance = True if longdistance == "Yes" else False

        station_id = await get_station_info(station)
        data = await get_departure_data(station_id[0], longdistance)
        
        embed = discord.Embed(
            title=f"{station_id[1]} Departures*"
        )
        for departure in data:
            delay = calc_delay(format_dt(departure["plannedWhen"]), format_dt(departure["when"]))
            delay_str = f"(+{delay})" if delay != 0 else ""
            embed.add_field(
                name=f"{departure['line']['name']} ➡️ {departure['direction']}",
                value=f"**Departure:** {format_dt(departure['when'])} {delay_str}\n**Platform:** {departure['plannedPlatform']}",
                inline=False
            )

        embed.set_footer(text="*for the next hour")

        return await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Departures(bot))
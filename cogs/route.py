import discord
from discord.ext import commands
from discord import app_commands
from utils import get_station_info, get_journey_info, format_dt
from typing import Optional

class Route(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_journey_info(self, start, end, data: dict, price) -> discord.Embed:
        embed = discord.Embed(title=f"{start} ➡️ {end}")
        for stop in data:
            try:
                load_factor = f"\n**Auslastung:** {stop['loadFactor']}"
            except KeyError:
                load_factor = ""
            try:
                dep_time = format_dt(stop["plannedDeparture"]) # arrivalDelay
                ar_time = format_dt(stop["plannedArrival"])

                embed.add_field(
                    name=f"{stop['line']['name']} - {stop['direction']}",
                    value=f"**From:** {stop['origin']['name']} Gl.{stop['departurePlatform']}\n**Departure:** {dep_time}\n**To:** {stop['destination']['name']} Gl.{stop['arrivalPlatform']}\n**Arrival:** {ar_time}{load_factor}\n⬇️",
                    inline=False
                ) 
            except:
                continue # Skips "laufzeit" (von tief zu normal)
        
        embed.add_field(name="Price:", value="Can't get price!" if price is None else f"{price['amount']}€", inline=False)
        return embed


    @app_commands.command(name='route', description="Plan your DB route!") # Later departure
    @app_commands.describe(start="The start train station", end="The end destination of your trip")
    async def route_command(self, interaction: discord.Interaction, start: str, end: str, date: Optional[str]):
        start_id = await get_station_info(start)
        end_id = await get_station_info(end)
        journey_info = await get_journey_info(start_id[0], end_id[0])

        if start_id == 0 or end_id == 0 or journey_info[0] == 0:
            return await interaction.response.send_message("Error", ephemeral=True)

        route = journey_info[0]
        price = journey_info[1]
        return await interaction.response.send_message(embed=self.format_journey_info(start_id[1], end_id[1], route, price))

async def setup(bot):
    await bot.add_cog(Route(bot))
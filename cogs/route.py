import discord
from discord.ext import commands
from discord import app_commands
from utils import get_station_id, get_journey_info
from typing import Optional

class Route(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def format_journey_info(self, start, end, data: dict, price) -> discord.Embed:
        embed = discord.Embed(title=f"{start} ➡️ {end}")
        for stop in data:
            embed.add_field(
                name=f"{stop['direction']} - {stop['line']['name']}",
                value=f"From: {stop['origin']['name']} Gl.{stop['departurePlatform']}\nTo: {stop['destination']['name']} Gl.{stop['arrivalPlatform']}\n⬇️",
                inline=False
            ) # TODO add times!
            # value: From - To, Departure Arrival, Platform, bei ice/ic auch auslastung
        
        embed.add_field(name="Price:", value="Can't get price!" if price is None else f"{price}€", inline=False)
        return embed


    @app_commands.command(name='route', description="Plan your DB route!")
    @app_commands.describe(start="The start train station", end="The end destination of your trip")
    async def route_command(self, interaction: discord.Interaction, start: Optional[str]="Darmstadt Hbf", end: Optional[str]="Hamburg Hbf"):
        start_id = await get_station_id(start)
        end_id = await get_station_id(end)
        # TODO error handler if one is 0
        journey_info = await get_journey_info(start_id, end_id)
        route = journey_info[0]
        price = journey_info[1]
        return await interaction.response.send_message(embed=self.format_journey_info(start, end, route, price))

async def setup(bot):
    await bot.add_cog(Route(bot))
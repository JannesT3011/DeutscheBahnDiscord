import discord
from discord.ext import commands
from discord import app_commands
from utils import get_station_info, get_journey_info, format_dt, str_to_time, calc_delay, format_dt_for_api
from typing import Optional


class Route(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_journey_info(self, start, end, data: dict, price) -> discord.Embed:
        """CREATED THE EMBED FOR THE ROUTE"""
        embed = discord.Embed(title=f"{start} ➡️ {end}", color=self.bot.embed_color)
        embed.set_footer(text="All data without guarantee")

        start_time = str_to_time(format_dt(data[0]["plannedDeparture"]))
        end_time = str_to_time(format_dt(data[len(data)-1]["plannedArrival"]))

        trip_duration = str(end_time-start_time).split(":")
        embed.description = f"**Duration:** {trip_duration[0]}:{trip_duration[1]}"

        for stop in data:
            try:
                load_factor = f"\n**👥:** {stop['loadFactor']}\n"
            except KeyError:
                load_factor = ""
            try:
                dep_time = format_dt(stop["plannedDeparture"]) # arrivalDelay
                dep_delay = calc_delay(dep_time, format_dt(stop["departure"]))
                dep_delay_str = f"(+{dep_delay})" if dep_delay != 0 else ""
                ar_time = format_dt(stop["plannedArrival"])
                ar_delay = calc_delay(ar_time, format_dt(stop["arrival"]))
                ar_delay_str = f"(+{ar_delay})" if ar_delay != 0 else ""

                embed.add_field(
                    name=f"{stop['line']['name']} - {stop['direction']}",
                    value=f"**From:** {stop['origin']['name']} Gl.{stop['departurePlatform']}\n**Departure:** {dep_time} {dep_delay_str}\n**To:** {stop['destination']['name']} Gl.{stop['arrivalPlatform']}\n**Arrival:** {ar_time} {ar_delay_str}{load_factor}\n⬇️",
                    inline=False
                ) 
            except:
                continue # Skips "laufzeit"
        
        embed.add_field(name="Price:", value="Can't get price!" if price is None else f"{price['amount']}€", inline=False)
        return embed


    @app_commands.command(name='route', description="Plan your DB route!") # Later departure
    @app_commands.describe(start="The start train station", end="The end destination of your trip")
    async def route_command(self, interaction: discord.Interaction, start: str, end: str, date: Optional[str]): # 
        """GET INFOS ABOUT A ROUTE (START>END)"""
        await interaction.response.defer(thinking=True, ephemeral=True)

        start_id = await get_station_info(start)
        end_id = await get_station_info(end)

        if start_id == (0) or end_id == (0):
            return await interaction.followup.send("No data found", ephemeral=True)

        if when is not None:
            when = format_dt_for_api(when)
        
        journey_info = await get_journey_info(start_id[0], end_id[0], format_dt_for_api(date))

        if journey_info[0] == (0):
            return await interaction.followup.send("No data found", ephemeral=True)

        route = journey_info[0]
        price = journey_info[1]

        return await interaction.followup.send(embed=self.format_journey_info(start_id[1], end_id[1], route, price))


async def setup(bot):
    await bot.add_cog(Route(bot))
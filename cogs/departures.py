import discord
from discord.ext import commands
from discord import app_commands
from utils import get_station_info, get_departure_data, format_dt, calc_delay, format_dt_for_api
from typing import Optional, Literal
from discord.ui import View, Button


class Departures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='departures', description="Departure of given Station")
    @app_commands.describe(station="The Station you want to see the departures", onlylongdistance="Only show long distance Trains", duration="Period of time (hours)", when="Date (dd-mm-yy HH:MM)")
    async def departures_command(self, 
                                 interaction: discord.Interaction, 
                                 station: str, 
                                 onlylongdistance: Optional[Literal["Yes", "No"]], 
                                 duration: Optional[app_commands.Range[int, 1, 24]]=1, 
                                 when: Optional[str]=None):
        """SEE THE STATION DEPARTURES: TRAIN, DESTINATION, DEPARTURE, PLATFORM"""
        await interaction.response.defer(thinking=True, ephemeral=True)

        onlylongdistance = True if onlylongdistance == "Yes" else False
        longdistance_str = " for Long Distance Trains" if onlylongdistance else ""

        station_id = await get_station_info(station)

        if station_id == 0:
            return await interaction.followup.send("No data found!", ephemeral=True)
        
        data = await get_departure_data(station_id[0], onlylongdistance, duration*60, format_dt_for_api(when))
        
        embed = discord.Embed(
            title=f"{station_id[1]} Departures{longdistance_str}:{'*' if duration==1 else ''}",
            color=self.bot.embed_color
        )
        for departure in data:
            try:
                delay = calc_delay(format_dt(departure["plannedWhen"]), format_dt(departure["when"]))
                delay_str = f"(+{delay})" if delay != 0 else ""
                embed.add_field(
                    name=f"{departure['line']['name']} ➡️ {departure['direction']}",
                    value=f"**Departure:** {format_dt(departure['plannedWhen'])} {delay_str}\n**Platform:** {departure['plannedPlatform']}",
                    inline=False
                )
            except:
                continue
        
        if duration == 1:
            embed.set_footer(text="*for the next hour\nAll data without guarantee")
        else:
            embed.set_footer(text="All data without guarantee")

        view = View()
        url = f"https://www.bahnhof.de/{station_id[1].replace(' ', '-')}"
        view.add_item(Button(label="See station infos", url=url))

        return await interaction.followup.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Departures(bot))
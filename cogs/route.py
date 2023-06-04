import discord
from discord.ext import commands
from discord import app_commands
from utils import get_station_info, get_journey_info, format_dt, str_to_time, calc_delay, format_dt_for_api, NoDataFound
from typing import Optional, Literal

bahncards = ["bahncard-1st-25", "bahncard-2nd-25", "bahncard-1st-50", "bahncard-2nd-50"]

class RouteView(discord.ui.View):

    def __init__(self, user: int, routes: list, index, guild:bool):
        super(RouteView, self).__init__(
            timeout=120
        )
        self.user = user
        self.interaction = None
        self.max = len(routes)
        self.routes = routes
        self.index = index
        self.pressed = False

        back_button = discord.ui.Button(emoji="⬅️")
        back_button.callback = self._back
        self.add_item(back_button)

        next_button = discord.ui.Button(emoji="➡️")
        next_button.callback = self._next
        self.add_item(next_button)

        if not guild:
            save_button = discord.ui.Button(emoji="📌")
            save_button.callback = self._save
            self.add_item(save_button)

        fav_button = discord.ui.Button(emoji="⭐")

    async def _back(self, interaction: discord.Interaction):
        self.index = self.index - 1 if self.index != 0 else self.max
        if self.index == 0: # Somehow useless but doesnt work with this (idk why)
            self.index = self.max
        self.interaction = interaction
        self.pressed = True
        self.stop()

    async def _next(self, interaction: discord.Interaction):
        self.index = self.index + 1 if self.index != self.max else 1
        self.interaction = interaction
        self.pressed = True
        self.stop()

    async def _save(self, interaction: discord.Interaction):
        channel = interaction.channel
        route = await channel.fetch_message(self.message.id)
        await route.pin()
        self.interaction = interaction
        self.pressed = True
        self.stop()

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        self.index = None
        self.stop()


class Route(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_journey_info(self, start, end, data: dict, price, index, max) -> discord.Embed:
        """CREATED THE EMBED FOR THE ROUTE"""
        embed = discord.Embed(title=f"{start} ➡️ {end}", color=self.bot.embed_color)
        embed.set_footer(text=f"All data without guarantee ({index}/{max})")

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
    @app_commands.describe(start="The start train station", end="The end destination of your trip", date="Departure of your route (dd-mm-yy HH:MM)", age="Age of traveler", bahncard="Bahncard")
    async def route_command(self, interaction: discord.Interaction, start: str, end: str, date: Optional[str]=None, age: Optional[app_commands.Range[int, 1, 99]]=None, bahncard: Optional[Literal["bahncard-1st-25", "bahncard-2nd-25", "bahncard-1st-50", "bahncard-2nd-50"]]=None):
        """GET INFOS ABOUT A ROUTE (START>END)"""
        await self.route_backend(interaction, start, end, date, bahncard=bahncard, age=age)

    async def route_backend(self, interaction: discord.Interaction, start: str, end: str, date: Optional[str]=None, edit:bool=False, index=1, bahncard=None, age=None):
        if not edit:
            ephemeral = True if interaction.guild else False
            await interaction.response.defer(thinking=True, ephemeral=ephemeral)

        start_id = await get_station_info(start)
        end_id = await get_station_info(end)

        if start_id == (0) or end_id == (0):
            raise NoDataFound

        if date is not None and not edit:
            date = format_dt_for_api(date)

        journeys = await get_journey_info(start_id[0], end_id[0], date, age, bahncard)

        if len(journeys) == 0 or journeys == [0]:
            raise NoDataFound

        view = RouteView(interaction.user.id, journeys, index, interaction.guild)

        route = journeys[index-1]["legs"]
        price = journeys[index-1]["price"]

        if edit:
            embed = self.format_journey_info(start_id[1], end_id[1], route, price, view.index, len(journeys))
            msg = await interaction.response.edit_message(embed=embed, view=view)
        else:
            embed = self.format_journey_info(start_id[1], end_id[1], route, price, index, len(journeys))
            msg = await interaction.followup.send(embed=embed, view=view)

        view.message = await interaction.original_response()

        await view.wait()

        interaction = view.interaction

        if view.pressed:
            return await self.route_backend(interaction, start, end, date, edit=True, index=view.index, age=age, bahncard=bahncard)


async def setup(bot):
    await bot.add_cog(Route(bot))
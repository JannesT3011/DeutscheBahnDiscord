import discord
from discord.ext import commands, tasks
from config import *
from discord import Color
import logging
from datetime import datetime

from utils import WrongDateFormat, NoDataFound, NoTrainFound
#logging.basicConfig(filename="logging.log", encoding='utf-8', level=logging.DEBUG)

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        intents = discord.Intents.all()
        intents.message_content = True
        super(Bot, self).__init__(
            command_prefix="db.",
            description=DESCRIPTION,
            intents=intents,
            activity=discord.Activity(name=ACTIVITY, type=discord.ActivityType.watching),
            help_command=None
        )
        self.embed_color = Color.from_str(EMBED_COLOR)

    # STARTUP FUNCTIONS
    async def startup(self) -> None:
        await self.wait_until_ready()
        await self.tree.sync()

    async def load_cogs(self) -> None:
        for ext in COGS:
            try:
                await self.load_extension(ext)
                print(f"{ext} loaded!")
                #logging.info(f"{ext} loaded!")
            except Exception as e:
                #logging.error(f"Cant load {ext}")
                raise e

    async def setup_hook(self) -> None:
        await self.load_cogs()
        self.tree.on_error = self.on_app_command_error
        self.loop.create_task(self.startup())

    # ERROR HANDLER:
    async def on_app_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, WrongDateFormat):
            return await interaction.followup.send(embed=ErrorEmbed("Wrong date format (dd.mm.yyyy hh:mm)"), ephemeral=True)
        elif isinstance(error, NoDataFound):
            embed = ErrorEmbed("Can't find any data! Please make sure the station exists")
            return await interaction.followup.send(embed=embed, ephemeral=True)
        elif isinstance(error, NoTrainFound):
            embed = ErrorEmbed("Can't find any data! Please make sure the train exists")
            return await interaction.followup.send(embed=embed, ephemeral=True)
        elif isinstance(error, discord.app_commands.CommandInvokeError):
            channel = await self.fetch_channel(1084802176464998450)
            await channel.send(f"Error:```{error}```")
            return await interaction.followup.send(embed=ErrorEmbed("Something went wrong!"), ephemeral=True)

    # EVENTS:
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

class ErrorEmbed(discord.Embed):
    def __init__(self, description):
        super().__init__(
            title="Error",
            description=description,
            color=discord.Color.red(),
            timestamp=datetime.utcnow(),
        )
        #self.set_footer(text=f"{bot.version} • made with ❤️ by {bot.creator}", icon_url=bot.user.display_avatar.url)

bot = Bot()

bot.run(TOKEN, reconnect=True)

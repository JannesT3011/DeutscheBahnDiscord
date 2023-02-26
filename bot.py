import discord
from discord.ext import commands, tasks
from config import *
from discord import Color
import logging

logging.basicConfig(filename="logging.log", encoding='utf-8', level=logging.DEBUG)

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        intents = discord.Intents.all()
        intents.message_content = True
        super(Bot, self).__init__(
            command_prefix="db.",
            description=DESCRIPTION,
            intents=intents,
            activity=discord.Game(name=ACTIVITY)
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
                logging.info(f"{ext} loaded!")
            except Exception as e:
                logging.error(f"Cant load {ext}")
                raise e
        
    async def setup_hook(self) -> None:
        await self.load_cogs()
        self.tree.on_error = self.on_app_command_error
        self.loop.create_task(self.startup())
    
    # ERROR HANDLER:
    async def on_app_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.CommandInvokeError):
            logging.warning(error)
            return await interaction.response.send_message("Something went wrong!", ephemeral=True)

    # EVENTS:
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return


bot = Bot()

bot.run(TOKEN, reconnect=True)

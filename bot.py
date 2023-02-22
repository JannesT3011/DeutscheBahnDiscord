import discord
from discord.ext import commands, tasks
from config import *
from datetime import datetime, timedelta


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
    
    # STARTUP FUNCTIONS
    async def startup(self) -> None:
        await self.wait_until_ready()
        await self.tree.sync()
       
    async def load_cogs(self) -> None:
        for ext in COGS:
            try:
                await self.load_extension(ext)
                print(f"{ext} loaded!")
            except Exception as e:
                print(f"Cant load {ext}")
                raise e
        
    async def setup_hook(self) -> None:
        await self.load_cogs()
        # self.tree.on_error = self.on_app_command_error
        self.loop.create_task(self.startup())

    
    # EVENTS:
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return


bot = Bot()

bot.run(TOKEN, reconnect=True)

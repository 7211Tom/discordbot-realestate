import discord
from discord.ext import commands

from config import TOKEN
from data.listings import ListingStore


class RealEstateBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.store = ListingStore()

    async def setup_hook(self):
        await self.load_extension("cogs.listings")
        await self.load_extension("cogs.admin")


bot = RealEstateBot()


@bot.event
async def on_ready():
    print(f"Bot is online als {bot.user}")


bot.run(TOKEN)

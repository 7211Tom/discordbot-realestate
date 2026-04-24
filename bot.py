import logging
import os
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands

from config import ALLOWED_CHANNEL_NAME, DB_FILE, GUILD_ID, TOKEN
from data.listings import ListingStore


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "bot.log")
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            LOG_FILE,
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        ),
    ],
)
logger = logging.getLogger(__name__)


class RealEstateBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.store = ListingStore()
        logger.info("Bot initialized with database %s", DB_FILE)

    async def setup_hook(self):
        logger.info("Loading extensions")
        await self.load_extension("cogs.listings")
        await self.load_extension("cogs.admin")

        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced_commands = await self.tree.sync(guild=guild)
            logger.info(
                "Synced %s application commands for guild %s",
                len(synced_commands),
                GUILD_ID,
            )
        else:
            synced_commands = await self.tree.sync()
            logger.info("Synced %s global application commands", len(synced_commands))

        logger.info("Extensions loaded successfully")

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Er ontbreekt invoer voor dit commando. Gebruik !helpme voor hulp.")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("Ongeldige invoer voor dit commando. Gebruik !helpme voor het juiste formaat.")
            return

        original = getattr(error, "original", error)
        logger.exception("Unhandled command error in %s", ctx.command, exc_info=original)
        await ctx.send("Er ging iets mis bij het uitvoeren van dit commando. Probeer het opnieuw.")


bot = RealEstateBot()


@bot.event
async def on_ready():
    logger.info("Bot is online als %s", bot.user)
    logger.info("Allowed channel is %s", ALLOWED_CHANNEL_NAME)


bot.run(TOKEN, log_handler=None)

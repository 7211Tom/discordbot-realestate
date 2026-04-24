import discord
from discord import app_commands
from discord.ext import commands

from utils.guards import is_allowed_channel
from utils.messages import send_list


class ListingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list")
    async def list_command(self, ctx):
        if not is_allowed_channel(ctx):
            return

        await send_list(ctx)

    @commands.command()
    async def search(self, ctx, *, keyword):
        if not is_allowed_channel(ctx):
            return

        results = self.bot.store.search(keyword)

        if not results:
            await ctx.send(f"Geen resultaten gevonden voor '{keyword}'.")
            return

        await send_list(ctx, results)

    @commands.command()
    async def helpme(self, ctx):
        if not is_allowed_channel(ctx):
            return

        help_text = (
            "!list\n"
            "!sold <zoekwoord>\n"
            "!forsale <zoekwoord>\n"
            "!remove <id>\n"
            "!search <zoekwoord>\n"
            "!add adres | stad | land | prijs | optionele notitie"
        )
        await ctx.send(f"```{help_text}```")

    @app_commands.command(
        name="commands",
        description="Toont een overzicht van alle beschikbare bot-commands.",
    )
    async def commands_overview(self, interaction: discord.Interaction):
        help_text = (
            "!list\n"
            "!sold <zoekwoord>\n"
            "!forsale <zoekwoord>\n"
            "!remove <id>\n"
            "!search <zoekwoord>\n"
            "!add adres | stad | land | prijs | optionele notitie"
        )
        await interaction.response.send_message(
            f"```{help_text}```",
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(ListingsCog(bot))

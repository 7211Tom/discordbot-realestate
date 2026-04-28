import discord
from discord import app_commands
from discord.ext import commands

from utils.guards import ensure_interaction_channel, ensure_interaction_editor
from utils.messages import (
    COMMANDS_OVERVIEW_TEXT,
    build_notice_embed,
    send_public_list,
    send_private_list,
)


class ListingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="list",
        description="Show the current listing board.",
    )
    async def slash_list(self, interaction: discord.Interaction):
        await send_private_list(interaction)

    @app_commands.command(
        name="search",
        description="Search listings by address, city, country, status, or note.",
    )
    async def slash_search(self, interaction: discord.Interaction, keyword: str):
        results = self.bot.store.search(keyword)

        if not results:
            await interaction.response.send_message(
                embed=build_notice_embed(
                    "No Results",
                    f"No listings found for '{keyword}'.",
                ),
                ephemeral=True,
            )
            return

        await send_private_list(interaction, results, title="Search Results")

    @app_commands.command(
        name="help",
        description="Show the public user commands.",
    )
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=build_notice_embed(
                "Help",
                "/list - Show the listings privately\n"
                "/search - Search listings privately",
            ),
            ephemeral=True,
        )

    @app_commands.command(
        name="public_list",
        description="Post the current listing board publicly.",
    )
    @app_commands.default_permissions(administrator=True)
    async def public_list(self, interaction: discord.Interaction):
        if not await ensure_interaction_editor(interaction):
            return

        await send_public_list(interaction)

    @app_commands.command(
        name="commands",
        description="Show all available bot commands.",
    )
    @app_commands.default_permissions(administrator=True)
    async def commands_overview(self, interaction: discord.Interaction):
        if not await ensure_interaction_channel(interaction):
            return

        if not await ensure_interaction_editor(interaction):
            return

        await interaction.response.send_message(
            embed=build_notice_embed(
                "Commands",
                f"```{COMMANDS_OVERVIEW_TEXT}```",
            ),
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(ListingsCog(bot))

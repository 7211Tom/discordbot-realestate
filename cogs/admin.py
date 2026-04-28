import discord
from discord import app_commands
from discord.ext import commands

import logging

from utils.guards import (
    ensure_interaction_channel,
    ensure_interaction_editor,
)
from utils.messages import build_notice_embed, send_private_list


logger = logging.getLogger(__name__)


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="add",
        description="Add a listing to the board.",
    )
    @app_commands.default_permissions(administrator=True)
    async def slash_add(
        self,
        interaction: discord.Interaction,
        address: str,
        city: str,
        country: str,
        price: str,
        note: str = "",
    ):
        if not await ensure_interaction_channel(interaction):
            return

        if not await ensure_interaction_editor(interaction):
            return

        logger.info(
            "Admin command /add invoked by %s (%s)",
            interaction.user,
            interaction.user.id,
        )

        try:
            listing = self.bot.store.add_listing([address, city, country, price, note])
        except ValueError:
            await interaction.response.send_message(
                embed=build_notice_embed(
                    "Invalid Price",
                    "Use numbers only, for example 250000 or 250000.50.",
                ),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=build_notice_embed(
                "Listing Added",
                f"#{listing['id']} {listing['address']}",
            ),
            ephemeral=True,
        )
        await send_private_list(interaction)

    @app_commands.command(
        name="sold",
        description="Mark a listing as sold.",
    )
    @app_commands.default_permissions(administrator=True)
    async def slash_sold(self, interaction: discord.Interaction, keyword: str):
        if not await ensure_interaction_channel(interaction):
            return

        if not await ensure_interaction_editor(interaction):
            return

        logger.info(
            "Admin command /sold invoked by %s (%s)",
            interaction.user,
            interaction.user.id,
        )

        item = self.bot.store.mark_sold(keyword)

        if not item:
            await interaction.response.send_message(
                embed=build_notice_embed(
                    "No Match",
                    f"No for-sale listing found for '{keyword}'.",
                ),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=build_notice_embed("Marked Sold", item["address"]),
            ephemeral=True,
        )
        await send_private_list(interaction)

    @app_commands.command(
        name="forsale",
        description="Mark a sold listing as for sale.",
    )
    @app_commands.default_permissions(administrator=True)
    async def slash_forsale(self, interaction: discord.Interaction, keyword: str):
        if not await ensure_interaction_channel(interaction):
            return

        if not await ensure_interaction_editor(interaction):
            return

        logger.info(
            "Admin command /forsale invoked by %s (%s)",
            interaction.user,
            interaction.user.id,
        )

        item = self.bot.store.mark_for_sale(keyword)

        if not item:
            await interaction.response.send_message(
                embed=build_notice_embed(
                    "No Sold Match",
                    f"No sold listing found for '{keyword}'.",
                ),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=build_notice_embed("Marked For Sale", item["address"]),
            ephemeral=True,
        )
        await send_private_list(interaction)

    @app_commands.command(
        name="remove",
        description="Remove a listing from the board.",
    )
    @app_commands.default_permissions(administrator=True)
    async def slash_remove(self, interaction: discord.Interaction, listing_id: int):
        if not await ensure_interaction_channel(interaction):
            return

        if not await ensure_interaction_editor(interaction):
            return

        logger.info(
            "Admin command /remove invoked by %s (%s)",
            interaction.user,
            interaction.user.id,
        )

        item = self.bot.store.remove_listing(str(listing_id))

        if not item:
            await interaction.response.send_message(
                embed=build_notice_embed(
                    "Invalid ID",
                    "No valid listing ID found. Use /list or /search first.",
                ),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=build_notice_embed(
                "Listing Removed",
                f"#{item['id']} {item['address']}",
            ),
            ephemeral=True,
        )
        await send_private_list(interaction)


async def setup(bot):
    await bot.add_cog(AdminCog(bot))

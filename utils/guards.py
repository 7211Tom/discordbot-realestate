from config import ALLOWED_CHANNEL_NAME, OWNER_DISCORD_ID
from utils.messages import build_notice_embed


def is_allowed_interaction_channel(interaction):
    return getattr(interaction.channel, "name", None) == ALLOWED_CHANNEL_NAME


def interaction_user_can_edit(interaction):
    if not OWNER_DISCORD_ID:
        return False

    return str(interaction.user.id) == OWNER_DISCORD_ID.strip()


async def ensure_interaction_channel(interaction):
    if is_allowed_interaction_channel(interaction):
        return True

    await interaction.response.send_message(
        embed=build_notice_embed(
            "Wrong Channel",
            f"Please use this command in #{ALLOWED_CHANNEL_NAME}.",
        ),
        ephemeral=True,
    )
    return False


async def ensure_interaction_editor(interaction):
    if interaction_user_can_edit(interaction):
        return True

    if not OWNER_DISCORD_ID:
        await interaction.response.send_message(
            embed=build_notice_embed(
                "Editing Disabled",
                "Set OWNER_DISCORD_ID in your .env file to edit the listing board.",
            ),
            ephemeral=True,
        )
        return False

    await interaction.response.send_message(
        embed=build_notice_embed(
            "Access Denied",
            "Only the bot owner can edit the listing board.",
        ),
        ephemeral=True,
    )
    return False

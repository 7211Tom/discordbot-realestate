from config import ALLOWED_CHANNEL_NAME, OWNER_DISCORD_ID


def is_allowed_channel(ctx):
    return getattr(ctx.channel, "name", None) == ALLOWED_CHANNEL_NAME


async def ensure_allowed_channel(ctx):
    return is_allowed_channel(ctx)


def user_can_edit(ctx):
    if not OWNER_DISCORD_ID:
        return False

    return str(ctx.author.id) == OWNER_DISCORD_ID.strip()


async def ensure_editor(ctx):
    if user_can_edit(ctx):
        return True

    if not OWNER_DISCORD_ID:
        await ctx.send(
            "Schrijven staat uit. Zet OWNER_DISCORD_ID in je .env om !add, !sold, !forsale en !remove te gebruiken."
        )
        return False

    await ctx.send("Alleen de eigenaar van deze bot mag de lijst aanpassen.")
    return False

import discord

from config import FOR_SALE_INDICATOR, SOLD_INDICATOR


MAX_EMBED_DESCRIPTION_LENGTH = 3900
MAX_MESSAGE_LENGTH = 1900
MAX_LINE_LENGTH = 400
EMBED_COLOR = discord.Color.gold()
COMMANDS_OVERVIEW_TEXT = (
    "/list\n"
    "/search keyword:<keyword>\n"
    "/public_list\n"
    "/add address:<address> city:<city> country:<country> price:<price> note:<note>\n"
    "/sold keyword:<keyword>\n"
    "/forsale keyword:<keyword>\n"
    "/remove listing_id:<id>"
)


def truncate_text(text, limit):
    if len(text) <= limit:
        return text

    return f"{text[: limit - 3].rstrip()}..."


def get_recent_sold_id(items):
    sold_items = [item for item in items if item["status"] == "SOLD"]
    if not sold_items:
        return None

    recent_item = max(
        sold_items,
        key=lambda item: (item.get("updated_at") or "", item["id"]),
    )
    return recent_item["id"]


def build_listing_line(item, recent_sold_id=None):
    status_icon = SOLD_INDICATOR if item["status"] == "SOLD" else FOR_SALE_INDICATOR
    location = ", ".join(
        part for part in [item["city"].strip(), item["country"].strip()] if part
    )

    meta = []
    if item["status"] == "SOLD":
        meta.append("SOLD")
    else:
        price = item["price"] if item["price"] else "?"
        meta.append(f"FOR SALE - **$ {price}**")

    if item["note"]:
        meta.append(item["note"])

    recent_badge = (
        "`RECENT` "
        if item["status"] == "SOLD" and item["id"] == recent_sold_id
        else ""
    )
    line = f"`#{item['id']}` {recent_badge}{status_icon} {item['address']} - **{location}** - {' | '.join(meta)}"
    return truncate_text(line, MAX_LINE_LENGTH)


def build_notice_embed(title, description, color=EMBED_COLOR):
    return discord.Embed(title=title, description=description, color=color)


def build_list_messages(items, title="UPDATE"):
    if not items:
        return ["The listing board is empty."]

    recent_sold_id = get_recent_sold_id(items)
    chunks = []
    current_chunk = title

    for item in items:
        line = build_listing_line(item, recent_sold_id=recent_sold_id)
        candidate = f"{current_chunk}\n{line}"

        if len(candidate) <= MAX_MESSAGE_LENGTH:
            current_chunk = candidate
            continue

        if current_chunk != title:
            chunks.append(current_chunk)
        current_chunk = f"{title}\n{line}"

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def build_list_embeds(items, title="Listings"):
    if not items:
        return [build_notice_embed("Listings", "The listing board is empty.")]

    recent_sold_id = get_recent_sold_id(items)
    embeds = []
    current_lines = []
    current_length = 0

    for item in items:
        line = build_listing_line(item, recent_sold_id=recent_sold_id)
        line_length = len(line) + 1

        if current_lines and current_length + line_length > MAX_EMBED_DESCRIPTION_LENGTH:
            embeds.append(
                discord.Embed(
                    title=title,
                    description="\n".join(current_lines),
                    color=EMBED_COLOR,
                )
            )
            current_lines = []
            current_length = 0

        current_lines.append(line)
        current_length += line_length

    if current_lines:
        embeds.append(
            discord.Embed(
                title=title,
                description="\n".join(current_lines),
                color=EMBED_COLOR,
            )
        )

    return embeds


async def send_interaction_list(
    interaction,
    items_to_show=None,
    title="Listings",
    ephemeral=True,
):
    items = (
        items_to_show
        if items_to_show is not None
        else interaction.client.store.listings
    )
    embeds = build_list_embeds(items, title=title)
    if interaction.response.is_done():
        await interaction.followup.send(embed=embeds[0], ephemeral=ephemeral)
    else:
        await interaction.response.send_message(embed=embeds[0], ephemeral=ephemeral)

    for embed in embeds[1:]:
        await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def send_public_list(interaction, items_to_show=None, title="UPDATE"):
    items = (
        items_to_show
        if items_to_show is not None
        else interaction.client.store.listings
    )
    chunks = build_list_messages(items, title=title)

    if interaction.response.is_done():
        await interaction.followup.send(chunks[0])
    else:
        await interaction.response.send_message(chunks[0])

    for chunk in chunks[1:]:
        await interaction.followup.send(chunk)


async def send_private_list(interaction, items_to_show=None, title="Listings"):
    await send_interaction_list(
        interaction,
        items_to_show=items_to_show,
        title=title,
        ephemeral=True,
    )

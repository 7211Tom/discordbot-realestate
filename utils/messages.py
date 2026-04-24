MAX_MESSAGE_LENGTH = 1900


def build_listing_line(item):
    emoji = "❌" if item["status"] == "SOLD" else "✅"
    location = ", ".join(
        part for part in [item["city"].strip(), item["country"].strip()] if part
    )

    meta = []
    if item["status"] == "SOLD":
        meta.append("SOLD")
    else:
        price = item["price"] if item["price"] else "?"
        meta.append(f"FOR SALE · $ {price}")

    if item["recent"]:
        meta.append("`RECENT`")
    if item["note"]:
        meta.append(item["note"])

    return f"`#{item['id']}` {emoji} {item['address']} · {location} - {' | '.join(meta)}"


async def send_list(ctx, items_to_show=None):
    items = items_to_show if items_to_show is not None else ctx.bot.store.listings

    if not items:
        await ctx.send("Lijst is leeg.")
        return

    chunks = []
    current_chunk = "UPDATE"

    for item in items:
        line = build_listing_line(item)
        candidate = f"{current_chunk}\n{line}"

        if len(candidate) <= MAX_MESSAGE_LENGTH:
            current_chunk = candidate
            continue

        chunks.append(current_chunk)
        current_chunk = f"UPDATE\n{line}"

    if current_chunk:
        chunks.append(current_chunk)

    for chunk in chunks:
        await ctx.send(chunk)

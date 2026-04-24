from discord.ext import commands


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

    message = "UPDATE\n" + "\n".join(build_listing_line(item) for item in items)
    await ctx.send(message)


class ListingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list")
    async def list_command(self, ctx):
        await send_list(ctx)

    @commands.command()
    async def search(self, ctx, *, keyword):
        results = self.bot.store.search(keyword)

        if not results:
            await ctx.send(f"Geen resultaten gevonden voor '{keyword}'.")
            return

        await send_list(ctx, results)

    @commands.command()
    async def helpme(self, ctx):
        help_text = (
            "!list\n"
            "!sold <zoekwoord>\n"
            "!forsale <zoekwoord>\n"
            "!remove <id>\n"
            "!search <zoekwoord>\n"
            "!add adres | stad | land | prijs | optionele notitie"
        )
        await ctx.send(f"```{help_text}```")


async def setup(bot):
    await bot.add_cog(ListingsCog(bot))

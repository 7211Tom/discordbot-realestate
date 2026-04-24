from discord.ext import commands

from utils.guards import ensure_editor, is_allowed_channel
from utils.messages import send_list


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, *, text):
        if not is_allowed_channel(ctx):
            return

        if not await ensure_editor(ctx):
            return

        if "|" in text:
            parts = [part.strip() for part in text.split("|")]
        else:
            parts = [part.strip() for part in text.split(",")]

        if len(parts) < 4:
            await ctx.send(
                "Gebruik: !add adres | stad | land | prijs | optionele notitie"
            )
            return

        try:
            listing = self.bot.store.add_listing(parts)
        except ValueError:
            await ctx.send(
                "Ongeldige prijs. Gebruik alleen cijfers, bijvoorbeeld 250000 of 250000.50."
            )
            return

        await ctx.send(f"Toegevoegd: #{listing['id']} {listing['address']}")
        await send_list(ctx)

    @commands.command()
    async def sold(self, ctx, *, keyword):
        if not is_allowed_channel(ctx):
            return

        if not await ensure_editor(ctx):
            return

        item = self.bot.store.mark_sold(keyword)

        if not item:
            await ctx.send(f"Geen match gevonden voor '{keyword}'.")
            return

        await ctx.send(f"Gemarkeerd als SOLD: {item['address']}")
        await send_list(ctx)

    @commands.command()
    async def forsale(self, ctx, *, keyword):
        if not is_allowed_channel(ctx):
            return

        if not await ensure_editor(ctx):
            return

        item = self.bot.store.mark_for_sale(keyword)

        if not item:
            await ctx.send(f"Geen verkochte match gevonden voor '{keyword}'.")
            return

        await ctx.send(f"Terug op FOR SALE: {item['address']}")
        await send_list(ctx)

    @commands.command(name="remove")
    async def remove_listing(self, ctx, listing_id: str):
        if not is_allowed_channel(ctx):
            return

        if not await ensure_editor(ctx):
            return

        item = self.bot.store.remove_listing(listing_id)

        if not item:
            await ctx.send(
                "Geen geldige ID gevonden. Gebruik eerst !list of !search en daarna bv. !remove 7"
            )
            return

        await ctx.send(f"Verwijderd: #{item['id']} {item['address']}")
        await send_list(ctx)


async def setup(bot):
    await bot.add_cog(AdminCog(bot))

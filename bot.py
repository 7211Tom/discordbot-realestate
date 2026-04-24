import json
import os

import discord
from discord.ext import commands


def load_dotenv(path=".env"):
    if not os.path.exists(path):
        return

    with open(path, encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DATA_FILE = "listings.json"

if not TOKEN:
    raise RuntimeError(
        "DISCORD_BOT_TOKEN ontbreekt. Zet je token in het .env bestand."
    )


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


DEFAULT_LISTINGS = [
    {
        "address": "Travessa Da Povoa 263",
        "city": "Porto",
        "country": "Portugal",
        "price": "3",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "111 Cornelia St",
        "city": "Brooklyn",
        "country": "USA",
        "price": "",
        "status": "SOLD",
        "note": "",
        "recent": False,
    },
    {
        "address": "7 Rue Emile Connoy",
        "city": "St Denis",
        "country": "France",
        "price": "4",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "25908 81St Ave",
        "city": "Queens",
        "country": "USA",
        "price": "",
        "status": "SOLD",
        "note": "thx @Athex",
        "recent": False,
    },
    {
        "address": "58 Stoke Poges Ln",
        "city": "Slough",
        "country": "UK",
        "price": "4",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "1784 SW 11TH",
        "city": "Miami",
        "country": "Florida, USA",
        "price": "5",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "52 Scott's Hill Road",
        "city": "Bermuda",
        "country": "Bermuda",
        "price": "",
        "status": "SOLD",
        "note": "",
        "recent": False,
    },
    {
        "address": "Via Muzio Oddi",
        "city": "Rome",
        "country": "Italy",
        "price": "",
        "status": "SOLD",
        "note": "",
        "recent": False,
    },
    {
        "address": "232 New John St West",
        "city": "Birmingham",
        "country": "UK",
        "price": "5",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "4 Fielders Lane",
        "city": "Bermuda",
        "country": "Bermuda",
        "price": "",
        "status": "SOLD",
        "note": "",
        "recent": False,
    },
    {
        "address": "17 Hochstrasse",
        "city": "Berlin",
        "country": "Germany",
        "price": "6",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "5412 Shippee Ln",
        "city": "Stockton",
        "country": "California, USA",
        "price": "7",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "37 Via Carlo Em.",
        "city": "Rome",
        "country": "Italy",
        "price": "",
        "status": "SOLD",
        "note": "thx @JohnFrifri",
        "recent": False,
    },
    {
        "address": "2 Chome 46 10",
        "city": "Shibuya City, Tokyo",
        "country": "Japan",
        "price": "8",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "5586 Black Oak Dr",
        "city": "Stockton",
        "country": "California, USA",
        "price": "8.5",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "212 New John St West",
        "city": "Birmingham",
        "country": "UK",
        "price": "9",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "2323 Comstock Dr",
        "city": "Park City",
        "country": "Utah, USA",
        "price": "",
        "status": "SOLD",
        "note": "",
        "recent": False,
    },
    {
        "address": "185 MCDONALD AVE",
        "city": "Brooklyn",
        "country": "NY, USA",
        "price": "10",
        "status": "FOR SALE",
        "note": "park view",
        "recent": False,
    },
    {
        "address": "17 Crest View",
        "city": "Smiths Parish",
        "country": "Bermuda",
        "price": "",
        "status": "SOLD",
        "note": "thx @Athex",
        "recent": False,
    },
    {
        "address": "93 Ilbert St",
        "city": "London",
        "country": "UK",
        "price": "10",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "1 Pokio Cresent",
        "city": "Smiths Parish",
        "country": "Bermuda",
        "price": "",
        "status": "SOLD",
        "note": "thx @Athex",
        "recent": False,
    },
    {
        "address": "8624 Musket St",
        "city": "Bellerose, Queens",
        "country": "USA",
        "price": "22",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "8108 252nd St",
        "city": "Bellerose, Queens",
        "country": "USA",
        "price": "",
        "status": "SOLD",
        "note": "thx @Shaktilyn",
        "recent": False,
    },
    {
        "address": "901B Avenue B",
        "city": "Treasure Island, San Francisco",
        "country": "California, USA",
        "price": "26",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
    {
        "address": "2 Thaynex Canyon Way",
        "city": "Park City",
        "country": "Utah, USA",
        "price": "45",
        "status": "FOR SALE",
        "note": "",
        "recent": False,
    },
]


def normalize_listings(items):
    normalized = []
    for index, item in enumerate(items, start=1):
        normalized_item = {
            "address": item.get("address", "").strip(),
            "city": item.get("city", "").strip(),
            "country": item.get("country", "").strip(),
            "price": str(item.get("price", "")).strip(),
            "status": item.get("status", "FOR SALE").strip().upper(),
            "note": item.get("note", "").strip(),
            "recent": bool(item.get("recent", False)),
            "id": index,
        }
        normalized.append(normalized_item)

    return normalized


def save_listings():
    with open(DATA_FILE, "w", encoding="utf-8") as data_file:
        json.dump(listings, data_file, ensure_ascii=False, indent=2)


def load_listings():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding="utf-8") as data_file:
            loaded = json.load(data_file)
        return normalize_listings(loaded)

    loaded = normalize_listings(DEFAULT_LISTINGS)
    with open(DATA_FILE, "w", encoding="utf-8") as data_file:
        json.dump(loaded, data_file, ensure_ascii=False, indent=2)
    return loaded


listings = load_listings()


def refresh_ids():
    for index, item in enumerate(listings, start=1):
        item["id"] = index


refresh_ids()


def clear_recent_flags():
    for item in listings:
        item["recent"] = False


def find_listing(keyword, prefer_status=None):
    keyword = keyword.lower().strip()

    matches = []
    for item in listings:
        haystack = " | ".join(
            [
                item["address"],
                item["city"],
                item["country"],
                item["note"],
            ]
        ).lower()
        if keyword in haystack:
            matches.append(item)

    if prefer_status:
        preferred = [item for item in matches if item["status"] == prefer_status]
        if preferred:
            return preferred[0]

    return matches[0] if matches else None


def find_listing_by_id(raw_value):
    try:
        listing_id = int(raw_value)
    except ValueError:
        return None

    for item in listings:
        if item["id"] == listing_id:
            return item

    return None


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
    items = items_to_show if items_to_show is not None else listings

    if not items:
        await ctx.send("Lijst is leeg.")
        return

    message = "UPDATE\n" + "\n".join(build_listing_line(item) for item in items)
    await ctx.send(message)


@bot.event
async def on_ready():
    print(f"Bot is online als {bot.user}")


@bot.command(name="list")
async def list_command(ctx):
    await send_list(ctx)


@bot.command()
async def add(ctx, *, text):
    if "|" in text:
        parts = [part.strip() for part in text.split("|")]
    else:
        parts = [part.strip() for part in text.split(",")]

    if len(parts) < 4:
        await ctx.send(
            "Gebruik: !add adres | stad | land | prijs | optionele notitie"
        )
        return

    listing = {
        "address": parts[0],
        "city": parts[1],
        "country": parts[2],
        "price": parts[3],
        "status": "FOR SALE",
        "note": parts[4] if len(parts) > 4 else "",
        "recent": False,
    }

    clear_recent_flags()
    listing["id"] = max((item["id"] for item in listings), default=0) + 1
    listing["recent"] = True
    listings.append(listing)
    save_listings()

    await ctx.send(f"Toegevoegd: #{listing['id']} {listing['address']}")
    await send_list(ctx)


@bot.command()
async def sold(ctx, *, keyword):
    item = find_listing(keyword, prefer_status="FOR SALE")

    if not item:
        await ctx.send(f"Geen match gevonden voor '{keyword}'.")
        return

    clear_recent_flags()
    item["status"] = "SOLD"
    item["recent"] = True
    save_listings()

    await ctx.send(f"Gemarkeerd als SOLD: {item['address']}")
    await send_list(ctx)


@bot.command()
async def forsale(ctx, *, keyword):
    item = find_listing(keyword, prefer_status="SOLD")

    if not item:
        await ctx.send(f"Geen verkochte match gevonden voor '{keyword}'.")
        return

    clear_recent_flags()
    item["status"] = "FOR SALE"
    item["recent"] = True
    save_listings()

    await ctx.send(f"Terug op FOR SALE: {item['address']}")
    await send_list(ctx)


@bot.command(name="remove")
async def remove_listing(ctx, listing_id: str):
    item = find_listing_by_id(listing_id)

    if not item:
        await ctx.send(
            "Geen geldige ID gevonden. Gebruik eerst !list of !search en daarna bv. !remove 7"
        )
        return

    listings.remove(item)
    clear_recent_flags()
    refresh_ids()
    save_listings()

    await ctx.send(f"Verwijderd: #{item['id']} {item['address']}")
    await send_list(ctx)


@bot.command()
async def search(ctx, *, keyword):
    keyword = keyword.lower().strip()
    results = [
        item
        for item in listings
        if keyword in item["address"].lower()
        or keyword in item["city"].lower()
        or keyword in item["country"].lower()
        or keyword in item["status"].lower()
        or keyword in item["note"].lower()
    ]

    if not results:
        await ctx.send(f"Geen resultaten gevonden voor '{keyword}'.")
        return

    await send_list(ctx, results)


@bot.command()
async def helpme(ctx):
    help_text = (
        "!list\n"
        "!sold <zoekwoord>\n"
        "!forsale <zoekwoord>\n"
        "!remove <id>\n"
        "!search <zoekwoord>\n"
        "!add adres | stad | land | prijs | optionele notitie"
    )
    await ctx.send(f"```{help_text}```")


bot.run(TOKEN)

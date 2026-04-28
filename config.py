import os


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

            if key:
                os.environ[key] = value


load_dotenv()


def parse_csv_env(value):
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OWNER_DISCORD_ID = os.getenv("OWNER_DISCORD_ID")
OWNER_DISCORD_IDS = parse_csv_env(os.getenv("OWNER_DISCORD_IDS"))
if OWNER_DISCORD_ID and OWNER_DISCORD_ID.strip():
    OWNER_DISCORD_IDS = [OWNER_DISCORD_ID.strip(), *OWNER_DISCORD_IDS]
OWNER_DISCORD_IDS = tuple(dict.fromkeys(OWNER_DISCORD_IDS))
GUILD_ID = os.getenv("GUILD_ID")
ALLOWED_CHANNEL_NAME = os.getenv("ALLOWED_CHANNEL_NAME", "for-sale💰").strip()
FOR_SALE_INDICATOR = os.getenv("FOR_SALE_INDICATOR", "🟢").strip()
SOLD_INDICATOR = os.getenv("SOLD_INDICATOR", "🔴").strip()
DB_FILE = os.path.join(DATA_DIR, "listings.db")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_BOT_TOKEN is missing. Set your token in the .env file."
    )

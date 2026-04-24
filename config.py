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

            if key and key not in os.environ:
                os.environ[key] = value


load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OWNER_DISCORD_ID = os.getenv("OWNER_DISCORD_ID")
DATA_FILE = "listings.json"

if not TOKEN:
    raise RuntimeError(
        "DISCORD_BOT_TOKEN ontbreekt. Zet je token in het .env bestand."
    )

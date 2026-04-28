# Discord Real Estate Bot

Discord bot for publishing and managing a real estate listing board with slash commands and SQLite storage.

User-facing lookups are private by default (`/list`, `/search`), while owners can still post a public board update with `/public_list`.

## Features

- Private embed responses for normal user lookup commands.
- Public board publishing for owners via `/public_list`.
- Owner-only listing management: add, mark sold, relist, remove.
- Runtime owner authorization with support for single or multiple owner IDs.
- SQLite-backed storage with automatic table initialization.
- Configurable channel name and status indicators.
- Pagination-friendly embed rendering with summary stats and timestamps.

## Project Structure

```text
bot.py                 # bot startup and cog loading
config.py              # .env loading and runtime settings
cogs/
  listings.py          # public/user command handlers
  admin.py             # owner edit command handlers
data/
  listings.py          # ListingStore (SQLite CRUD)
utils/
  guards.py            # channel + owner authorization guards
  messages.py          # embed/text formatting + response helpers
seed_listings.py       # optional DB seed from listings.json
```

## Quick Start

### 1) Install

```bash
python -m pip install -r requirements.txt
```

### 2) Configure environment

```bash
cp .env.example .env
```

Example:

```env
DISCORD_BOT_TOKEN=your_bot_token
OWNER_DISCORD_ID=your_primary_discord_user_id
OWNER_DISCORD_IDS=your_discord_user_id_1,your_discord_user_id_2
GUILD_ID=your_server_id
ALLOWED_CHANNEL_NAME=for-sale💰
FOR_SALE_INDICATOR=🟢
SOLD_INDICATOR=🔴
```

### 3) Run locally

```bash
python bot.py
```

The bot loads `.env`, initializes `data/listings.db`, loads cogs, and syncs slash commands (guild-scoped when `GUILD_ID` is set).

## Environment Variables

- `DISCORD_BOT_TOKEN` (required): bot token from Discord Developer Portal.
- `OWNER_DISCORD_ID` (optional): single owner ID (legacy/backward-compatible).
- `OWNER_DISCORD_IDS` (optional): comma-separated owner IDs.
- `GUILD_ID` (optional): guild ID for faster command sync during development.
- `ALLOWED_CHANNEL_NAME` (optional, default `for-sale💰`): allowed channel for owner edit/admin commands that enforce channel guard.
- `FOR_SALE_INDICATOR` (optional, default `🟢`): indicator shown for active listings.
- `SOLD_INDICATOR` (optional, default `🔴`): indicator shown for sold listings.

Notes:

- You can use `OWNER_DISCORD_ID`, `OWNER_DISCORD_IDS`, or both.  
  If both are set, they are merged and deduplicated.
- You can use custom Discord emoji for indicators:

```env
FOR_SALE_INDICATOR=<:green_light:123456789012345678>
SOLD_INDICATOR=<:red_light:123456789012345678>
```

## Commands

### User Commands (private responses)

```text
/help
/list
/search keyword:<keyword>
```

- Return ephemeral embeds (only visible to the user who ran the command).
- Can be used in any channel because they do not post public messages.

### Owner Commands

```text
/public_list
/commands
/add address:<address> city:<city> country:<country> price:<price> note:<note>
/sold keyword:<keyword>
/forsale keyword:<keyword>
/remove listing_id:<id>
```

Authorization behavior:

- Hidden from regular user autocomplete via Discord command default permissions.
- Runtime authorization in `utils/guards.py` enforces configured owner IDs.

Channel behavior:

- `/add`, `/sold`, `/forsale`, `/remove`, `/commands` enforce `ALLOWED_CHANNEL_NAME`.
- `/public_list` is owner-restricted but currently does not enforce channel guard; it posts publicly in the channel where the command is executed.

## Listing Output Format

Listings are rendered as embeds with:

- One listing line per item (id, status icon, address, location, price/status, optional note).
- `RECENT` badge on the most recently updated sold listing.
- Board summary field (`for sale | sold | total`).
- Page footer (`Listing Board | Page x/y`) and timestamp.

`/list` and `/public_list` share the same embed rendering; the difference is visibility:

- `/list`: private/ephemeral
- `/public_list`: public

## Data and Seeding

SQLite database path:

```text
data/listings.db
```

Seed from `listings.json`:

```bash
python seed_listings.py
```

Replace existing data:

```bash
python seed_listings.py --force
```

## Discord Setup

Invite scopes:

```text
bot
applications.commands
```

Suggested bot permissions:

```text
Send Messages
Use Slash Commands
Embed Links
```

Privileged intents are not required for this slash-command workflow.

## Docker

Run with Docker Compose:

```bash
docker compose up -d
```

## Security Notes

- Never commit `.env` or real bot tokens.
- Rotate token immediately if exposed.
- Runtime owner checks enforce `OWNER_DISCORD_ID` / `OWNER_DISCORD_IDS` even if command visibility settings are misconfigured.
- `.env` values loaded by `config.py` populate process environment for this project at startup.

# Discord Real Estate Bot

A small Discord bot for publishing and managing a real estate listing board.

The bot stores listings in SQLite, exposes Discord slash commands, and keeps public channel noise low by returning normal user lookups as private ephemeral responses. The bot owner can still publish a public board update when needed.

## Features

- Private `/list` command for users to view all listings without spamming a channel.
- Private `/search` command for users to search by address, city, country, status, or note.
- Owner-only listing management commands for adding, selling, relisting, and removing listings.
- Owner-only `/public_list` command for posting the full board publicly.
- Owner-only `/commands` command for viewing the full command overview.
- Discord permission defaults hide owner/admin commands from normal user autocomplete.
- SQLite-backed listing storage with automatic schema initialization.
- Configurable status indicators for for-sale and sold listings.

## Getting Started

### Installation

```bash
python -m pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Fill in the required values:

```env
DISCORD_BOT_TOKEN=your_bot_token
OWNER_DISCORD_ID=your_discord_user_id
GUILD_ID=your_server_id
ALLOWED_CHANNEL_NAME=for-sale💰
FOR_SALE_INDICATOR=🟢
SOLD_INDICATOR=🔴
```

Required variables:

- `DISCORD_BOT_TOKEN`: Bot token from the Discord Developer Portal.
- `OWNER_DISCORD_ID`: Discord user ID that is allowed to manage listings.
- `GUILD_ID`: Discord server ID used for fast guild command syncing.
- `ALLOWED_CHANNEL_NAME`: Channel name where owner-only public/admin commands are allowed.

Optional variables:

- `FOR_SALE_INDICATOR`: Indicator shown before for-sale listings.
- `SOLD_INDICATOR`: Indicator shown before sold listings.

You can use custom Discord emoji for the indicators, for example:

```env
FOR_SALE_INDICATOR=<:green_light:123456789012345678>
SOLD_INDICATOR=<:red_light:123456789012345678>
```

## Development

Run the bot locally:

```bash
python bot.py
```

The bot will:

- Load `.env`
- Initialize `data/listings.db`
- Load cogs from `cogs/`
- Sync slash commands to `GUILD_ID` if configured

## Commands

### Public User Commands

These commands are available to normal users and return private ephemeral embeds:

```text
/help
/list
/search keyword:<keyword>
```

They can be used in any server channel because they do not post public messages.

### Owner Commands

These commands are hidden from normal user autocomplete with Discord command permissions and also protected at runtime by `OWNER_DISCORD_ID`:

```text
/commands
/public_list
/add address:<address> city:<city> country:<country> price:<price> note:<note>
/sold keyword:<keyword>
/forsale keyword:<keyword>
/remove listing_id:<id>
```

`/public_list` posts a normal public Discord message with the full board, using the larger regular Discord message text rather than embed body text.

## Listing Format

Public board lines are formatted like:

```text
#1 🟢 123 Main St - **Porto, Portugal** - FOR SALE - **$ 3**
#2 `RECENT` 🔴 456 Sold St - **Roubaix, USA** - SOLD
```

The `RECENT` badge is shown on the most recently updated sold listing.

## Data

Listings are stored in SQLite at:

```text
data/listings.db
```

The database file is ignored by Git.

To seed from `listings.json`:

```bash
python seed_listings.py
```

To replace existing database contents:

```bash
python seed_listings.py --force
```

## Discord Setup

Invite the bot with these scopes:

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

Privileged intents are not required for the slash-command workflow.

## Deployment

The included `docker-compose.yml` can run the bot in Docker:

```bash
docker compose up -d
```

For local development, running `python bot.py` is enough.

## Security Notes

- Never commit `.env` or a real Discord bot token.
- If a token is exposed, reset it immediately in the Discord Developer Portal.
- Owner/admin commands are hidden from normal users, but runtime checks still enforce `OWNER_DISCORD_ID`.
- `.env` values override existing process environment variables for this project.

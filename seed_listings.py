import argparse
import json
import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_JSON_FILE = os.path.join(BASE_DIR, "listings.json")
DEFAULT_DB_FILE = os.path.join(BASE_DIR, "data", "listings.db")


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    price REAL NULL,
    status TEXT NOT NULL DEFAULT 'FOR SALE'
        CHECK(status IN ('FOR SALE', 'SOLD')),
    note TEXT NOT NULL DEFAULT '',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


def normalize_price(raw_value):
    if raw_value in (None, ""):
        return None

    value = str(raw_value).strip().replace("$", "").replace(",", "").strip()
    if not value:
        return None

    return float(value)


def normalize_status(raw_value):
    status = str(raw_value or "FOR SALE").strip().upper()
    if status not in {"FOR SALE", "SOLD"}:
        return "FOR SALE"
    return status


def load_json(path):
    with open(path, encoding="utf-8") as json_file:
        items = json.load(json_file)

    if not isinstance(items, list):
        raise ValueError(f"{path} moet een JSON-lijst bevatten.")

    return items


def seed_database(json_file, db_file, force=False):
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    items = load_json(json_file)

    with sqlite3.connect(db_file) as connection:
        connection.execute(CREATE_TABLE_SQL)

        existing_count = connection.execute(
            "SELECT COUNT(*) FROM listings"
        ).fetchone()[0]

        if existing_count and not force:
            raise RuntimeError(
                f"Database bevat al {existing_count} listings. "
                "Gebruik --force als je de tabel eerst wil leegmaken."
            )

        if force:
            connection.execute("DELETE FROM listings")
            connection.execute(
                "DELETE FROM sqlite_sequence WHERE name = 'listings'"
            )

        imported_count = 0
        skipped_count = 0

        for item in items:
            if not isinstance(item, dict):
                skipped_count += 1
                continue

            address = str(item.get("address", "")).strip()
            city = str(item.get("city", "")).strip()
            country = str(item.get("country", "")).strip()

            if not address or not city or not country:
                skipped_count += 1
                continue

            listing_id = item.get("id")
            price = normalize_price(item.get("price"))
            status = normalize_status(item.get("status"))
            note = str(item.get("note", "")).strip()

            if listing_id in (None, ""):
                connection.execute(
                    """
                    INSERT INTO listings (
                        address, city, country, price, status, note, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    (address, city, country, price, status, note),
                )
            else:
                connection.execute(
                    """
                    INSERT INTO listings (
                        id, address, city, country, price, status, note, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    (
                        int(listing_id),
                        address,
                        city,
                        country,
                        price,
                        status,
                        note,
                    ),
                )

            imported_count += 1

    return imported_count, skipped_count


def main():
    parser = argparse.ArgumentParser(
        description="Vul data/listings.db met data uit listings.json."
    )
    parser.add_argument("--json", default=DEFAULT_JSON_FILE, help="Pad naar listings.json")
    parser.add_argument("--db", default=DEFAULT_DB_FILE, help="Pad naar listings.db")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Maak de listings-tabel eerst leeg als er al data in zit.",
    )
    args = parser.parse_args()

    imported_count, skipped_count = seed_database(args.json, args.db, args.force)
    print(f"Geimporteerd: {imported_count} listings")
    print(f"Overgeslagen: {skipped_count} items")
    print(f"Database: {args.db}")


if __name__ == "__main__":
    main()

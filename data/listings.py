import logging
import os
import sqlite3

from config import DB_FILE


logger = logging.getLogger(__name__)


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


class ListingStore:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        self._initialize_database()

    @property
    def listings(self):
        return self.fetch_all()

    def _get_connection(self):
        connection = sqlite3.connect(self.db_file)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self):
        with self._get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS listings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    country TEXT NOT NULL,
                    price TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL,
                    note TEXT NOT NULL DEFAULT '',
                    recent INTEGER NOT NULL DEFAULT 0
                )
                """
            )

            row_count = connection.execute(
                "SELECT COUNT(*) FROM listings"
            ).fetchone()[0]
            if row_count:
                logger.info("SQLite database loaded with %s listings", row_count)
                return

            seed_items = self._normalize_seed_items(DEFAULT_LISTINGS)
            self._insert_many(connection, seed_items)
            logger.info("SQLite database initialized with %s default listings", len(seed_items))

    def _normalize_seed_items(self, items):
        normalized = []
        for index, item in enumerate(items, start=1):
            normalized.append(
                {
                    "id": int(item.get("id", index)),
                    "address": item.get("address", "").strip(),
                    "city": item.get("city", "").strip(),
                    "country": item.get("country", "").strip(),
                    "price": str(item.get("price", "")).strip(),
                    "status": item.get("status", "FOR SALE").strip().upper(),
                    "note": item.get("note", "").strip(),
                    "recent": 1 if item.get("recent", False) else 0,
                }
            )
        return normalized

    def _insert_many(self, connection, items):
        connection.executemany(
            """
            INSERT INTO listings (id, address, city, country, price, status, note, recent)
            VALUES (:id, :address, :city, :country, :price, :status, :note, :recent)
            """,
            items,
        )

    def _row_to_listing(self, row):
        return {
            "id": row["id"],
            "address": row["address"],
            "city": row["city"],
            "country": row["country"],
            "price": row["price"],
            "status": row["status"],
            "note": row["note"],
            "recent": bool(row["recent"]),
        }

    def fetch_all(self):
        with self._get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, address, city, country, price, status, note, recent
                FROM listings
                ORDER BY id
                """
            ).fetchall()
        return [self._row_to_listing(row) for row in rows]

    def clear_recent_flags(self):
        with self._get_connection() as connection:
            connection.execute("UPDATE listings SET recent = 0")

    def find_listing(self, keyword, prefer_status=None):
        term = f"%{keyword.lower().strip()}%"
        query = """
            SELECT id, address, city, country, price, status, note, recent
            FROM listings
            WHERE LOWER(address) LIKE ?
               OR LOWER(city) LIKE ?
               OR LOWER(country) LIKE ?
               OR LOWER(note) LIKE ?
        """
        params = [term, term, term, term]

        if prefer_status:
            query += " AND status = ?"
            params.append(prefer_status)

        query += " ORDER BY id LIMIT 1"

        with self._get_connection() as connection:
            row = connection.execute(query, tuple(params)).fetchone()

        return self._row_to_listing(row) if row else None

    def find_listing_by_id(self, raw_value):
        try:
            listing_id = int(raw_value)
        except ValueError:
            return None

        with self._get_connection() as connection:
            row = connection.execute(
                """
                SELECT id, address, city, country, price, status, note, recent
                FROM listings
                WHERE id = ?
                """,
                (listing_id,),
            ).fetchone()

        return self._row_to_listing(row) if row else None

    def search(self, keyword):
        term = f"%{keyword.lower().strip()}%"
        with self._get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, address, city, country, price, status, note, recent
                FROM listings
                WHERE LOWER(address) LIKE ?
                   OR LOWER(city) LIKE ?
                   OR LOWER(country) LIKE ?
                   OR LOWER(status) LIKE ?
                   OR LOWER(note) LIKE ?
                ORDER BY id
                """,
                (term, term, term, term, term),
            ).fetchall()

        return [self._row_to_listing(row) for row in rows]

    def add_listing(self, parts):
        self.clear_recent_flags()
        with self._get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO listings (address, city, country, price, status, note, recent)
                VALUES (?, ?, ?, ?, 'FOR SALE', ?, 1)
                """,
                (
                    parts[0],
                    parts[1],
                    parts[2],
                    parts[3],
                    parts[4] if len(parts) > 4 else "",
                ),
            )
            listing_id = cursor.lastrowid
        logger.info("Added listing #%s: %s", listing_id, parts[0])

        return self.find_listing_by_id(listing_id)

    def mark_sold(self, keyword):
        item = self.find_listing(keyword, prefer_status="FOR SALE")
        if not item:
            return None

        self.clear_recent_flags()
        with self._get_connection() as connection:
            connection.execute(
                "UPDATE listings SET status = 'SOLD', recent = 1 WHERE id = ?",
                (item["id"],),
            )
        logger.info("Marked listing #%s as SOLD", item["id"])

        return self.find_listing_by_id(item["id"])

    def mark_for_sale(self, keyword):
        item = self.find_listing(keyword, prefer_status="SOLD")
        if not item:
            return None

        self.clear_recent_flags()
        with self._get_connection() as connection:
            connection.execute(
                "UPDATE listings SET status = 'FOR SALE', recent = 1 WHERE id = ?",
                (item["id"],),
            )
        logger.info("Marked listing #%s as FOR SALE", item["id"])

        return self.find_listing_by_id(item["id"])

    def remove_listing(self, listing_id):
        item = self.find_listing_by_id(listing_id)
        if not item:
            return None

        with self._get_connection() as connection:
            connection.execute("DELETE FROM listings WHERE id = ?", (item["id"],))
        logger.info("Removed listing #%s: %s", item["id"], item["address"])

        return item

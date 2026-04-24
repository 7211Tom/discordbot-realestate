import logging
import os
import sqlite3

from config import DB_FILE


logger = logging.getLogger(__name__)


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
            self._create_table(connection)
            self._migrate_price_column_if_needed(connection)

            row_count = connection.execute(
                "SELECT COUNT(*) FROM listings"
            ).fetchone()[0]
            if row_count:
                logger.info("SQLite database loaded with %s listings", row_count)
                return

            logger.info("SQLite database initialized with an empty listings table")

    def _create_table(self, connection, table_name="listings"):
        connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                price REAL NULL,
                status TEXT NOT NULL,
                note TEXT NOT NULL DEFAULT '',
                recent INTEGER NOT NULL DEFAULT 0
            )
            """
        )

    def _migrate_price_column_if_needed(self, connection):
        columns = connection.execute("PRAGMA table_info(listings)").fetchall()
        price_column = next((column for column in columns if column[1] == "price"), None)

        if not price_column or price_column[2].upper() == "REAL":
            return

        logger.info("Migrating listings.price from TEXT to REAL")
        self._create_table(connection, table_name="listings_new")
        connection.execute(
            """
            INSERT INTO listings_new (id, address, city, country, price, status, note, recent)
            SELECT
                id,
                address,
                city,
                country,
                CASE
                    WHEN TRIM(COALESCE(price, '')) = '' THEN NULL
                    ELSE CAST(price AS REAL)
                END,
                status,
                note,
                recent
            FROM listings
            """
        )
        connection.execute("DROP TABLE listings")
        connection.execute("ALTER TABLE listings_new RENAME TO listings")
        logger.info("Price column migration completed")

    def _normalize_price(self, raw_value):
        if raw_value in (None, ""):
            return None

        return float(str(raw_value).strip())

    def _display_price(self, raw_value):
        if raw_value is None:
            return None

        number = float(raw_value)
        if number.is_integer():
            return str(int(number))
        return str(number)

    def _row_to_listing(self, row):
        return {
            "id": row["id"],
            "address": row["address"],
            "city": row["city"],
            "country": row["country"],
            "price": self._display_price(row["price"]),
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
                    self._normalize_price(parts[3]),
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

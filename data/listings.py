import json
import os

from config import DATA_FILE


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
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.listings = self.load_listings()
        self.refresh_ids()

    def normalize_listings(self, items):
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

    def save_listings(self):
        with open(self.data_file, "w", encoding="utf-8") as data_file:
            json.dump(self.listings, data_file, ensure_ascii=False, indent=2)

    def load_listings(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, encoding="utf-8") as data_file:
                loaded = json.load(data_file)
            return self.normalize_listings(loaded)

        loaded = self.normalize_listings(DEFAULT_LISTINGS)
        with open(self.data_file, "w", encoding="utf-8") as data_file:
            json.dump(loaded, data_file, ensure_ascii=False, indent=2)
        return loaded

    def refresh_ids(self):
        for index, item in enumerate(self.listings, start=1):
            item["id"] = index

    def clear_recent_flags(self):
        for item in self.listings:
            item["recent"] = False

    def find_listing(self, keyword, prefer_status=None):
        keyword = keyword.lower().strip()

        matches = []
        for item in self.listings:
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

    def find_listing_by_id(self, raw_value):
        try:
            listing_id = int(raw_value)
        except ValueError:
            return None

        for item in self.listings:
            if item["id"] == listing_id:
                return item

        return None

    def search(self, keyword):
        keyword = keyword.lower().strip()
        return [
            item
            for item in self.listings
            if keyword in item["address"].lower()
            or keyword in item["city"].lower()
            or keyword in item["country"].lower()
            or keyword in item["status"].lower()
            or keyword in item["note"].lower()
        ]

    def add_listing(self, parts):
        listing = {
            "address": parts[0],
            "city": parts[1],
            "country": parts[2],
            "price": parts[3],
            "status": "FOR SALE",
            "note": parts[4] if len(parts) > 4 else "",
            "recent": False,
        }

        self.clear_recent_flags()
        listing["id"] = max((item["id"] for item in self.listings), default=0) + 1
        listing["recent"] = True
        self.listings.append(listing)
        self.save_listings()
        return listing

    def mark_sold(self, keyword):
        item = self.find_listing(keyword, prefer_status="FOR SALE")
        if not item:
            return None

        self.clear_recent_flags()
        item["status"] = "SOLD"
        item["recent"] = True
        self.save_listings()
        return item

    def mark_for_sale(self, keyword):
        item = self.find_listing(keyword, prefer_status="SOLD")
        if not item:
            return None

        self.clear_recent_flags()
        item["status"] = "FOR SALE"
        item["recent"] = True
        self.save_listings()
        return item

    def remove_listing(self, listing_id):
        item = self.find_listing_by_id(listing_id)
        if not item:
            return None

        self.listings.remove(item)
        self.clear_recent_flags()
        self.refresh_ids()
        self.save_listings()
        return item

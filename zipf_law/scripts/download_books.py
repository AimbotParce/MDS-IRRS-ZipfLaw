import configparser
import os
import random
import urllib.request

import pandas as pd

config = configparser.ConfigParser()
config.read("config.ini")
books_per_language = config.getint("Download", "BooksPerLanguage", fallback=10)
if books_per_language <= 0:
    raise ValueError("Books per language is set to 0 or negative, exiting.")
strategy = config.get("Download", "Strategy", fallback="popular").lower()
if not strategy in ["popular", "random"]:
    raise ValueError(f"Unknown strategy: {strategy}")

CATALOG_FILE = "data/processed/catalog.csv"
DOWNLOAD_URL = "https://www.gutenberg.org/ebooks/{pub_id}.txt.utf-8"
OUT_DIR = "data/raw/books/"

if __name__ == "__main__":
    catalog = pd.read_csv(CATALOG_FILE, header=0)
    print(f"Catalog loaded with {len(catalog)} entries.")

    # Group books by language (remove languages with ";" in them)
    languages = catalog[~catalog["languages"].str.contains(";")].groupby("languages")
    print(f"Found {len(languages)} languages.")
    for lang, group in languages:
        print(f"Downloading books for language: {lang}")
        if strategy == "popular":
            group = group.sort_values("downloads", ascending=False)
            selected = group.head(books_per_language)
        else:  # random
            selected = group.sample(min(books_per_language, len(group)), random_state=42)

        for _, row in selected.iterrows():
            pub_id = row["id"]
            filename = os.path.join(OUT_DIR, str(lang), f"{pub_id}.txt")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            url = DOWNLOAD_URL.format(pub_id=pub_id)
            try:
                urllib.request.urlretrieve(url, filename)
            except Exception as e:
                print(f"    Failed to download book {pub_id}: {e}")
                if os.path.exists(filename):
                    os.remove(filename)

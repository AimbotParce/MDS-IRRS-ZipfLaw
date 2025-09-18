from collections import defaultdict
import configparser
import csv
import os
import random
import urllib.request

config = configparser.ConfigParser()
config.read("config.ini")
books_per_language = config.getint("Download", "BooksPerLanguage", fallback=10)

with open("data/raw/pg_catalog.csv", "r", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip header row
    books_by_language = defaultdict(list)
    for pub_id, pub_type, _, pub_title, pub_lang, _, pub_subject, _, _ in reader:
        if pub_type == "Text" and pub_lang and not len(pub_lang.split(";")) > 1:
            books_by_language[pub_lang].append((pub_id, pub_title, pub_subject))

random.seed(42)

print(f"Downloading up to {books_per_language} books for {len(books_by_language)} languages.")
for lang, books in books_by_language.items():
    # Randomly sample books_per_language from each language
    sampled_books = random.sample(books, min(books_per_language, len(books)))
    output_dir = f"data/raw/books/{lang}"
    os.makedirs(output_dir, exist_ok=True)
    for pub_id, pub_title, pub_subject in sampled_books:
        print(f"Downloading Language: {lang}, Book ID: {pub_id}, Title: {pub_title}")
        url = f"https://www.gutenberg.org/ebooks/{pub_id}.txt.utf-8"
        output_file = os.path.join(output_dir, f"{pub_id}.txt")
        urllib.request.urlretrieve(url, output_file)
        # Save metadata
        with open(os.path.join(output_dir, f"{pub_id}_metadata.txt"), "w", encoding="utf-8") as metafile:
            metafile.write(f"Title: {pub_title}\n")
            metafile.write(f"Language: {lang}\n")
            metafile.write(f"Subjects: {pub_subject}\n")

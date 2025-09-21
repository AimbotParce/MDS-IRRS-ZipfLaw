import configparser
import csv
import os
import sys
import tarfile
import tempfile
from time import strftime
import xml.etree.ElementTree as ET

from tqdm import tqdm

config = configparser.ConfigParser()
config.read("config.ini")

DOWNLOAD_PATH = "data/raw/catalog.tar.bz2"
OUT_FILE = "data/processed/catalog.csv"
TEMP_DIR = os.path.join(tempfile.gettempdir(), "gutenberg_catalog")


def uncompress_catalog(tar_path: str, extract_path: str):
    print(f"Uncompressing catalog from {tar_path} to {extract_path}")
    if not tarfile.is_tarfile(tar_path):
        print(f"The file {tar_path} is not a valid tar file.")
        sys.exit(1)
    with tarfile.open(tar_path, "r:bz2") as tar:
        tar.extractall(path=extract_path)
    print(f"Catalog uncompressed to {extract_path}")


def process_catalog(catalog_path: str, out_csv: str):
    print(f"Processing catalog at {catalog_path}")
    with open(out_csv, "w", encoding="utf-8") as csvfile:
        fieldnames = [
            "id",
            "title",
            "authors",
            "languages",
            "subjects",
            "type",
            "publisher",
            "issued",
            "downloads",
            "descriptions",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()

        for book_id in tqdm(
            os.listdir(os.path.join(catalog_path, "cache", "epub")),
            leave=False,
            desc="Processing books",
            unit="book",
            ncols=80,
        ):
            book_dir = os.path.join(catalog_path, "cache", "epub", book_id)
            metadata_file = os.path.join(book_dir, "pg" + book_id + ".rdf")
            if os.path.isfile(metadata_file):
                try:
                    tree = ET.parse(metadata_file)
                    root = tree.getroot()
                    # print(ET.tostring(root, encoding="unicode"))
                    for ebook in root.findall("{http://www.gutenberg.org/2009/pgterms/}ebook"):
                        book_data = {"id": int(book_id)}
                        publisher = ebook.find("{http://purl.org/dc/terms/}publisher")
                        if publisher is not None and publisher.text:
                            book_data["publisher"] = publisher.text.strip().replace("\n", " ").replace("\r", " ")
                        issued = ebook.find("{http://purl.org/dc/terms/}issued")
                        if issued is not None and issued.text:
                            book_data["issued"] = issued.text.strip().replace("\n", " ").replace("\r", " ")
                        downloads = ebook.find("{http://www.gutenberg.org/2009/pgterms/}downloads")
                        if downloads is not None and downloads.text and downloads.text.strip().isdigit():
                            book_data["downloads"] = int(downloads.text.strip())

                        author_names = []
                        for creator in ebook.findall("{http://purl.org/dc/terms/}creator"):
                            agent = creator.find("{http://www.gutenberg.org/2009/pgterms/}agent")
                            name = agent.find("{http://www.gutenberg.org/2009/pgterms/}name")
                            if name is not None and name.text:
                                author_names.append(
                                    name.text.strip().replace(";", ",").replace("\n", " ").replace("\r", " ")
                                )
                        if author_names:
                            book_data["authors"] = ";".join(author_names)

                        title = ebook.find("{http://purl.org/dc/terms/}title")
                        if title is not None and title.text:
                            book_data["title"] = title.text.strip().replace("\n", " ").replace("\r", " ")

                        descriptions = []
                        for description in ebook.findall("{http://purl.org/dc/terms/}description"):
                            if description is not None and description.text:
                                descriptions.append(
                                    description.text.strip().replace(";", ",").replace("\n", " ").replace("\r", " ")
                                )
                        if descriptions:
                            book_data["descriptions"] = ";".join(descriptions)

                        languages = []
                        for lang in ebook.findall("{http://purl.org/dc/terms/}language"):
                            lang_desc = lang.find("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description")
                            lang_value = lang_desc.find("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value")
                            if lang_value is not None and lang_value.text:
                                languages.append(
                                    lang_value.text.strip().replace(";", ",").replace("\n", " ").replace("\r", " ")
                                )
                        if languages:
                            book_data["languages"] = ";".join(languages)

                        subjects = []
                        for subject in ebook.findall("{http://purl.org/dc/terms/}subject"):
                            subj_desc = subject.find("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description")
                            for value in subj_desc.findall("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value"):
                                if value is not None and value.text:
                                    subjects.append(
                                        value.text.strip().replace(";", ",").replace("\n", " ").replace("\r", " ")
                                    )
                        if subjects:
                            book_data["subjects"] = ";".join(subjects)

                        type_ = ebook.find("{http://purl.org/dc/terms/}type")
                        type_desc = type_.find("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description")
                        type_value = type_desc.find("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value")
                        if type_value is not None and type_value.text:
                            book_data["type"] = type_value.text.strip().replace("\n", " ").replace("\r", " ")
                        writer.writerow(book_data)
                except Exception as e:
                    print(f"Failed to process {metadata_file}: {e}")
            else:
                print(f"No metadata file found for book ID {book_id}")


if __name__ == "__main__":
    print(f"Starting catalog uncompressing at {strftime('%Y-%m-%d %H:%M:%S')}")
    uncompress_catalog(DOWNLOAD_PATH, TEMP_DIR)
    process_catalog(TEMP_DIR, OUT_FILE)
    print(f"Catalog processing completed at {strftime('%Y-%m-%d %H:%M:%S')}")

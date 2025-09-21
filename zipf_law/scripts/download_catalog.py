import configparser
import os
import sys
from time import strftime
import urllib.request

config = configparser.ConfigParser()
config.read("config.ini")

URL = config.get("Download", "CatalogURL")
TEMP_DIR = "data/raw/"
DOWNLOAD_PATH = os.path.join(TEMP_DIR, "catalog.tar.bz2")


def download_catalog(url: str, download_path: str):
    os.makedirs(os.path.dirname(download_path), exist_ok=True)
    print(f"Downloading catalog from {url} to {download_path}")
    try:
        urllib.request.urlretrieve(url, download_path)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print(f"Starting catalog download at {strftime('%Y-%m-%d %H:%M:%S')}")
    download_catalog(URL, DOWNLOAD_PATH)
    print(f"Catalog downloaded to {DOWNLOAD_PATH}")

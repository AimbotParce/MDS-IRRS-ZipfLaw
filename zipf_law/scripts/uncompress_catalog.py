import configparser
import os
import sys
import tarfile
from time import strftime

config = configparser.ConfigParser()
config.read("config.ini")

TEMP_DIR = "data/raw/"
DOWNLOAD_PATH = os.path.join(TEMP_DIR, "catalog.tar.bz2")
OUT_DIR = os.path.join(TEMP_DIR, "catalog")


def uncompress_catalog(tar_path: str, extract_path: str):
    print(f"Uncompressing catalog from {tar_path} to {extract_path}")
    if not tarfile.is_tarfile(tar_path):
        print(f"The file {tar_path} is not a valid tar file.")
        sys.exit(1)
    with tarfile.open(tar_path, "r:bz2") as tar:
        tar.extractall(path=extract_path)
    print(f"Catalog uncompressed to {extract_path}")


if __name__ == "__main__":
    print(f"Starting catalog uncompressing at {strftime('%Y-%m-%d %H:%M:%S')}")
    uncompress_catalog(DOWNLOAD_PATH, OUT_DIR)
    print(f"Catalog processing completed at {strftime('%Y-%m-%d %H:%M:%S')}")

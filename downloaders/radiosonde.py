import requests
import zipfile
import os
from downloaders.commons import DATA_FOLDER
from downloaders.generic_large_file import download_large_file

def download():

    fname = "SZM00006610-drvd.txt"
    # dowload zip file from url https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/derived-por/SZM00006610-drvd.txt.zip
    url = f"https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/derived-por/{fname}.zip"

    zip_file_path = f"{DATA_FOLDER}/radiosonde.zip"

    download_large_file(url, zip_file_path)

    print("RADIOSONDE: Download complete. Unzipping...")
    # unzip the file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(f"{DATA_FOLDER}")

    # remove the zip file
    os.remove(zip_file_path)

    # move from fname to data/radiosonde.txt
    os.rename(f"{DATA_FOLDER}/{fname}", f"{DATA_FOLDER}/radiosonde.txt")

    print("RADIOSONDE: done.")
from downloaders.generic_file import download_file
from datetime import datetime


def download():

    current_year = datetime.now().year

    found = False
    for year in range(current_year, 2000, -1):
        for irel in range(9, 0, -1):
            url = f"https://sealevel.colorado.edu/files/2026_rel2/gmsl_{year}rel{irel}_seasons_rmvd.txt"
            res = download_file(url, "sea_level.txt", verbose_error=False)
            if res is not None:
                found = True
                break  # Exit the inner loop if the download is successful

        if found:
            break  # Exit the outer loop if the download is successful
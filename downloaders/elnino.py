from downloaders.generic_file import download_file


def download():
    """Download the El Nino ENSO data."""

    urls = ["https://www.cpc.ncep.noaa.gov/data/indices/sstoi.indices"]

    for url in urls:
        try:
            download_file(url, "elnino.txt")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
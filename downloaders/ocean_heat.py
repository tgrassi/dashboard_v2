from downloaders.generic_file import download_file

def download():
    """Download the ocean heat content data."""

    urls = ["https://www.ncei.noaa.gov/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/3month/ohc_levitus_climdash_seasonal.csv"]

    for url in urls:
        try:
            download_file(url, "ocean_heat.csv")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
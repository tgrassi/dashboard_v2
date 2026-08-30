from downloaders.generic_file import download_file

def download():
    """Download the NOAA CO2 data CSV file."""

    urls = ["https://sites.ecmwf.int/data/climatepulse/data/series/era5_daily_series_2t_global.csv",
            "https://sites.ecmwf.int/data/climatepulse/data/series/era5_daily_series_sst_60S-60N_ocean.csv"]

    for url in urls:
        try:
            destination_filename = url.split("/")[-1]
            download_file(url, destination_filename)
        except Exception as e:
            print(f"Failed to download {url}: {e}")
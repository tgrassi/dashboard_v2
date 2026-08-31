from downloaders.generic_file import download_file

def download():

    url = "https://noaadata.apps.nsidc.org/NOAA/G02135/north/daily/data/N_seaice_extent_daily_v4.0.csv"
    download_file(url, f"N_seaice_extent_daily_v4.0.csv")
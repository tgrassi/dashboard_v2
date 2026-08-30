#https://www.sidc.be/SILSO/DATA/SN_m_tot_V2.0.txt

from downloaders.generic_file import download_file


def download():
    """Download the NOAA CO2 data CSV file."""

    urls = ["https://www.sidc.be/SILSO/DATA/SN_m_tot_V2.0.txt"]

    for url in urls:
        try:
            download_file(url, "sunspots.txt")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
from downloaders.generic_file import download_file

def download():
    """Download the NOAA CO2 data CSV file."""

    urls = ["https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv",
            "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_daily_mlo.csv",
            "https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_mm_gl.csv",
            "https://gml.noaa.gov/webdata/ccgg/trends/n2o/n2o_mm_gl.csv",
            "https://gml.noaa.gov/webdata/ccgg/trends/sf6/sf6_mm_gl.csv"]

    for url in urls:
        try:
            destination_filename = url.split("/")[-1]
            download_file(url, destination_filename)
        except Exception as e:
            print(f"Failed to download {url}: {e}")
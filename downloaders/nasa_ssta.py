from downloaders.generic_file import download_file

def download():
    """Download the NASA GISS surface temperature anomaly CSV file."""

    url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    destination_filename = "GLB.Ts+dSST.csv"

    download_file(url, destination_filename)
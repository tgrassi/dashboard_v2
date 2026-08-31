from downloaders.generic_file import download_file

def download():
    url = "http://wgms.ch/data/faq/mb_ref.csv"

    download_file(url, "glaciers_mass.csv")
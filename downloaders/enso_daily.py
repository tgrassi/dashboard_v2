from downloaders.generic_file import download_file


def download():
    #https://climatereanalyzer.org/clim/sst_daily/json_2clim/oisst2.1_nino3.4_sst_day.json
    url = "https://climatereanalyzer.org/clim/sst_daily/json_2clim/oisst2.1_nino3.4_sst_day.json"
    download_file(url, "enso_daily.json")
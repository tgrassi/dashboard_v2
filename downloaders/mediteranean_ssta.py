import datetime
import copernicusmarine
from downloaders.commons import DATA_FOLDER

def download():

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)  # yesterday
    yesterday_iso = yesterday.strftime("%Y-%m-%dT00:00:00")

    copernicusmarine.subset(
      dataset_id="SST_MED_SSTA_L4_NRT_OBSERVATIONS_010_004_b",
      variables=["sst_anomaly"],
      minimum_longitude=-18.125,
      maximum_longitude=36.25,
      minimum_latitude=30.25,
      maximum_latitude=46.0,
      start_datetime=yesterday_iso,
      end_datetime=yesterday_iso,
    #  force_download=True,
    #  subset_method="strict",
      disable_progress_bar=True,
      output_filename = "med_ssta_map.nc",
      output_directory = DATA_FOLDER,
      username="tgrassi1",
      password="azy+<e2#dLAVaSi@WHC!",
    )
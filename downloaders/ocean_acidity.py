import os
import copernicusmarine
from downloaders.commons import DATA_FOLDER


def download():

    request_dataframe = copernicusmarine.read_dataframe(
        dataset_id="global_omi_health_carbon_ph_area_averaged",
        username="tgrassi1",
        password="azy+<e2#dLAVaSi@WHC!",
    )

    # write to file as text
    with open(os.path.join(DATA_FOLDER, "ocean_acidity.csv"), "w") as f:
        f.write(request_dataframe.to_string())

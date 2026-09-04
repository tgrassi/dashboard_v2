import os
from downloaders import (ghg_mlo,
                         nasa_ssta,
                         pulse,
                         sunspots,
                         mediteranean_ssta,
                         ocean_heat,
                         elnino,
                         seaice_north,
                         seaice_south,
                         glaciers_mass,
                         sea_level,
                         city_openmeteo,
                         ocean_acidity,
                         radiosonde
                         )
from downloaders.commons import DATA_FOLDER

# create data folder if not exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

modules = [
        radiosonde,
        ocean_acidity,
        city_openmeteo,
        glaciers_mass,
        sea_level,
        seaice_south,
        seaice_north,
        ocean_heat,
        elnino,
        mediteranean_ssta,
        nasa_ssta,
        ghg_mlo,
        pulse,
        sunspots
    ]


for module in modules:
    module.download()
    #break # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< DEBUGGING: REMOVE THIS LINE TO DOWNLOAD ALL DATASETS

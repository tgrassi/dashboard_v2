import os
from downloaders import (ghg_mlo,
                         nasa_ssta,
                         pulse,
                         sunspots,
                         mediteranean_ssta,
                         ocean_heat,
                         elnino
                         )
from downloaders.commons import DATA_FOLDER

# create data folder if not exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

modules = [
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

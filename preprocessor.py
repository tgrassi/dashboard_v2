import os
from preprocessors import global_temperature, era5_daily, era5_ocean, ocean_heat

# create website data folder if not exists
if not os.path.exists('website/data'):
    os.makedirs('website/data')

preproc = [global_temperature,
           era5_daily,
           era5_ocean,
           ocean_heat
        ]

for p in preproc:
    print(f"Preprocessing {p.__name__}...")
    p.preprocess()
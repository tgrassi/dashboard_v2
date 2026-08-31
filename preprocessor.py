import os
from preprocessors import (co2_mlo,
                           global_temperature,
                           era5_daily,
                           era5_ocean,
                           med_ssta_map,
                           ocean_heat,
                           ch4_gl,
                           n2o_gl,
                           sf6_gl,
                           enso
                           )

# create website data folder if not exists
if not os.path.exists('website/data'):
    os.makedirs('website/data')

preproc = [
            enso,
            sf6_gl,
            n2o_gl,
            ch4_gl,
            co2_mlo,
            med_ssta_map,
            global_temperature,
            era5_daily,
            era5_ocean,
            ocean_heat
        ]

for p in preproc:
    print(f"Preprocessing {p.__name__}...")
    p.preprocess()
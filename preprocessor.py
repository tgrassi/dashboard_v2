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
                           enso,
                           era5_daily_anomaly,
                           era5_ocean_anomaly,
                           seaice_north,
                           seaice_south,
                           glaciers_mass,
                           sea_level,
                           city_tmax_days,
                           city_tmin_days,
                           city_heat,
                           city_gauss_max,
                           co2_800kyr,
                           temperature_2kyrs,
                           stripes_factory,
                           )

# create website data folder if not exists
if not os.path.exists('website/data'):
    os.makedirs('website/data')

preproc = [
            temperature_2kyrs,
            co2_800kyr,
            city_gauss_max,
            city_heat,
            city_tmin_days,
            city_tmax_days,
            sea_level,
            glaciers_mass,
            seaice_south,
            seaice_north,
            era5_ocean_anomaly,
            era5_daily_anomaly,
            enso,
            sf6_gl,
            n2o_gl,
            ch4_gl,
            co2_mlo,
            med_ssta_map,
            global_temperature,
            era5_daily,
            era5_ocean,
            ocean_heat,
            stripes_factory # IMPORTANT: this must be the last one because it reads all the json files created by the other preprocessors
        ]

for p in preproc:
    print(f"Preprocessing {p.__name__}...")
    p.preprocess()
import os
from preprocessors import (ghg_ch4, ghg_co2_mlo, ghg_n2o, ghg_sf6,
                           global_temperature,
                           era5_daily,
                           era5_ocean,
                           med_ssta_map,
                           med_gaussian,
                           ocean_heat,
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
                           rank_months,
                           correlation_temp_co2,
                           correlation_temp_sunspots,
                           city_summer,
                           stripes_factory,
                           overview_factory
                           )

# create website data folder if not exists
if not os.path.exists('website/data'):
    os.makedirs('website/data')

# create data_stripes folder if not exists
if not os.path.exists('data_stripes'):
    os.makedirs('data_stripes')

# remove all files in data_stripes folder
for filename in os.listdir('data_stripes'):
    os.remove(os.path.join('data_stripes', filename))

# create data_overview folder if not exists
if not os.path.exists('data_overview'):
    os.makedirs('data_overview')

# remove all files in data_overview folder
for filename in os.listdir('data_overview'):
    os.remove(os.path.join('data_overview', filename))

preproc = [
            city_summer,
            correlation_temp_sunspots,
            correlation_temp_co2,
            rank_months,
            med_gaussian,
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
            ghg_sf6,
            ghg_n2o,
            ghg_ch4,
            ghg_co2_mlo,
            med_ssta_map,
            global_temperature,
            era5_daily,
            era5_ocean,
            ocean_heat,
            stripes_factory, # IMPORTANT: this must be the last one because it reads all the json files created by the other preprocessors
            overview_factory # IMPORTANT: same as above
        ]

for p in preproc:
    print(f"Preprocessing {p.__name__}...")
    p.preprocess()
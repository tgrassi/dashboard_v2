import xarray as xr
import pandas as pd
import numpy as np
import json
#import geopandas as gpd

def preprocess():

    # open era5_monthly_map.nc
    ds = xr.open_dataset("data/era5_monthly_map.nc")

    dates = ds["valid_time"].values

    years = np.array([pd.to_datetime(d).year for d in dates])  # years
    months = np.array([pd.to_datetime(d).month for d in dates])  # months
    years_season = [y if m != 12 else y + 1 for y, m in zip(years, months)] # years assuming that December belongs to the next year for seasonal analysis

    # get season (DJF, MAM, JJA, SON) for each month
    def get_season(month):
        seasons_dict = {
            "DJF": [12, 1, 2],
            "MAM": [3, 4, 5],
            "JJA": [6, 7, 8],
            "SON": [9, 10, 11]
        }

        for season, months in seasons_dict.items():
            if month in months:
                return season
        return None

    # get seasons for each month and year
    seasons = np.array([get_season(m) for m in months])

    # get lats, lons, and temperature
    lats = ds["latitude"].values
    lons = ds["longitude"].values
    temp = ds["t2m"].values - 273.15  # convert from K to C

    # get last month, year, and season
    last_month = months[-1]
    last_year = years[-1]
    last_season = seasons[-1]

    last_season_text = {
        "DJF": "Inverno",
        "MAM": "Primavera",
        "JJA": "Estate",
        "SON": "Autunno"
    }[last_season]

    temp_mean = []
    for y in sorted(np.unique(years_season)):
        temp_mean.append(np.mean(temp[(years_season == y) & (seasons == last_season), :, :], axis=0))

    temp_mean_last = np.mean(temp[(years_season == last_year) & (seasons == last_season), :, :], axis=0)

    temp_rank = np.sort(temp_mean, axis=0)

    rank = len(np.unique(years_season)) - np.argmin(np.abs(temp_rank - temp_mean_last), axis=0)

    rank_min = int(np.min(rank))

    rank = rank.astype(float) - 0.5

    lons = [float(x) for x in lons]
    lats = [float(x) for x in lats]
    rank = [[float(y) for y in x] for x in rank]


    # save to json
    data = [{
             "x": lons,
             "y": lats,
             "z": rank,
             "type": "contour",
             "colorscale": "RdBu",
             "reversescale": True,
             "colorbar":{
                "tickvals": [i - 0.5 for i in range(rank_min, rank_min + 6)],
                "ticktext": [str(i) for i in range(rank_min, rank_min + 6)]
             },
               "contours": {
                "start": rank_min,
                "end": rank_min + 4,
                "size": 1
            }
             }]

    layout = {
          "width": 600,
          "height": 600,
        "title": {"text": f"{last_season_text.title()} {last_year}: come si piazza in classifica negli ultimi {len(np.unique(years_season))} anni?"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/era5_seasonal_rank.json", "w") as f:
        json.dump(bundle, f, indent=4)

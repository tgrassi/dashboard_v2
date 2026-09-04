
from glob import glob
import pandas as pd
import numpy as np
import json
from preprocessors.commons import PLOTLY_COLOR_SEQUENCE, MONTHS_NAME

def preprocess():
    cities = sorted([city.split('_')[-1].replace('.csv', '') for city in glob("data/city_openmeteo_*.csv")])

    first_city = cities[0]

    year_avg_min = 1980
    year_avg_max = year_avg_min + 31

    data = []
    for i, city in enumerate(cities):
        print(f"STRIPES: Preprocessing {city}...")

        # date,temperature_2m_max,temperature_2m_min
        df = pd.read_csv(f"data/city_openmeteo_{city.lower()}.csv")

        # take first 10 characters of date column to get YYYY-MM-DD format
        df['date'] = df['date'].str[:10]

        # convert date to datetime
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

        years = df['date'].dt.year.unique().tolist()
        month_average = {i: [] for i in range(1, 13)}
        for year in years:
            if year < year_avg_min or year > year_avg_max:
                continue
            for month in range(1, 13):
                tmax = df[(df['date'].dt.year == year) & (df['date'].dt.month == month)]['temperature_2m_max'].tolist()
                month_average[month].extend(tmax)

        month_average = {month: np.mean(tmax) for month, tmax in month_average.items() if len(tmax) > 0}


        anomaly = []
        for year in years:
            tot = 0e0
            for month in range(1, 13):
                tmax = df[(df['date'].dt.year == year) & (df['date'].dt.month == month)]['temperature_2m_max'].tolist()
                if len(tmax) == 0:
                    continue
                tot += np.nanmean(tmax - month_average[month])
            anomaly.append(tot / 12.)


        xx = [int(x) for x in years]
        zz = [float(x) for x in anomaly]

        val = np.abs(zz).max()

        # save to json
        data = [{
                "x": xx,
                "y": [0, 1],
                "z": [zz, zz],
                "type": "heatmap",
                "colorscale": "RdBu",
                "reversescale": zz,
                "zmin": -val,
                "zmax": val
                }]

        layout = {
                    "xaxis": {"tickformat": "%Y"},
                    "yaxis": {"visible": False},
                    "title": {"text": f"{city.title()}: Anomalia temperatura massima mensile rispetto alla media {year_avg_min}-{year_avg_max}"}
                }

        # first layout so it is easier to debug in the json file
        bundle = {"layout": layout, "data": data}

        city_encoded = city.replace(" ", "_").lower()
        with open(f"website/data/stripes_city_{city_encoded}.json", "w") as f:
            json.dump(bundle, f, indent=4)
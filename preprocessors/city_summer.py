import numpy as np
import pandas as pd
import json
from glob import glob
from statsmodels.nonparametric.smoothers_lowess import lowess

def preprocess():

    cities = sorted([city.split('_')[-1].replace('.csv', '') for city in glob("data/city_openmeteo_*.csv")])

    first_city = cities[0]

    data = []
    for city in cities:
        # date,temperature_2m_max,temperature_2m_min
        df = pd.read_csv(f"data/city_openmeteo_{city.lower()}.csv")

        # take first 10 characters of date column to get YYYY-MM-DD format
        df['date'] = df['date'].str[:10]

        df["year"] = df['date'].str[:4].astype(int)
        df["month"] = df['date'].str[5:7].astype(int)

        #print(df["year"])
        #print(df["month"].max())

        month_min = 6
        month_max = 8

        years = df["year"].unique()

        average_tmax = []
        for year in years:
            tmax_list = df['temperature_2m_max'][(df['year'] == year) & (df['month'] >= month_min) & (df['month'] <= month_max)]
            average_tmax.append(float(tmax_list.mean()))

        if city == first_city:
            visible = "true"
        else:
            visible = "legendonly"

        val = np.abs(average_tmax).max()

        # save to json
        data.append({
                "x": years.tolist(),
                "y": average_tmax,
                "type": "scatter",
                "mode": "lines+markers",
                "name": city.title(),
                "visible": visible,
            #     "marker": {
            #      "color": average_tmax,
            #      "colorscale": "Reds",
            #      "cmin": -val,
            #      "cmax": val
            #    }
                })


    layout = {
                "xaxis": {},
                "yaxis": {"title": {"text": "Temperatura massima media (°C)"}},
                "title": {"text": "Media delle temperature massime giornaliere estive (giugno-agosto) per città"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/city_summer.json", "w") as f:
        json.dump(bundle, f, indent=4)
import numpy as np
import pandas as pd
import json
from glob import glob
from statsmodels.nonparametric.smoothers_lowess import lowess

def preprocess():

    cities = sorted([city.split('_')[-1].replace('.csv', '') for city in glob("data/city_openmeteo_*.csv")])

    first_city = cities[0]

    year_avg_min = 1980
    year_avg_max = year_avg_min + 31

    data = []
    for city in cities:
        # date,temperature_2m_max,temperature_2m_min
        df = pd.read_csv(f"data/city_openmeteo_{city.lower()}.csv")

        # take first 10 characters of date column to get YYYY-MM-DD format
        df['date'] = df['date'].str[:10]

        # convert date to datetime
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

        last_year = df['date'].dt.year.max()

        avg = []
        for year in range(year_avg_min, year_avg_max + 1):
            tmax = df[df['date'].dt.year == year]['temperature_2m_max'].tolist()[:365]
            avg.append(tmax)
        # apply lowess smoothing
        avg = np.array(avg).mean(axis=0)
        doy = np.arange(1, len(avg) + 1)

        lowess_smoothed = lowess(avg, doy, return_sorted=False, frac=1/30.)

        current_tmax = df[df['date'].dt.year == last_year]['temperature_2m_max'].tolist()[:365]

        ndays = len(current_tmax)

        current_anomaly = current_tmax - lowess_smoothed[:ndays]
        current_anomaly = [float(x) for x in current_anomaly]

        # days of the year to datetime
        dates = pd.date_range(start=f"{last_year}-01-01", periods=ndays).to_pydatetime().tolist()
        dates = [str(x) for x in dates]

        if city == first_city:
            visible = "true"
        else:
            visible = "legendonly"


        val = np.abs(current_anomaly).max()

        # save to json
        data.append({
                "x": dates,
                "y": current_anomaly,
                "type": "bar",
                "name": city.title(),
                "visible": visible,
                "marker": {
                 "color": current_anomaly,
                 "colorscale": "RdBu",
                 "cmin": -val,
                 "cmax": val
               }
                })


    layout = {
                "xaxis": {"tickformat": "%d %b"},
                "yaxis": {"title": {"text": "Differenza di temperatura (°C)"}},
                "title": {"text": f"Anomalia temperautura massima giornaliera rispetto alla media {year_avg_min}-{year_avg_max}"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/city_heat.json", "w") as f:
        json.dump(bundle, f, indent=4)
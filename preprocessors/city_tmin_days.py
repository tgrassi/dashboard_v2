import pandas as pd
import json
from glob import glob

def preprocess():

    cities = sorted([city.split('_')[-1].replace('.csv', '') for city in glob("data/city_openmeteo_*.csv")])

    first_city = cities[0]

    data = []
    for city in cities:
        # date,temperature_2m_max,temperature_2m_min
        df = pd.read_csv(f"data/city_openmeteo_{city.lower()}.csv")

        # take first 10 characters of date column to get YYYY-MM-DD format
        df['date'] = df['date'].str[:10]

        # convert date to datetime
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

        years = df['date'].dt.year.unique().astype(str).tolist()

        tmin_threshold = 20.
        tmin_days = []
        for year in years:
            count_tmin = df[df['date'].dt.year == int(year)]['temperature_2m_min'].gt(tmin_threshold).sum()
            tmin_days.append(int(count_tmin))

        if city == first_city:
            visible = "true"
        else:
            visible = "legendonly"

        # save to json
        data.append({
                "x": years,
                "y": tmin_days,
                "type": "bar",
                "name": city.title(),
                "visible": visible,
                })

        # compute moving average of tmin_days
        window_size = 10
        tmin_days_ma = pd.Series(tmin_days).rolling(window=window_size, min_periods=1).mean().tolist()



        # save to json
        data.append({
                "x": years,
                "y": tmin_days_ma,
                "type": "line",
                "name": f"{city.title()} ({window_size} anni)",
                "visible": visible,
                })



    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Numero di giorni"}},
                "title": {"text": f"Giorni con temperatura minima > {tmin_threshold}°C"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/city_tmin_days.json", "w") as f:
        json.dump(bundle, f, indent=4)

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
        # date,temperature_2m_max,temperature_2m_min
        df = pd.read_csv(f"data/city_openmeteo_{city.lower()}.csv")

        # take first 10 characters of date column to get YYYY-MM-DD format
        df['date'] = df['date'].str[:10]

        # convert date to datetime
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

        last_day = df['date'].max()

        last_tmax = df[df['date'] == last_day]['temperature_2m_max'].values[0]

        this_month = last_day.month

        # get all the days with the given month within year_avg_min and year_avg_max
        avg = []
        for year in range(year_avg_min, year_avg_max + 1):
            tmax = df[(df['date'].dt.year == year) & (df['date'].dt.month == this_month)]['temperature_2m_max'].tolist()
            avg.extend(tmax)

        avg = np.array(avg)

        mean = avg.mean()
        std = avg.std()

        xx = np.linspace(avg.min(), avg.max(), 100)
        yy = np.exp(-0.5 * ((xx - mean)/std)**2) / (std * np.sqrt(2 * np.pi))

        xx = [float(x) for x in xx]
        yy = [float(x) for x in yy]

        if city == first_city:
            visible = "true"
        else:
            visible = "legendonly"

        data.append({
                "x": xx,
                "y": yy,
                "type": "line",
                "name": city.title(),
                "line": {
                    "color": PLOTLY_COLOR_SEQUENCE[i % len(PLOTLY_COLOR_SEQUENCE)],
                },
                "visible": visible,
                })


        last_date_text = last_day.strftime("%d/%m/%Y")
        data.append({
                "x": [last_tmax, last_tmax],
                "y": [0, max(yy)],
                "type": "line",
                "name": f"{last_date_text} {city.title()}",
                "line": {
                    "color": PLOTLY_COLOR_SEQUENCE[i % len(PLOTLY_COLOR_SEQUENCE)],
                },
                "visible": visible,
                })

    month_name = MONTHS_NAME[int(this_month) - 1]
    layout = {
                "xaxis": {"tickformat": "%d %b", "title": {"text": "Temperatura massima giornaliera (°C)"}},
                "yaxis": {"title": {"text": "Probabilità"}},
                "title": {"text": f"Probabilità di temperatura massima giornaliera ({month_name}, media {year_avg_min}-{year_avg_max})"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/city_gauss_max.json", "w") as f:
        json.dump(bundle, f, indent=4)
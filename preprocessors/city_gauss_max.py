
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

        xmin = min(avg.min(), last_tmax) - 1
        xmax = max(avg.max(), last_tmax) + 1

        def gaussian(x, mean, std):
            return np.exp(-0.5 * ((x - mean)/std)**2) / (std * np.sqrt(2 * np.pi))

        xx = np.linspace(xmin, xmax, 100)
        yy = gaussian(xx, mean, std)

        ymax = max(yy)

        xx = [float(x) for x in xx]
        yy = [float(x) for x in yy]

        if city == first_city:
            visible = "true"
        else:
            visible = "legendonly"

        # this is the gaussian
        data.append({
                "x": xx,
                "y": yy,
                "type": "line",
                "name": city.title(),
                "line": {
                    "color": PLOTLY_COLOR_SEQUENCE[i % len(PLOTLY_COLOR_SEQUENCE)],
                },
                "visible": visible,
                "legendgroup": f"city_{city}",
                })


        percentiles = [np.percentile(avg, p) for p in [1, 5, 25, 75, 95, 99]]
        percentiles = [xmin] + percentiles + [xmax]

        purple = "#800080"
        red = "#a33f3f"
        orange = "#b96c1f"
        green = "#249124"
        colors = [purple, red, orange, green, orange, red, purple]

        for j in range(1, len(percentiles)):

            xpmin = percentiles[j - 1]
            xpmax = percentiles[j]

            xx = np.linspace(xpmin, xpmax, 100)
            yy = gaussian(xx, mean, std)

            xx = [float(x) for x in xx]
            yy = [float(x) for x in yy]

            data.append({
                "x": xx,
                "y": yy,
                "fill": 'tozeroy',
                "type": "line",
                "mode": "lines",
                "line": {
                    "color": colors[j - 1],
                    "dash": "dot",
                    "width": 0,
                    "opacity": 0.1,
                },
                "visible": visible,
                "legendgroup": f"city_{city}",
                "showlegend": False,
                })


        # this is the vertical line
        last_date_text = last_day.strftime("%d/%m/%Y")
        data.append({
                "x": [last_tmax, last_tmax],
                "y": [0, ymax],
                "type": "line",
                "mode": "lines",
                "name": f"{last_date_text} {city.title()}",
                "line": {
                    "color": "white",
                    "dash": "dash",
                    "width": 4,
                },
                "visible": visible,
                "legendgroup": f"city_{city}",
                "showlegend": False,
                })

    month_name = MONTHS_NAME[int(this_month) - 1]
    layout = {
                "xaxis": {"tickformat": "%d %b", "title": {"text": "Temperatura massima giornaliera (°C)"}},
                "yaxis": {"title": {"text": "Probabilità"}},
                "title": {"text": f"Quanto è probabile la temperatura massima di oggi per {month_name}?"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/city_gauss_max.json", "w") as f:
        json.dump(bundle, f, indent=4)
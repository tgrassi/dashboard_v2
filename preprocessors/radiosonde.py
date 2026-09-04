import json

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def preprocess():

    fname = "data/radiosonde.txt"

    yearmin = 1981
    yearmax = yearmin + 30

    rows = [x for x in open(fname, "r")]

    dates = []
    freezing_heights = []

    months = {i: [] for i in range(1, 13)}
    current_year = 2025 # np.datetime64("today").astype(object).year

    for row in tqdm(rows):
        srow = row.strip()
        if srow == "":
            continue
        if srow.startswith("#"):
            date = srow[13:23].replace(" ", "-")
            year = int(srow[13:17])
            month = int(srow[17:20])
            hour = int(srow[24:27])
            npoints = int(srow[31:36])
            height = []
            temperature = []
            continue

        if hour != 12:
            continue

        arow = srow.split()
        height.append(float(arow[2]))
        temperature.append(float(arow[3]) / 10.0 - 273.15)  # convert to Celsius

        if len(height) == npoints:
            imin = None
            for i in range(npoints - 2, -1, -1):
                if temperature[i] * temperature[i + 1] < 0.0:
                    imin = i
                    break
            if imin is None:
                #print(f"{date} No inversion found")
                continue
            h0 = height[imin]
            h1 = height[imin + 1]
            t0 = temperature[imin]
            t1 = temperature[imin + 1]
            h0 = h0 + (0.0 - t0) * (h1 - h0) / (t1 - t0)
            if year == current_year:
                dates.append(date)
                freezing_heights.append(h0)
            if yearmin <= year <= yearmax:
                months[month].append(h0)


    average = {k: np.mean(v) for k, v in months.items() if len(v) > 0}

    dates = [np.datetime64(x) for x in dates]

    anomalies = []
    for date, height in zip(dates, freezing_heights):
        month = date.astype(object).month
        avg = average[month]
        anomalies.append(height - avg)

    dates = [str(x) for x in dates]
    anomalies = [float(x) for x in anomalies]

    val = np.abs(anomalies).max()

    # save to json
    data = [{
             "x": dates,
             "y": anomalies,
             "type": "bar",
             "marker": {
                 "color": anomalies,
                 "colorscale": "RdBu",
                 "cmin": -val,
                 "cmax": val
               }
             }]

    layout = {
                "xaxis": {"tickformat": "%d %b %Y",
                          "angle": 90,
                          "range": [str(np.datetime64(f"{current_year}-01-01")), str(np.datetime64(f"{current_year}-12-31"))]},
                "yaxis": {"title": {"text": "Anomalia quota (m)"}},
                "title": {"text": "Quale la differenza tra quota di congelamento e media mensile?"}
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}


    with open("website/data/radiosonde.json", "w") as f:
        json.dump(bundle, f, indent=4)
import json
import numpy as np
import datetime

def preprocess():

    fname = "data/ocean_heat.csv"
    dates = []
    heat = []
    for line in open(fname):
        if line.startswith("#"):
            continue
        date, h = line.strip().split(",")
        year, month = date.split("-")
        dates.append(datetime.datetime(int(year), int(month), 1).strftime("%Y-%m-%d"))

        dates.append(date)
        heat.append(float(h))

    val = np.abs(heat).max()

    # save to json
    data = [{
             "x": dates,
             "y": heat,
             "type": "scatter",
             "mode": "lines+markers",
             "marker": {
                 "color": heat,
                 "colorscale": "RdBu",
                 "cmin": -val,
                 "cmax": val,
                 "size": 6
               }
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Calore oceani (10<sup>22</sup> Joules)"}},
                "title": {"text": "Calore oceani (0-700m)"}
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/ocean_heat.json", "w") as f:
        json.dump(bundle, f, indent=4)
import json
import numpy as np
import datetime

from preprocessors.overview_factory import save_overview
from preprocessors.stripes_factory import save_stripes
from preprocessors.commons import MONTHS_NAME

def preprocess():

    fname = "data/ocean_heat.csv"
    dates = []
    heat = []
    for line in open(fname):
        if line.startswith("#"):
            continue
        date, h = line.strip().split(",")
        year, month = date.split("-")
        last_year = int(year)
        last_month = int(month)
        dates.append(datetime.datetime(int(year), int(month), 1).strftime("%Y-%m-%d"))
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

    # save stripes json for the stripes factory
    save_stripes(dates, heat, "Calore oceani (10<sup>22</sup> Joules)", "ocean_heat.json", symmetric_minmax=True)

    # save overview data for overview factory
    month_name = MONTHS_NAME[last_month-1]
    save_overview("ocean_heat", f"Calore Oceani ({month_name} {last_year})", f"{heat[-1]:+.1f}", dates[-1])
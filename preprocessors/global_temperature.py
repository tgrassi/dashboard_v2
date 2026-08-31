# load GLB.Ts+dSST.csv
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

def preprocess():
    """Preprocess the global temperature data."""
    df = pd.read_csv("data/GLB.Ts+dSST.csv", skiprows=1)
    # Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON
    df = df.rename(columns={"Year": "year", "J-D": "annual_mean"})

    # unique years
    years = df["year"].unique()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    dates = []
    temperatures = []
    for year in years:
        # loop on months columns
        for i, month in enumerate(months):
            # get the value for the month
            value = df.loc[df["year"] == year, month].values[0]
            if value != "***":
                # create a date string
                date = f"{year}-{i+1:02d}-01"
                dates.append(date)
                temperatures.append(float(value))

    val = np.abs(temperatures).max()

    # save to json
    data = [{
             "x": dates,
             "y": temperatures,
             "type": "bar",
             "marker": {
                 "color": temperatures,
                 "colorscale": "RdBu",
                 "cmin": -val,
                 "cmax": val
               }
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Anomalia temperatura (°C)"}},
                "title": {"text": "Anomalia temperatura globale (media 1951-1980)"}
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/global_temperature.json", "w") as f:
        json.dump(bundle, f, indent=4)

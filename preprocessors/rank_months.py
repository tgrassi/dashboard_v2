import pandas as pd
import numpy as np
import json

from preprocessors.commons import MONTHS_NAME_SHORT

def preprocess():
    """Preprocess the global temperature data."""
    df = pd.read_csv("data/GLB.Ts+dSST.csv", skiprows=1)
    # Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON
    df = df.rename(columns={"Year": "year", "J-D": "annual_mean"})

    # unique years
    years = df["year"].unique()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    temperature_dict = {x: [] for x in months}

    temperatures = []
    for year in years:
        # loop on months columns
        for i, month in enumerate(months):
            # get the value for the month
            value = df.loc[df["year"] == year, month].values[0]
            if value != "***":
                temperature_dict[month].append(float(value))
            else:
                temperature_dict[month].append(-9999.0)


    sort_dict = {}
    for k, v in temperature_dict.items():
        av = np.argsort(v)
        rank = np.zeros(len(v))
        for i, idx in enumerate(av):
            rank[idx] = len(v) - i
        sort_dict[k] = rank.copy()


    sort_dict = {k: [int(x) for x in v[-25:]] for k, v in sort_dict.items()}

    xgrid = [int(x) for x in years[-25:]]
    ygrid = [MONTHS_NAME_SHORT[i] for i in range(12)]
    zgrid = [sort_dict[month] for month in months]

    annotations = []
    for i in range(len(zgrid)):
        for j in range(len(zgrid[i])):
            if zgrid[i][j] == len(years):
                text = "?"
            else:
                text = str(zgrid[i][j])
            annotations.append(
                {
                    "x": xgrid[j],
                    "y": ygrid[i],
                    "text": text,
                    "xref": "x1",
                    "yref": "y1",
                    "showarrow": False,
                    "font": {"color": "white" if zgrid[i][j] > 15 else "black"},
                }
            )

    data = [{
             "x": xgrid,
             "y": ygrid,
             "z": zgrid,
             "type": "heatmap",
             "colorscale": "RdBu",
             "reversescale": True,
             "showscale": False,
             "zmin": 1,
             "zmax": 30,}]

    layout = {
        "title": {"text": f"Quali sono stati i mesi più caldi a livello globale ({min(years)}-{max(years)})?"},
        "xaxis": {"dtick": 1, "tickangle": 90},
        "annotations": annotations,
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/rank_months.json", "w") as f:
        json.dump(bundle, f, indent=4)

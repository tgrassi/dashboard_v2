import pandas as pd
import json
import numpy as np
from preprocessors.stripes_factory import save_stripes

def preprocess():

    # Year	Cowtan & Way instrumental target	Full ensemble median	Full ensemble 2.5th percentile	Full ensemble 97.5th percentile	Cowtan & Way instrumental target 31-year filtered	31-year filtered full ensemble median	31-year filtered full ensemble 2.5th percentile	31-year filtered full ensemble 97.5th percentile
    df = pd.read_csv("data_fix/page2k.txt", comment="#", delimiter="\t")

    # drop nans
    df = df.dropna(subset=['Full ensemble median'])

    dates = df['Year'].astype(str).tolist()
    temperatures = df['Full ensemble median'].tolist()

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
                "xaxis": {},
                "yaxis": {"title": {"text": "Temperatura (°C)"}},
                "title": {"text": "Temperatura ultimi 2000 anni"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/temperature_2kyrs.json", "w") as f:
        json.dump(bundle, f, indent=4)

    # save stripes json for the stripes factory
    save_stripes(dates, temperatures, "Temperatura ultimi 2000 anni", "temperature_2kyrs.json", cmap="RdBu", symmetric_minmax=True)
import pandas as pd
import json
from preprocessors.overview_factory import save_overview
from preprocessors.stripes_factory import save_stripes

def preprocess():
    df = pd.read_csv("data/ocean_acidity.csv", sep="\s+", skiprows=2, header=None, names=["time", "ph", "ph_uncertainty"])

    # first 4 character is year
    df["time"] = df["time"].astype(str).str[:4].astype(int)

    years = [int(x) for x in df["time"]]
    ph = [float(x) for x in df["ph"]]

    # save to json
    data = [{
             "x": years,
             "y": ph,
             "type": "scatter",
             "mode": "lines+markers",
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "pH"}, "tickformat": ".3f", "autorange": "reversed"},
                "title": {"text": "Quanto è cambiata l'acidità degli oceani?"}
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/ocean_acidity.json", "w") as f:
        json.dump(bundle, f, indent=4)

    # save stripes json for the stripes factory
    save_stripes(years, ph, "pH", "ocean_acidity.json", symmetric_minmax=False, cmap="YlGnBu")

    # save overview data for overview factory
    save_overview("ocean_acidity", f"Acidità Oceani (pH, {years[-1]})", f"{ph[-1]:.3f}", years[-1])
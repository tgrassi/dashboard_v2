import json
import numpy as np
from glob import glob

def preprocess():

    for g in glob("data_stripes/*.json"):

        print(f"STRIPES: Preprocessing {g}...")

        fname_base = g.split("/")[-1].split(".")[0]
        with open(g, "r") as f:
            data = json.load(f)

        title = data["title"]
        xdata = data["x"]
        ydata = data["y"]
        cmap = data["cmap"]
        symmetric_minmax = data["symmetric_minmax"]

        if symmetric_minmax:
            val = np.abs(ydata).max()
            cmin = -val
            cmax = val
        else:
            cmin = float(np.min(ydata))
            cmax = float(np.max(ydata))

        z = [ydata, ydata]

        # save to json
        data = [{
                "x": xdata,
                "y": [0, 1],
                "z": z,
                "type": "heatmap",
                "colorscale": cmap,
                "zmin": cmin,
                "zmax": cmax
                }]

        layout = {
                    "xaxis": {"tickformat": "%Y"},
                    "yaxis": {"visible": False},
                    "title": {"text": title}
                }

        # first layout so it is easier to debug in the json file
        bundle = {"layout": layout, "data": data}

        with open(f"website/data/stripes_{fname_base}.json", "w") as f:
            json.dump(bundle, f, indent=4)


def save_stripes(xdata, ydata, title, filename, cmap="RdBu", symmetric_minmax=False):

    if filename.endswith(".json"):
        filename = filename[:-5]

    data = {
            "title": title,
            "x": xdata,
            "y": ydata,
            "symmetric_minmax": symmetric_minmax,
            "cmap": cmap
            }

    with open(f"data_stripes/{filename}.json", "w") as f:
        json.dump(data, f, indent=4)
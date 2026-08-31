import xarray as xr
import numpy as np
import json

def preprocess():

    # load nc
    filename = "data/med_ssta_map.nc"

    # load the data
    ds = xr.open_dataset(filename)

    lats = [str(x) for x in list(ds.latitude.values)]
    lons = [str(x) for x in list(ds.longitude.values)]
    sst_anomaly = ds.sst_anomaly.values.squeeze()

    ssta = [[str(y) for y in x] for x in sst_anomaly]

    sst_nan = sst_anomaly[~np.isnan(sst_anomaly)]
    val = np.abs(sst_nan).max()

    # save to json
    data = [{
             "x": lons,
             "y": lats,
             "z": ssta,
             "type": "heatmap",
             "colorscale": "RdBu",
             "zmin": -val,
             "zmax": val
             }]

    layout = {
        "title": {"text": "Anomalia della temperatura superficiale del mare nel Mediterraneo"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/med_ssta_map.json", "w") as f:
        json.dump(bundle, f, indent=4)
from preprocessors.overview_factory import save_overview
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

    hist, bin_edges = np.histogram(sst_nan, bins=30, density=True)

    bins = (bin_edges[:-1] + bin_edges[1:]) / 2

    mean = np.nanmean(sst_anomaly)
    std = np.nanstd(sst_anomaly)

    def gaussian(x, mu, sigma):
        return 1e0 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sigma)**2)

    xx = np.linspace(-val, val, 100)
    yy = gaussian(xx, mean, std)

    hist = [float(x) for x in hist]
    bins = [float(x) for x in bins]

    xx = [float(x) for x in xx]
    yy = [float(x) for x in yy]

    # save to json
    data = [{
             "x": bins,
             "y": hist,
             "type": "bar",
             "name": "Distribuzione",
             },
            {
                "x": xx,
                "y": yy,
                "type": "scatter",
                "mode": "lines",
                "name": "Fit gaussiano",
                "line": {"color": "#17becf"}
             },
             {
                 "x": [mean, mean],
                 "y": [0, max(yy)],
                 "type": "scatter",
                 "mode": "lines",
                 "name": f"Media: {mean:+.1f}°C",
                 "line": {
                     "color": "#ff7f0e",
                     "width": 2
                 },
             }
    ]

    layout = {
        "title": {"text": "Qual è la distribuzione dell'anomalia termica superficiale del Mediterraneo?"},
        "xaxis": {"title": {"text": "Anomalia della temperatura superficiale (°C)"}},
        "yaxis": {"title": {"text": "Densità di probabilità"}},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/med_gaussian.json", "w") as f:
        json.dump(bundle, f, indent=4)

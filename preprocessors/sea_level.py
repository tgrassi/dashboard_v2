import numpy as np
import json

from preprocessors.overview_factory import save_overview
from preprocessors.stripes_factory import save_stripes
from preprocessors.commons import MONTHS_NAME


def preprocess():


    dates, sea_level = np.loadtxt("data/sea_level.txt", comments="#").T

    years = [int(x) for x in dates]
    months = [int((x - int(x)) * 12) + 1 for x in dates]

    dates = [f"{y}-{m:02d}-01" for y, m in zip(years, months)]
    sea_level = [float(x) for x in sea_level]

    # save to json
    data = [{
             "x": dates,
             "y": sea_level,
             "type": "scatter",
             "mode": "lines",
             "color": "#1f77b4",
             },

            {
                "x": [dates[-1]],
                "y": [sea_level[-1]],
                "type": "scatter",
                "mode": "markers",
                "marker": {
                    "color": "#1f77b4",
                    "size": 10
                }
            }

             ]

    layout = {
                "xaxis": {
                    "tickformatstops": [
                    {
                    "dtickrange": ["null", 'M1'],
                    "value": '%d %b %Y'
                    },
                    {
                    "dtickrange": ['M1', 'M12'],
                    "value": '%b %Y'
                    },
                    {
                    "dtickrange": ['M12', "null"],
                    "value": '%Y'
                    }]
                },
                "yaxis": {"title": {"text": "Livello degli oceani (mm)"}},
                "title": {"text": "Di quanto si è alzato il livello degli oceani?"},
                "showlegend": False,
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/sea_level.json", "w") as f:
        json.dump(bundle, f, indent=4)

    # save stripes json for the stripes factory
    save_stripes(dates, sea_level, "Livello oceani (mm)", "sea_level.json", symmetric_minmax=False)

    # save overview data for overview factory
    year = int(dates[-1][:4])
    month = int(dates[-1][5:7])
    month_name = MONTHS_NAME[month - 1]
    date_mmyyyy = f"{month_name} {year}"
    save_overview("sea_level", f"Livello oceani (mm, {date_mmyyyy})", f"{sea_level[-1]:+.1f}", dates[-1])
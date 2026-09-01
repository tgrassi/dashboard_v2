import numpy as np
import json

from preprocessors.overview_factory import save_overview
from preprocessors.stripes_factory import save_stripes
from preprocessors.commons import MONTHS_NAME

def preprocess():


    dates, sea_level = np.loadtxt("data/sea_level.txt", comments="#").T

    dates = [float(x) for x in dates]
    sea_level = [float(x) for x in sea_level]

    # save to json
    data = [{
             "x": dates,
             "y": sea_level,
             "type": "scatter",
             "mode": "lines",
             },

            {
                "x": [dates[-1]],
                "y": [sea_level[-1]],
                "text": [f"{dates[-1]:.0f}<br>{sea_level[-1]:.1f} mm"],
                "type": "scatter",
                "mode": "markers+text",
                "marker": {
                    "color": "#17becf",
                    "size": 10
                },
                "textposition": "right",
                "textfont": {
                    "family": "sans serif",
                    "size": 18,
                    "color": "#17becf"
                }
            }

             ]

    layout = {
                "xaxis": {"tickformat": "%Y", "range": [dates[0], float(dates[-1])+7]},
                "yaxis": {"title": {"text": "Livello degli oceani (mm)"}},
                "title": {"text": "Variazione del livello degli oceani rispetto al 2000 (mm)"},
                "showlegend": False,
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/sea_level.json", "w") as f:
        json.dump(bundle, f, indent=4)

    # save stripes json for the stripes factory
    save_stripes(dates, sea_level, "Livello oceani (mm)", "sea_level.json", symmetric_minmax=False)

    # save overview data for overview factory
    year = int(dates[-1])
    month_decimal = float(dates[-1]) - year
    month_name = MONTHS_NAME[int(month_decimal * 12)]
    date_mmyyyy = f"{month_name} {year}"
    save_overview("sea_level", f"Livello oceani (mm, {date_mmyyyy})", f"{sea_level[-1]:+.1f}", dates[-1])
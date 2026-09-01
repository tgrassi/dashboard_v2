import pandas as pd
import json

from preprocessors.stripes_factory import save_stripes


def preprocess():


    # Year,MB_REF_count,REF_regionAVG,REF_regionAVG_cum-rel-1970
    df = pd.read_csv("data/glaciers_mass.csv")

    dates = df['Year'].astype(str).tolist()
    mass_balance = df['REF_regionAVG_cum-rel-1970'].tolist()

    # save to json
    data = [{
             "x": dates,
             "y": mass_balance,
             "type": "scatter",
             "mode": "lines+markers",
             },

            {
                "x": [dates[-1]],
                "y": [mass_balance[-1]],
                "text": [f"{dates[-1]}<br>{mass_balance[-1] / 1e3:.1f} Tt"],
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
                "xaxis": {"tickformat": "%Y", "range": [dates[0], int(dates[-1])+20]},
                "yaxis": {"title": {"text": "Bilancio di massa dei ghiacciai (Gt)"}},
                "title": {"text": "Bilancio di massa dei ghiacciai rispetto al 1970 (Gt)"},
                "showlegend": False,
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/glaciers_mass.json", "w") as f:
        json.dump(bundle, f, indent=4)

    # save stripes json for the stripes factory
    save_stripes(dates, mass_balance, "Bilancio di massa dei ghiacciai", "glaciers_mass.json", cmap="Blues")
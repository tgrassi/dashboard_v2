import pandas as pd
import json

from preprocessors.overview_factory import save_overview
from preprocessors.commons import MONTHS_NAME

def preprocess():
    # YR  MON  NINO1+2  ANOM  NINO3  ANOM.1  NINO4  ANOM.2  NINO3.4  ANOM.3
    df = pd.read_csv("data/elnino.txt", comment='#', sep='\s+')

    dates = df['YR'].astype(str) + '-' + df['MON'].astype(str)
    dates = [str(x) for x in pd.to_datetime(dates, format='%Y-%m').tolist()]

    last_month = df['MON'].tolist()[-1]
    last_year = df['YR'].tolist()[-1]

    nino12 = [float(x) for x in df['ANOM'].tolist()]
    nino3 = [float(x) for x in df['ANOM.1'].tolist()]
    nino4 = [float(x) for x in df['ANOM.2'].tolist()]
    nino34 = [float(x) for x in df['ANOM.3'].tolist()]

    val_12 = df['ANOM'].abs().max()
    val_3 = df['ANOM.1'].abs().max()
    val_4 = df['ANOM.2'].abs().max()
    val_34 = df['ANOM.3'].abs().max()

    # save to json
    data = [
                    {
                "x": dates,
                "y": nino34,
                "type": "bar",
                "name": "NINO3+4",
                "visible": "true",
                "marker": {
                    "color": nino34,
                    "colorscale": "RdBu",
                    "cmin": -val_34,
                    "cmax": val_34
                },
            },

            {
             "x": dates,
             "y": nino12,
             "type": "bar",
             "name": "NINO1+2",
             "visible": "legendonly",
             "marker": {
                 "color": nino12,
                 "colorscale": "RdBu",
                 "cmin": -val_12,
                 "cmax": val_12
               }
             },
            {
                "x": dates,
                "y": nino3,
                "type": "bar",
                "name": "NINO3",
                "visible": "legendonly",
                "marker": {
                    "color": nino3,
                    "colorscale": "RdBu",
                    "cmin": -val_3,
                    "cmax": val_3
                }
            },

            {
                "x": dates,
                "y": nino4,
                "type": "bar",
                "name": "NINO4",
                "visible": "legendonly",
                "marker": {
                    "color": nino4,
                    "colorscale": "RdBu",
                    "cmin": -val_4,
                    "cmax": val_4
                }
            }
]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Anomalia di temperatura (°C)"}},
                "title": {"text": "Qual è l'anomalia di temperatura delle regioni El Niño?"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/enso.json", "w") as f:
        json.dump(bundle, f, indent=4)

    # save overview data for overview factory
    month_name = MONTHS_NAME[last_month-1]
    save_overview("enso", f"El Niño 3+4 ({month_name} {last_year})", f"{nino34[-1]:+.1f}°C", dates[-1])

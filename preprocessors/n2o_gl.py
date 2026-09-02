import pandas as pd
import json
from preprocessors.commons import PLOTLY_COLOR_SEQUENCE

def preprocess():

    # year,month,decimal,average,average_unc,trend,trend_unc
    df = pd.read_csv("data/n2o_mm_gl.csv", comment='#')
    dates = df['decimal'].tolist()
    n2o_average = df['average'].tolist()
    n2o_trend = df['trend'].tolist()

    # save to json
    data = [{
             "x": dates,
             "y": n2o_average,
             "type": "scatter",
             "mode": "lines",
             "name": "Dati",
             "marker": {
                 "color": PLOTLY_COLOR_SEQUENCE[0]
             },
             "legendgroup": "average"
             },
            {"x": [dates[-1]],
             "y": [n2o_average[-1]],
             "type": "scatter",
             "mode": "markers",
             "showlegend": False,
             "marker": {
                 "size": 10,
                 "color": PLOTLY_COLOR_SEQUENCE[0]
             },
             "legendgroup": "average"
            },

             {
                 "x": dates,
                 "y": n2o_trend,
                 "type": "scatter",
                 "mode": "lines",
                 "name": "Trend",
                    "marker": {
                        "color": PLOTLY_COLOR_SEQUENCE[1]
                    }
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Concentrazione di N2O (ppm)"}},
                "title": {"text": "Come è cambiata la concentrazione di N<sub>2</sub>O?"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/n2o_gl.json", "w") as f:
        json.dump(bundle, f, indent=4)
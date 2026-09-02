import pandas as pd
import json
from preprocessors.commons import PLOTLY_COLOR_SEQUENCE

def preprocess():

    # year,month,decimal,average,average_unc,trend,trend_unc
    df = pd.read_csv("data/sf6_mm_gl.csv", comment='#')
    dates = df['decimal'].tolist()
    sf6_average = df['average'].tolist()
    sf6_trend = df['trend'].tolist()


    # save to json
    data = [{
             "x": dates,
             "y": sf6_average,
             "type": "scatter",
             "mode": "lines",
             "name": "Dati",
             "marker": {
                 "color": PLOTLY_COLOR_SEQUENCE[0]
             },
                "legendgroup": "average"
             },
            {"x": [dates[-1]],
             "y": [sf6_average[-1]],
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
                 "y": sf6_trend,
                 "type": "scatter",
                 "mode": "lines",
                 "name": "Trend",
                 "marker": {
                     "color": PLOTLY_COLOR_SEQUENCE[1]
                 }
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Concentrazione di SF6 (ppm)"}},
                "title": {"text": "Come è cambiata la concentrazione di SF<sub>6</sub> nel tempo?"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/sf6_gl.json", "w") as f:
        json.dump(bundle, f, indent=4)
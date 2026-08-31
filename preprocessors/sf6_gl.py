import pandas as pd
import json

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
             "name": "Media",
             },

             {
                 "x": dates,
                 "y": sf6_trend,
                 "type": "scatter",
                 "mode": "lines",
                 "name": "Trend",
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Concentrazione di SF6 (ppm)"}},
                "title": {"text": "Concentrazione di SF<sub>6</sub>"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/sf6_gl.json", "w") as f:
        json.dump(bundle, f, indent=4)
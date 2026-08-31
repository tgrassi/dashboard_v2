import pandas as pd
import json

def preprocess():

    # year,month,decimal,average,average_unc,trend,trend_unc
    df = pd.read_csv("data/ch4_mm_gl.csv", comment='#')
    dates = df['decimal'].tolist()
    ch4_average = df['average'].tolist()
    ch4_trend = df['trend'].tolist()


    # save to json
    data = [{
             "x": dates,
             "y": ch4_average,
             "type": "scatter",
             "mode": "lines",
             "name": "Media",
             },

             {
                 "x": dates,
                 "y": ch4_trend,
                 "type": "scatter",
                 "mode": "lines",
                 "name": "Trend",
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Concentrazione di CH4 (ppm)"}},
                "title": {"text": "Concentrazione di CH<sub>4</sub>"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/ch4_gl.json", "w") as f:
        json.dump(bundle, f, indent=4)
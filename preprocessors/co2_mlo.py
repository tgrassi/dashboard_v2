import pandas as pd
import json

def preprocess():

    #co2_daily_mlo.csv
    df = pd.read_csv("data/co2_daily_mlo.csv", comment='#', names=["year", "month", "day", "decimal_date", "co2"])
    dates_daily = df['decimal_date'].tolist()
    co2_daily = df['co2'].tolist()


    # year,month,decimal date,average,deseasonalized,ndays,sdev,unc
    df = pd.read_csv("data/co2_mm_mlo.csv", comment='#')
    dates_monthly = df['decimal date'].tolist()
    co2_monthly = df['deseasonalized'].tolist()


    # save to json
    data = [{
             "x": dates_daily,
             "y": co2_daily,
             "type": "scatter",
             "mode": "lines",
             "name": "Giornaliero",
             },

             {
                 "x": dates_monthly,
                 "y": co2_monthly,
                 "type": "scatter",
                 "mode": "lines",
                 "name": "Media",
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Concentrazione di CO2 (ppm)"}},
                "title": {"text": "Concentrazione di CO<sub>2</sub> Mauna Loa (Hawaii)"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/co2_mlo.json", "w") as f:
        json.dump(bundle, f, indent=4)
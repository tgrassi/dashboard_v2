import pandas as pd
import json
from preprocessors.commons import PLOTLY_COLOR_SEQUENCE
from preprocessors.stripes_factory import save_stripes
from preprocessors.overview_factory import save_overview

def preprocess():

    #co2_daily_mlo.csv
    df = pd.read_csv("data/co2_daily_mlo.csv", comment='#', names=["year", "month", "day", "decimal_date", "co2"])
    dates_daily = df['decimal_date'].tolist()
    co2_daily = df['co2'].tolist()

    last_date_ddmmyyyy = str(df["day"].tolist()[-1]) + "/" + str(df["month"].tolist()[-1]) + "/" + str(df["year"].tolist()[-1])

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
             "legendgroup": "daily",
             "marker": {
                 "color": PLOTLY_COLOR_SEQUENCE[0]
             }
             },
            {
                "x": [dates_daily[-1]],
                "y": [co2_daily[-1]],
                "type": "scatter",
                "mode": "markers",
                "showlegend": False,
                "marker": {
                    "size": 10,
                    "color": PLOTLY_COLOR_SEQUENCE[0]
                },
                "legendgroup": "daily"
            },

             {
                 "x": dates_monthly,
                 "y": co2_monthly,
                 "type": "scatter",
                 "mode": "lines",
                 "name": "Media",
                 "marker": {
                     "color": PLOTLY_COLOR_SEQUENCE[1]
                 }
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Concentrazione di CO2 (ppm)"}},
                "title": {"text": "Come è cambiata la concentrazione di anidride carbonica (CO<sub>2</sub>) nel tempo?"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/co2_mlo.json", "w") as f:
        json.dump(bundle, f, indent=4)


    # save stripes json for the stripes factory
    save_stripes(dates_monthly, co2_monthly, "Concentrazione di CO2 (ppm)", "co2_mlo.json", symmetric_minmax=False)

    # save overview data for overview factory
    save_overview("co2_mlo", f"Concentrazione di CO2 (ppm, {last_date_ddmmyyyy})", f"{co2_daily[-1]:.1f}", dates_daily[-1])
import pandas as pd
import json

from preprocessors.stripes_factory import save_stripes

def preprocess():

    # gas_ageBP	CO2
    df = pd.read_csv("data_fix/edc3-composite-co2-2008-noaa.txt", comment="#", delimiter="\t")

    years_ago = df["gas_ageBP"].tolist()
    co2 = df["CO2"].tolist()

    # year,month,decimal date,average,deseasonalized,ndays,sdev,unc
    df = pd.read_csv("data/co2_mm_mlo.csv", comment='#')
    dates_monthly = df['decimal date'].tolist()
    co2_monthly = df['deseasonalized'].tolist()

    max_year = dates_monthly[-1]

    years_ago = years_ago[::-1] + [max_year - y for y in dates_monthly]
    co2 = co2[::-1] + co2_monthly

    # save to json
    data = [{
             "x": years_ago,
             "y": co2,
             "type": "scatter",
             }]

    layout = {
                "xaxis": {"title": {"text": "Anni fa"}, "autorange": "reversed"},
                "yaxis": {"title": {"text": "Concentrazione di CO2 (ppm)"}},
                "title": {"text": "Concentrazione di CO2 negli ultimi 800.000 anni"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/co2_800kyr.json", "w") as f:
        json.dump(bundle, f, indent=4)

    # save stripes json for the stripes factory
    save_stripes(years_ago, co2, "Concentrazione di CO2", "co2_800kyr.json", symmetric_minmax=True)
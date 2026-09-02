# load GLB.Ts+dSST.csv
import pandas as pd
import json
import numpy as np
from preprocessors.commons import MONTHS_NAME
from preprocessors.stripes_factory import save_stripes
from preprocessors.overview_factory import save_overview

def preprocess():
    """Preprocess the global temperature data."""
    df = pd.read_csv("data/GLB.Ts+dSST.csv", skiprows=1)
    # Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON
    df = df.rename(columns={"Year": "year", "J-D": "annual_mean"})

    # unique years
    years = df["year"].unique()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    last_month = "-"

    dates = []
    temperatures_monthly = []
    temperatures_yearly = []
    for year in years:
        # loop on months columns
        for i, month in enumerate(months):
            # get the value for the month
            value = df.loc[df["year"] == year, month].values[0]
            if value != "***":
                # create a date string
                date = f"{year}-{i+1:02d}-01"
                dates.append(date)
                temperatures_monthly.append(float(value))
                last_month = month
        # append the annual mean to the yearly temperatures
        annual_mean = df.loc[df["year"] == year, "annual_mean"].values[0]
        if annual_mean != "***":
            temperatures_yearly.append(float(annual_mean))

    years = [int(x) for x in years]

    val_monthly = np.abs(temperatures_monthly).max()
    val_yearly = np.abs(temperatures_yearly).max()

    # save to json
    data_monthly = [{
             "x": dates,
             "y": temperatures_monthly,
             "type": "bar",
             "marker": {
                 "color": temperatures_monthly,
                 "colorscale": "RdBu",
                 "cmin": -val_monthly,
                 "cmax": val_monthly
               }
             }]

    layout_monthly = {
                "xaxis": {"tickformat": "%b %Y"},
                "yaxis": {"title": {"text": "Anomalia temperatura (°C)"}},
                "title": {"text": "Quanto si è scaldato il pianeta (media 1951-1980)?"}
             }


    data_yearly = [
            {
                "x": years,
                "y": temperatures_yearly,
                "type": "scatter",
                "mode": "lines+markers",
                "marker": {
                    "color": temperatures_yearly,
                    "colorscale": "RdBu",
                    "cmin": -val_yearly,
                    "cmax": val_yearly
                }
            }
            ]

    layout_yearly = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Anomalia temperatura (°C)"}},
                "title": {"text": "Quanto si è scaldato il pianeta ogni anno (media 1951-1980)?"}
             }


    # first layout so it is easier to debug in the json file
    bundle_monthly = {"layout": layout_monthly, "data": data_monthly}

    bundle_yearly = {"layout": layout_yearly, "data": data_yearly}

    with open("website/data/global_temperature_monthly.json", "w") as f:
        json.dump(bundle_monthly, f, indent=4)

    with open("website/data/global_temperature_yearly.json", "w") as f:
        json.dump(bundle_yearly, f, indent=4)

    # save stripes json for the stripes factory
    save_stripes(dates, temperatures_monthly, "Anomalia temperatura globale (°C, 1951-1980)", "global_temperature.json", symmetric_minmax=True)

    # save overview data for overview factory
    month_locale = MONTHS_NAME[months.index(last_month)]
    save_overview("global_temperature", f"Anomalia Temperatura Globale ({month_locale})", f"{temperatures_monthly[-1]:+.1f}°C", dates[-1])

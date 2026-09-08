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
    dates_yearly = []
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
            dates_yearly.append(year)

    years = [int(x) for x in years]
    dates_yearly = [int(x) for x in dates_yearly]

    val_monthly = np.abs(temperatures_monthly).max()
    val_yearly = np.abs(temperatures_yearly).max()

    xdata_fit = [x for x in dates_yearly if x >= 1970]
    ydata_fit = [y for x, y in zip(dates_yearly, temperatures_yearly) if x >= 1970]

    # linear fit
    coeffs = np.polyfit(xdata_fit, ydata_fit, 1)

    temperatures_yearly_fit = np.polyval(coeffs, xdata_fit)
    temperatures_yearly_fit = [float(x) for x in temperatures_yearly_fit]


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
                "xaxis": {
                    "tickformatstops": [
                    {
                    "dtickrange": ["null", 'M1'],
                    "value": '%b %Y'
                    },
                    {
                    "dtickrange": ['M1', 'M12'],
                    "value": '%b %Y'
                    },
                    {
                    "dtickrange": ['M12', "null"],
                    "value": '%Y'
                    }]
                },
                "yaxis": {"title": {"text": "Anomalia temperatura (°C)"}},
                "title": {"text": "Quanto si è scaldato il pianeta (media 1951-1980)?"}
             }


    data_yearly = [
            {
                "x": dates_yearly,
                "y": temperatures_yearly,
                "type": "scatter",
                "mode": "lines+markers",
                "marker": {
                    "color": temperatures_yearly,
                    "colorscale": "RdBu",
                    "cmin": -val_yearly,
                    "cmax": val_yearly
                },
                "name": "Anomalia"
            },
            {
                "x": xdata_fit,
                "y": temperatures_yearly_fit,
                "type": "scatter",
                "mode": "lines",
                "name": "Fit lineare",
                "line": {
                    "color": "#0DE4E4",
                    "width": 2,
                }
            }
            ]

    layout_yearly = {
                "xaxis": {
                    "tickformatstops": [
                    {
                    "dtickrange": ["null", 'M1'],
                    "value": '%b %Y'
                    },
                    {
                    "dtickrange": ['M1', 'M12'],
                    "value": '%b %Y'
                    },
                    {
                    "dtickrange": ['M12', "null"],
                    "value": '%Y'
                    }]
                },
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

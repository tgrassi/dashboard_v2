import json

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def preprocess():
    # year,month,decimal date,average,deseasonalized,ndays,sdev,unc
    df = pd.read_csv("data/co2_mm_mlo.csv", comment='#')
    dates_co2 = df['decimal date'].tolist()
    values_co2 = df['deseasonalized'].tolist()


    df = pd.read_csv("data/GLB.Ts+dSST.csv", skiprows=1)
    # Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D,D-N,DJF,MAM,JJA,SON

    # unique years
    years = df["Year"].unique()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    dates_temperature = []
    values_temperature = []
    for year in years:
        # loop on months columns
        for i, month in enumerate(months):
            # get the value for the month
            value = df.loc[df["Year"] == year, month].values[0]
            if value != "***":
                # create a date string
                date = year + i / 12.0
                dates_temperature.append(date)
                values_temperature.append(float(value))

    date_min = max(dates_co2[0], dates_temperature[0])
    date_max = min(dates_co2[-1], dates_temperature[-1])


    f_co2 = interp1d(dates_co2, values_co2)
    f_temperature = interp1d(dates_temperature, values_temperature)

    dates = np.linspace(date_min, date_max, 100)

    xdata = [float(x) for x in np.log2(f_co2(dates))]
    ydata = [float(y) for y in f_temperature(dates)]

    # linear fit
    coeffs = np.polyfit(xdata, ydata, 1)

    xx_fit = [float(x) for x in np.linspace(min(xdata), max(xdata), 10)]
    yy_fit = [float(y) for y in np.polyval(coeffs, xx_fit)]

    # save to json
    data = [{
             "x": xdata,
             "y": ydata,
             "type": "scatter",
             "mode": "markers",
             "name": "Dati"
             },
             {
             "x": xx_fit,
             "y": yy_fit,
             "type": "scatter",
             "mode": "lines",
             "name": "Fit Lineare"
             }
             #{coeffs[0]:.2f}
             ]

    layout = {
        "xaxis": {"title": {"text": "Log2 della Concentrazione di CO2 (ppm)"}},
        "yaxis": {"title": {"text": "Anomalia di temperatura globale (°C)"}},
        "title": {"text": "Correlazione tra concentrazione di CO2 e anomalia di temperatura globale"},
        "showlegend": False,
        "annotations": [
            {
                "x": 0.05,
                "y": 0.95,
                "xref": "paper",
                "yref": "paper",
                "text": f"{coeffs[0]:+.2f} °C per raddoppio della CO2",
                "showarrow": False,
                "font": {"size": 14}
             }
                ]
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/correlation_temp_co2.json", "w") as f:
        json.dump(bundle, f, indent=4)
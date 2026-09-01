import json

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def preprocess():
    # 1749 01 1749.042   96.7  -1.0    -1
    df = pd.read_csv("data/sunspots.txt", names=["year", "month", "decimal_date", "sunspots", "a", "b", "c"], comment='#', delim_whitespace=True, header=None)

    dates_sunspots = df['decimal_date'].tolist()
    values_sunspots = df['sunspots'].tolist()


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

    date_min = max(dates_sunspots[0], dates_temperature[0])
    date_max = min(dates_sunspots[-1], dates_temperature[-1])


    f_sunspots = interp1d(dates_sunspots, values_sunspots)
    f_temperature = interp1d(dates_temperature, values_temperature)

    dates = np.linspace(date_min, date_max, 100)

    xdata = [float(x) for x in f_sunspots(dates)]
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
        "xaxis": {"title": {"text": "Numero di macchie solari"}},
        "yaxis": {"title": {"text": "Anomalia di temperatura globale (°C)"}},
        "title": {"text": "Mancata correlazione tra numero di macchie solari e anomalia di temperatura globale"},
        "showlegend": False,
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/correlation_temp_sunspots.json", "w") as f:
        json.dump(bundle, f, indent=4)
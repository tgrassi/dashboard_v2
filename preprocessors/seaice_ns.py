import json
import pandas as pd
from preprocessors.commons import PLOTLY_COLOR_SEQUENCE
import numpy as np

def preprocess():
    preprocess_NS("N")
    preprocess_NS("S")

def preprocess_NS(what):
    # Year, Month, Day,     Extent,    Missing, Source Data
    df = pd.read_csv("data/{}_seaice_extent_daily_v4.0.csv".format(what), skiprows=2, comment='#', names=["Year", "Month", "Day", "Extent", "Missing", "Source Data"])

    dates = df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-' + df['Day'].astype(str)
    dates = [str(x) for x in pd.to_datetime(dates, format='%Y-%m-%d').tolist()]

    doy_all = np.array(pd.to_datetime(dates).dayofyear.tolist())
    years_all = np.array(df['Year'].tolist())
    extent_all = np.array(df['Extent'].tolist())

    assert len(doy_all) == len(years_all), "Length of doy_all and years_all should be the same"
    assert len(doy_all) == len(extent_all), "Length of doy_all and extent_all should be the same"

    # unique years
    years = df['Year'].unique().tolist()

    max_year = max([int(x) for x in years])
    min_year = min([int(x) for x in years])

    data = []

    step = 10
    for year in range(max_year-step, min_year - 1, -step):
        avgs = np.full((365, step), np.nan)
        for i, y in enumerate(range(year, year+step)):
            idx = (years_all == y) & (doy_all <= 365)  # only consider days up to 365 (ignore leap day)
            doy = doy_all[idx]
            avgs[doy-1, i] = extent_all[idx]

        avgs_mean = [float(x) for x in np.nanmean(avgs, axis=1)]
        new_dates = pd.to_datetime(np.arange(1, 366), format='%j').strftime('2000-%m-%d')
        dates_uniform = [str(x) for x in new_dates.tolist()]

        data.append(
            {
                "x": dates_uniform,
                "y": avgs_mean,
                "type": "scatter",
                "name": "{}-{}".format(year, year+step-1),
                "visible": "true",
                "line": {"dash": "dot"},
                "mode": "lines",
            }
        )

    # this is to have 9 colors and to avoid the same color when showing a line every 10 years
    color_sequence = PLOTLY_COLOR_SEQUENCE[:9]

    for year in years[::-1]:
        dd = df[df['Year'] == year]
        # create new dates with 2000 year (leap year) to uniform the x axis for consistent visualization
        new_dates = pd.to_datetime(dd['Day'].astype(str) + '-' + dd['Month'].astype(str) + '-2000', format='%d-%m-%Y')
        dates_uniform = [str(x) for x in new_dates.tolist()]
        ice_extent = dd['Extent'].tolist()

        # if the year is greater than max_year-2, make it visible, otherwise make it legendonly
        # (so that it is not visible by default but still in the legend)

        if year == max_year:
            visible = "true"
        else:
            visible = "legendonly"

        if int(year) == max_year:
            line = {"color": "#17becf",
                    "width": 2}
        else:
            color = color_sequence[(max_year - int(year)) % len(color_sequence)]
            line = {"color": color}

        data.append(
            {
                "x": dates_uniform,
                "y": ice_extent,
                "type": "scatter",
                "name": year,
                "visible": visible,
                "line": line,
                "mode": "lines",
            }
        )

    # add the last point of the last year as scatter point (so that it is visible in the legend)
    last_extent = df["Extent"].iloc[-1]

    last_date_text = df["Day"].iloc[-1].astype(str) + '/' + df["Month"].iloc[-1].astype(str) + '/' + df["Year"].iloc[-1].astype(str)

    # convert to iso date
    last_date = pd.to_datetime(last_date_text, format='%d/%m/%Y').strftime('2000-%m-%d')


    data.append({
        "x": [last_date],
        "y": [last_extent],
        "type": "scatter",
        "mode": "markers",
        "name": last_date_text,
        "marker": {"size": 10,
                   "color": "#17becf"}
    })

    what_fullname = "Artico" if what == "N" else "Antartico"

    layout = {
        "xaxis": {
                    "tickformatstops": [
                    {
                    "dtickrange": ["null", 'M1'],
                    "value": '%d %b'
                    },
                    {
                    "dtickrange": ['M1', 'M12'],
                    "value": '%b'
                    },
                    {
                    "dtickrange": ['M12', "null"],
                    "value": '%b'
                    }]
        },
        "yaxis": {
            "title": {"text": "Estensione Ghiaccio (10<sup>6</sup> km<sup>2</sup>)"},
        },
        "title": {
            "text": "Qual è l'estensione del ghiaccio marino {}?".format(what_fullname),
        }
    }

    bundled_data = {
        "layout": layout,
        "data": data
    }

    what_str = "north" if what == "N" else "south"
    with open('website/data/seaice_{}.json'.format(what_str), 'w') as f:
        json.dump(bundled_data, f, indent=4)
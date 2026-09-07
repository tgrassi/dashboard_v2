import pandas as pd
import json
import numpy as np

def preprocess():
    """Preprocess the global temperature data."""

    # date,2t,clim_91-20,ano_91-20,status
    df = pd.read_csv("data/era5_daily_series_2t_global.csv", skiprows=1, comment='#')

    # unique years
    years = df["date"].str[:4].unique()
    data_tmp = []

    # get the maximum year (i.e. the most recent year, likely the current year)
    max_year = max([int(year) for year in years])

    avgs_ranges = ["1991-2020", "1981-2010", "1971-2000", "1961-1990", "1951-1980"]
    avg = {x: [] for x in avgs_ranges}

    # iterate over the years in reverse order (so that the most recent year is plotted on top)
    # this will fill the data list for the plotly plot, with each year as a separate line
    for year in years[::-1]:
        # filter the dataframe for the current year
        df_year = df[df["date"].str.startswith(year)]

        # change the year to 1970 to have the same x axis for all years (1970 is a leap year)
        dates = ("1970-" + df_year["date"].str[5:]).tolist()

        # get the temperatures for the current year
        temperatures = df_year["2t"].tolist()

        # store temperatures for averaging later
        for ar in avgs_ranges:
            amin, amax = [int(x) for x in ar.split("-")]
            if int(year) >= amin and int(year) <= amax:
                # get the average temperature for the current year and range
                avg[ar].append(temperatures[:365])

        # if the year is greater than max_year-2, make it visible, otherwise make it legendonly
        # (so that it is not visible by default but still in the legend)
        if int(year) > max_year-2:
            visible = "true"
        else:
            visible = "legendonly"

        if int(year) == max_year:
            line = {"color": "red",
                    "width": 2}
        else:
            line = {}

        # store in a temporary list to be able to sort it later
        data_tmp.append({
            "x": dates,
            "y": temperatures,
            "type": "line",
            "name": year,
            "visible": visible,
            "line": line,
            "legendgroup": year
        })

    # create the data list for the plotly plot, with the most recent year on top
    data = [data_tmp[0]]

    # compute the average for each range and add it to the data list
    avg = {k: np.stack(v).mean(axis=0).tolist() for k, v in avg.items()}

    for ar in avgs_ranges:
        data.append({
            "x": dates[:365],
            "y": avg[ar],
            "type": "line",
            "name": f"Media {ar}",
            "line": {"dash": "dot"},
            "visible": "legendonly"
        })

    # add the rest of the years to the data list
    data.extend(data_tmp[1:])


    # add the last point of the last year as scatter point (so that it is visible in the legend)
    last_year = years[-1]
    last_year_df = df[df["date"].str.startswith(last_year)]
    last_date = "1970-" + last_year_df["date"].iloc[-1][5:]
    last_temperature = last_year_df["2t"].iloc[-1]

    last_date_text = last_year_df["date"].iloc[-1]
    last_date_year = last_date_text[:4]
    last_date_month = last_date_text[5:7]
    last_date_day = last_date_text[8:10]
    last_date_ddmmyyyy = f"{last_date_day}/{last_date_month}/{last_date_year}"


    data.append({
        "x": [last_date],
        "y": [last_temperature],
        #"text": [f"{last_date_ddmmyyyy}<br>\n{last_temperature:+.1f} °C"],
        "type": "scatter",
        "name": last_year,
        "mode": "markers",
        "legendgroup": last_year,
        "showlegend": False,
        # "textposition": "right",
        # "textfont": {
        #     "family": "sans serif",
        #     "size": 18,
        #     "color": "red"
        # },
        "marker": {"size": 10, "color": "red"}
    })

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
                "yaxis": {"title": {"text": "Temperatura (°C)"}},
                "title": {"text": "Qual è la temperatura giornaliera del pianeta?"}
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/era5_daily.json", "w") as f:
        json.dump(bundle, f, indent=4)

import pandas as pd
import json

def preprocess():
    """Preprocess the global temperature ocean data."""

    # date,2t,clim_91-20,ano_91-20,status
    df = pd.read_csv("data/era5_daily_series_sst_60S-60N_ocean.csv", skiprows=1, comment='#')

    # unique years
    years = df["date"].str[:4].unique()
    data = []

    # get the maximum year (i.e. the most recent year, likely the current year)
    max_year = max([int(year) for year in years])

    # iterate over the years in reverse order (so that the most recent year is plotted on top)
    # this will fill the data list for the plotly plot, with each year as a separate line
    for year in years[::-1]:
        # filter the dataframe for the current year
        df_year = df[df["date"].str.startswith(year)]

        # change the year to 1970 to have the same x axis for all years (1970 is a leap year)
        dates = ("1970-" + df_year["date"].str[5:]).tolist()

        # get the temperatures for the current year
        temperatures = df_year["sst"].tolist()

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

        data.append({
            "x": dates,
            "y": temperatures,
            "type": "line",
            "name": year,
            "visible": visible,
            "line": line
        })

    # add the last point of the last year as scatter point (so that it is visible in the legend)
    last_year = years[-1]
    last_year_df = df[df["date"].str.startswith(last_year)]
    last_date = "1970-" + last_year_df["date"].iloc[-1][5:]
    last_temperature = last_year_df["sst"].iloc[-1]

    last_date_text = last_year_df["date"].iloc[-1]
    last_date_year = last_date_text[:4]
    last_date_month = last_date_text[5:7]
    last_date_day = last_date_text[8:10]
    last_date_ddmmyyyy = f"{last_date_day}/{last_date_month}/{last_date_year}"


    data.append({
        "x": [last_date],
        "y": [last_temperature],
        "text": [f"{last_date_ddmmyyyy}<br>\n{last_temperature:+.1f} °C"],
        "type": "scatter",
        "name": last_year,
        "mode": "markers+text",
        "textposition": "right",
        "textfont": {
            "family": "sans serif",
            "size": 18,
            "color": "red"
        },
        "marker": {"size": 10, "color": "red"}
    })

    layout = {
                "xaxis": {"tickformat": "%b"},
                "yaxis": {"title": {"text": "Temperatura (°C)"}}
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout, "data": data}

    with open("website/data/era5_ocean.json", "w") as f:
        json.dump(bundle, f, indent=4)

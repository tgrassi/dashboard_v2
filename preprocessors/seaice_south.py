import json
import pandas as pd
from preprocessors.commons import PLOTLY_COLOR_SEQUENCE

def preprocess():

    # Year, Month, Day,     Extent,    Missing, Source Data
    df = pd.read_csv("data/S_seaice_extent_daily_v4.0.csv", skiprows=2, comment='#', names=["Year", "Month", "Day", "Extent", "Missing", "Source Data"])

    dates = df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-' + df['Day'].astype(str)
    dates = [str(x) for x in pd.to_datetime(dates, format='%Y-%m-%d').tolist()]

    # unique years
    years = df['Year'].unique().tolist()

    max_year = max([int(x) for x in years])


    # this is to have 9 colors and to avoid the same color when showing a line every 10 years
    color_sequence = PLOTLY_COLOR_SEQUENCE[:9]

    data = []
    for year in years[::-1]:
        dd = df[df['Year'] == year]
        # create new dates with 2000 year (leap year) to uniform the x axis for consistent visualization
        new_dates = pd.to_datetime(dd['Day'].astype(str) + '-' + dd['Month'].astype(str) + '-2000', format='%d-%m-%Y')
        dates_uniform = [str(x) for x in new_dates.tolist()]
        ice_extent = dd['Extent'].tolist()

        # if the year is greater than max_year-2, make it visible, otherwise make it legendonly
        # (so that it is not visible by default but still in the legend)

        is_multiple_of_10 = (max_year - int(year)) % 10 == 0

        if is_multiple_of_10:
            visible = "true"
        else:
            visible = "legendonly"

        if int(year) == max_year:
            line = {"color": "#17becf",
                    "width": 2}
        else:
            color = color_sequence[(max_year - int(year)) % len(color_sequence)]
            line = {"color": color}

        data .append(
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
        "text": [f"{last_date_text}<br>\n{last_extent:.1f}&#x2715;10<sup>6</sup> km<sup>2</sup>"],
        "type": "scatter",
        "mode": "markers+text",
        "textposition": "right",
        "name": last_date_text,
        "textfont": {
            "family": "sans serif",
            "size": 18,
            "color": "#17becf"
        },
        "marker": {"size": 10,
                   "color": "#17becf"}
    })


    layout = {
        "xaxis": {
            "title": "Date",
            "tickformat": "%b",
        },
        "yaxis": {
            "title": "Estensione Ghiaccio (10<sup>6</sup> km<sup>2</sup>)",
        },
        "title": {
            "text": "Estensione del ghiaccio marino antartico",
        }
    }

    bundled_data = {
        "layout": layout,
        "data": data
    }

    with open('website/data/seaice_south.json', 'w') as f:
        json.dump(bundled_data, f, indent=4)
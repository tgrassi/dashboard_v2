import json
from datetime import datetime, timedelta


def preprocess():
    # import data/enso_daily.json
    with open("data/enso_daily.json", "r") as f:
        data_json = json.load(f)

    current_year = datetime.now().year

    # THIS IS HARDCODED! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    enso_years = [1982, 1997, 2015, 2023, current_year]

    data = []

    for d in data_json[::-1]:
        try:
            year = int(d["name"])
        except (ValueError, TypeError):
            continue

        if year not in enso_years:
            continue

        temperatures = d["data"]

        dates = []
        ydata = []
        for i in range(len(temperatures)):
            if temperatures[i] is None:
                continue

            ydata.append(float(temperatures[i]))
            # convert doy to date
            dates.append(datetime(1972, 1, 1) + timedelta(days=i))

        xdata = [str(x) for x in dates]

        data.append({
            "x": xdata,
            "y": ydata,
            "type": "scatter",
            "name": str(year),
            "mode": "lines",
            "showlegend": True,
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
                    }]
                },
                "yaxis": {"title": {"text": "Anomalia di temperatura (°C)"}},
                "title": {"text": "Qual è l'anomalia giornaliera El Niño 3+4?"},
                }

    bundled_data = {
        "layout": layout,
        "data": data
    }

    with open('website/data/enso_daily.json', 'w') as f:
        json.dump(bundled_data, f, indent=4)
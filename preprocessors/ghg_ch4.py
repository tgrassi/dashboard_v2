import pandas as pd
import json
from preprocessors.overview_factory import save_overview
from preprocessors.commons import MONTHS_NAME, PLOTLY_COLOR_SEQUENCE, get_info
from preprocessors.stripes_factory import save_stripes

def preprocess():

    # year,month,decimal,average,average_unc,trend,trend_unc
    df = pd.read_csv("data/ch4_mm_gl.csv", comment='#')
    dates = df['decimal'].tolist()
    ch4_average = df['average'].tolist()
    ch4_trend = df['trend'].tolist()

    last_month = MONTHS_NAME[df['month'].tolist()[-1]-1]
    last_year = df['year'].tolist()[-1]

    # save to json
    data = [{
             "x": dates,
             "y": ch4_average,
             "type": "scatter",
             "mode": "lines",
             "name": "Dati",
             "marker": {
                 "color": PLOTLY_COLOR_SEQUENCE[0]
                },
             "legendgroup": "average"
             },
            {
                "x": [dates[-1]],
                "y": [ch4_average[-1]],
                "type": "scatter",
                "mode": "markers",
                "showlegend": False,
                "marker": {
                    "size": 10,
                    "color": PLOTLY_COLOR_SEQUENCE[0]
                },
                "legendgroup": "average"
            },

             {
                 "x": dates,
                 "y": ch4_trend,
                 "type": "scatter",
                 "mode": "lines",
                 "name": "Trend",
                 "marker": {
                     "color": PLOTLY_COLOR_SEQUENCE[1]
                 }
             }]

    layout = {
                "xaxis": {"tickformat": "%Y"},
                "yaxis": {"title": {"text": "Concentrazione di CH4 (ppb)"}},
                "title": {"text": "Come è cambiata la concentrazione di metano (CH<sub>4</sub>) nel tempo?"},
             }

    # first layout so it is easier to debug in the json file
    bundle = {"layout": layout,
              "data": data,
              "text_content": get_info("ghg_ch4")}

    with open("website/data/ch4_gl.json", "w") as f:
        json.dump(bundle, f, indent=4)

    # save stripes json for the stripes factory
    save_stripes(dates, ch4_average, "Concentrazione di CH4 (ppb)", "ch4_gl.json", symmetric_minmax=False)

    # save overview data for overview factory
    save_overview("ch4_gl", f"Concentrazione di metano (ppb, {last_month} {last_year})", f"{ch4_average[-1]:.1f}", dates[-1])
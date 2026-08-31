import json

def save_stripes(xdata, ydata, title, filename, cmap="RdBu", symmetric_minmax=False):

    if filename.endswith(".json"):
        filename = filename[:-5]

    data = {
            "title": title,
            "x": xdata,
            "y": ydata,
            "symmetric_minmax": symmetric_minmax,
            "cmap": cmap
            }

    with open(f"data_stripes/{filename}.json", "w") as f:
        json.dump(data, f, indent=4)
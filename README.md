# dashboard_v2

--------------------
### Download data
- `downloader.py` downloads the data by calling downloders functions
- Data are stored in `./data`
- Downloaders are in `./downloders`


--------------------
### Preprocess data
- `preprocess.py` preprocess the data by calling preprocessors functions
- The concept is that this produces the json necessary to pyplot to plot
- Preprocessors are in `./preprocessors`
- Json are stored in `./website/data/`

Example:
```
{
    "data": [
        {
            "x": [1, 2, 3, 4, 5],
            "y": [1, 2, 4, 8, 16],
            "type": "scatter",
            "mode": "lines"
        }
    ],
    "layout": {
        "title": {"text": "Test Plot"}
    }
}
```

Note that it contains `data` and `layout` to prepare the plot.

--------------------
### Website
- see `./website` folder.
- `index.html` call an external sidebar (`sidebar.html`) with the different topics (see sections)
- `index.html` contains a set of sections
- Each section is for a topic (e.g., temperature)
- In each section there is a list of `div` and a list of JS scripts to produce the plot
- The scripts are in `./website/plots`
- A set of utility functions (included the global plotting style) are in `./website/plotting`



// this function is to test the plot function.
// the plot function is defined in website/plotting/plot.js
// the data for the plot is defined in website/data/test.json
// the id of the div where the plot is plotted is "plot_test"
/*
example of the data in website/data/test.json:
[
    {
        "x": [1, 2, 3, 4, 5],
        "y": [1, 2, 4, 8, 16],
        "type": "scatter",
        "mode": "lines"
    }
]
*/
plot("data/test.json", "plot_test");
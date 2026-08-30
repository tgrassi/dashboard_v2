
// this function is a generic plot function.
// the definition of the plot is contained in a json file (see website/data/test.json for an example).
// the id is the id of the div where the plot is plotted
// the theme is a global variable defined in website/plotting/plotly_theme.js
function plot(data_json, id){
    fetch(data_json)
        .then(response => response.json())
        .then(bundle => {
            var element = document.getElementById(id);

            var data = bundle.data;

            var layout = bundle.layout;
            layout.template = dashboardTheme;

            Plotly.newPlot(element, data, layout);
        });
}
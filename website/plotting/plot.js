
// this function is a generic plot function.
// the definition of the plot is contained in a json file (see website/data/test.json for an example).
// the id is the id of the div where the plot is plotted
// the theme is a global variable defined in website/plotting/plotly_theme.js
function plot(data_json, id, style=null, use_button_text=true){

    // create a div child of the div with id=id
    var parent = document.getElementById(id);
    var child_plot = document.createElement("div");
    child_plot.setAttribute("id", id + "_plot");

    parent.appendChild(child_plot);

    if (use_button_text){
        var child_button = document.createElement("button");
        var child_button_id = id + "_button";
        child_button.setAttribute("id", child_button_id);
        child_button.innerHTML = "...";
        child_button.setAttribute("class", "button");

        parent.appendChild(child_button);
    }

    if (style != null){
        child_plot.setAttribute("style", style);
    }else{
        child_plot.setAttribute("style", "width: 800px; height: 600;");
    }

    fetch(data_json)
        .then(response => response.json())
        .then(bundle => {

            var data = bundle.data;

            var layout = bundle.layout;
            layout.template = dashboardTheme;

            var config = {locale: 'it'};
            Plotly.newPlot(child_plot, data, layout, config);

            if (use_button_text){
                if(bundle.hasOwnProperty("text_content")){
                    var text_content = bundle.text_content;
                    child_button.setAttribute("onclick", "toggleDescription('" + text_content + "', '" + child_button_id + "')");
                }else{
                    child_button.remove();
                }
            }
        });

}


function toggleDescription(text_content, button_id){
    const button = document.getElementById(button_id);
    button.classList.toggle("expanded");
    button.classList.toggle("collapsed");
    button.innerHTML = button.classList.contains("expanded") ? text_content : "...";
}
import json
from glob import glob


# <div class="dmu-19__card">
#     <div class="dmu-19__cardTop">
#     <span class="dmu-19__badge dmu-19__badge--feature">Temperatura Globale</span>
#     </div>
#     <h2 class="dmu-19__value">+1.1°C</h2>
# </div>

div_template = """
// create parent div at script position in the HTML
var parentDiv = document.createElement('div');
parentDiv.className = 'dmu-19__card';

// create cardTop div
var topDiv = document.createElement('div');
topDiv.className = 'dmu-19__cardTop';

// create badge span
var badgeSpan = document.createElement('span');
badgeSpan.className = 'dmu-19__badge dmu-19__badge--feature';
badgeSpan.textContent = '{name}';

// append badge to top div
topDiv.appendChild(badgeSpan);

// append top div to parent div
parentDiv.appendChild(topDiv);

// create value h2
var valueH2 = document.createElement('h2');
valueH2.className = 'dmu-19__value';
valueH2.textContent = '{value}';

// append value h2 to parent div
parentDiv.appendChild(valueH2);
"""


def preprocess():

    js_script = "var script = document.currentScript;\n\n"

    for g in glob("data_overview/*.json"):

        print(f"OVERVIEW: Preprocessing {g}...")

        with open(g, "r") as f:
            data = json.load(f)

        js_script += f"// --------------------------------\n"
        js_script += f"// Overview data for {data['name']}\n"
        js_script += f"// --------------------------------\n"

        js_script += div_template.format(name=data["name"], value=data["value"]) + "\n"

        js_script += "script.parentNode.insertBefore(parentDiv, script);\n\n"

    with open("website/data/overview.js", "w") as f:
        f.write(js_script)

def save_overview(id, name, value, date=None):
    """Save the overview data to a JSON file."""
    data = {
        "name": name,
        "value": value,
        "date": date,
    }

    with open(f"data_overview/{id}.json", "w") as f:
        json.dump(data, f, indent=4)



import os

PLOTLY_COLOR_SEQUENCE = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

MONTHS_NAME = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

MONTHS_NAME_SHORT = [x[:3] for x in MONTHS_NAME]

def get_info(filename):

    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    filename = os.path.join("info", filename)

    if not os.path.exists(filename):
        # create empty file with a message
        with open(filename, 'w') as f:
            f.write("")
        return f"Nessuna informazione disponibile (file {filename} non trovato)."

    # check if file is empty
    if os.stat(filename).st_size == 0:
        return f"Nessuna informazione disponibile (file {filename} vuoto)."

    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines if not line.startswith("#")]
    return " ".join(lines)
